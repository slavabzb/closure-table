from datetime import datetime

import sqlalchemy as sa

from .tables import comments, comments_tree


async def comment_create(conn, content, parent_id=None):
    await conn.execute('BEGIN')
    try:
        query = comments.insert().values(
            content=content, created=datetime.utcnow(),
            updated=datetime.utcnow()
        )
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
        comments.c.created,
        comments.c.updated,
    ]).select_from(comments.join(
        comments_tree, comments.c.id == comments_tree.c.descendant_id,
    )).where(comments_tree.c.depth == 0)
    comment_list = []
    async for row in await conn.execute(query):
        tree = {}
        await make_tree(tree, {
            'id': row[0],
            'content': row[1],
            'created': row[2].strftime('%c'),
            'updated': row[3].strftime('%c'),
        })
        comment_list.append(tree)
    return comment_list


async def comment_get_tree(conn, comment_id):
    query = sa.select([
        comments_tree.c.nearest_ancestor_id,
        comments.c.id,
        comments.c.content,
        comments.c.created,
        comments.c.updated,
    ]).select_from(comments.join(
        comments_tree, comments.c.id == comments_tree.c.descendant_id,
    )).where(comments_tree.c.ancestor_id == comment_id)
    tree = {}
    async for row in await conn.execute(query):
        await make_tree(tree, {
            'parent_id': row[0],
            'id': row[1],
            'content': row[2],
            'created': row[3].strftime('%c'),
            'updated': row[4].strftime('%c'),
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
        content=content, updated=datetime.utcnow()
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
    query = comments.select(comments.c.content.match(content))
    result = []
    async for row in conn.execute(query):
        result.append({
            'id': row[0],
            'content': row[1],
            'created': row[2].strftime('%c'),
            'updated': row[3].strftime('%c'),
        })
    return result
