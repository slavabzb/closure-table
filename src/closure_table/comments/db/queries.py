import sqlalchemy as sa
from closure_table.comments.db.tables import (
    comments,
    comments_tree,
)
from sqlalchemy.sql.expression import func


async def comment_create(conn, content, parent_id=None):
    await conn.execute('BEGIN')
    try:
        query = comments.insert().values(content=content)
        comment_id = await conn.scalar(query)
        query = sa.select([comments_tree.c.depth + 1]).where(sa.and_(
            comments_tree.c.ancestor_id == parent_id,
            comments_tree.c.descendant_id == parent_id,
        ))
        depth = await conn.scalar(query)
        query = comments_tree.insert().values(
            ancestor_id=comment_id, nearest_ancestor_id=comment_id,
            descendant_id=comment_id, depth=depth or 0
        )
        await conn.execute(query)
        if parent_id:
            ancestor = comments_tree.alias('ancestor')
            descendant = comments_tree.alias('descendant')
            nearest = comments_tree.alias('nearest')
            query = sa.select([
                descendant.c.ancestor_id,
                nearest.c.nearest_ancestor_id,
                ancestor.c.descendant_id,
                nearest.c.depth + 1
            ]).where(sa.and_(
                descendant.c.descendant_id == parent_id,
                ancestor.c.ancestor_id == comment_id,
                nearest.c.ancestor_id == parent_id,
                nearest.c.descendant_id == parent_id,
            ))
            query = comments_tree.insert().from_select([
                comments_tree.c.ancestor_id,
                comments_tree.c.nearest_ancestor_id,
                comments_tree.c.descendant_id,
                comments_tree.c.depth,
            ], query)
            # INSERT INTO comments_tree
            #   (ancestor_id, nearest_ancestor_id, descendant_id, depth)
            # SELECT
            #   descendant.ancestor_id,
            #   nearest.nearest_ancestor_id,
            #   ancestor.descendant_id,
            #   nearest.depth + 1
            # FROM
            #   comments_tree AS descendant,
            #   comments_tree AS nearest,
            #   comments_tree AS ancestor
            # WHERE descendant.descendant_id = PARENT_ID
            #   AND ancestor.ancestor_id = COMMENT_ID
            #   AND nearest.ancestor_id = PARENT_ID
            #   AND nearest.descendant_id = PARENT_ID
            await conn.execute(query)
    except:
        await conn.execute('ROLLBACK')
        raise
    else:
        await conn.execute('COMMIT')
    return comment_id


async def comment_get(conn):
    query = sa.select([
        comments.c.id,
        comments.c.content,
    ]).select_from(comments.join(
        comments_tree, comments.c.id == comments_tree.c.descendant_id,
    )).where(comments_tree.c.depth == 0)
    comment_list = []
    async for row in await conn.execute(query):
        tree = {}
        await make_tree(tree, {
            'id': row[0],
            'content': row[1],
        })
        comment_list.append(tree)
    return comment_list


async def comment_get_tree(conn, comment_id):
    query = sa.select([
        comments_tree.c.nearest_ancestor_id,
        comments.c.id,
        comments.c.content,
    ]).select_from(comments.join(
        comments_tree, comments.c.id == comments_tree.c.descendant_id,
    )).where(comments_tree.c.ancestor_id == comment_id)
    # SELECT
    #   comments_tree.nearest_ancestor_id,
    #   comments_comments.id,
    #   comments_comments.content
    # FROM
    #   comments_comments
    # JOIN comments_tree ON comments_comments.id = comments_tree.descendant_id
    # WHERE comments_tree.ancestor_id = COMMENT_ID
    tree = {}
    async for row in await conn.execute(query):
        await make_tree(tree, {
            'parent_id': row[0],
            'id': row[1],
            'content': row[2],
            'children': [],
        })
    return tree


async def make_tree(tree, data):
    if 'id' in tree:
        if tree['id'] == data['parent_id']:
            subtree = {}
            await make_tree(subtree, data)
            tree['children'].append(subtree)
        else:
            for child in tree['children']:
                await make_tree(child, data)
    else:
        for k, v in data.items():
            tree[k] = v


async def comment_update(conn, comment_id, content):
    query = comments.update().where(comments.c.id == comment_id).values(
        content=content
    )
    result = await conn.execute(query)
    return result.rowcount


async def comment_delete(conn, comment_id):
    await conn.execute('BEGIN')
    try:
        remove = comments_tree.alias('remove')
        descendant = comments_tree.alias('descendant')
        query = sa.select([remove.c.descendant_id, remove.c.id]).where(sa.and_(
            sa.or_(
                remove.c.ancestor_id == descendant.c.descendant_id,
                remove.c.nearest_ancestor_id == descendant.c.descendant_id,
                remove.c.descendant_id == descendant.c.descendant_id,
            ),
            descendant.c.ancestor_id == comment_id
        ))
        # SELECT
        #   remove.descendant_id,
        #   remove.id
        # FROM
        #   comments_tree AS remove,
        #   comments_tree AS descendant
        # WHERE (remove.ancestor_id = descendant.descendant_id
        #       OR remove.nearest_ancestor_id = descendant.descendant_id
        #       OR remove.descendant_id = descendant.descendant_id)
        #   AND descendant.ancestor_id = COMMENT_ID
        comment_ids = set()
        comment_tree_ids = set()
        async for row in conn.execute(query):
            comment_ids.add(row[0])
            comment_tree_ids.add(row[1])
        if comment_tree_ids:
            query = comments_tree.delete().where(comments_tree.c.id.in_(
                comment_tree_ids
            ))
            await conn.execute(query)
        if comment_ids:
            query = comments.delete().where(comments.c.id.in_(
                comment_ids
            ))
            await conn.execute(query)
    except:
        await conn.execute('ROLLBACK')
        raise
    else:
        await conn.execute('COMMIT')
    return len(comment_ids)


async def comment_search(conn, content):
    result = []
    query = sa.select([comments]).where(comments.c.content.match(
        sa.cast(func.plainto_tsquery(content), sa.TEXT)
    ))
    # SELECT
    #   comments_comments.id,
    #   comments_comments.content
    # FROM
    #   comments_comments
    # WHERE
    #   comments_comments.content @@ to_tsquery(
    #       CAST(plainto_tsquery('query text') AS TEXT)
    #   )
    async for row in conn.execute(query):
        result.append({
            'id': row[0],
            'content': row[1],
        })
    return result
