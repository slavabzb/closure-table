import sqlalchemy as sa

from .tables import comments, comments_tree


async def create(conn, content, parent_id=None):
    try:
        await conn.execute('BEGIN')

        query = comments.insert().values(content=content)
        comment_id = await conn.scalar(query)

        query = sa.select([comments_tree.c.depth + 1]).where(sa.and_(
            comments_tree.c.ancestor_id == parent_id,
            comments_tree.c.descendant_id == parent_id,
        ))
        depth = await conn.scalar(query)
        depth = depth or 0

        query = comments_tree.insert().values(
            ancestor_id=comment_id, nearest_ancestor_id=comment_id,
            descendant_id=comment_id, depth=depth
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


async def get_tree(conn, comment_id):
    query = sa.select([
        comments_tree.c.nearest_ancestor_id,
        comments.c.id,
        comments.c.content,
        comments.c.created,
        comments.c.updated,
    ]).select_from(comments.join(
        comments_tree, comments.c.id == comments_tree.c.descendant_id,
    )).where(comments_tree.c.ancestor_id == comment_id)
    rows = await conn.execute(query)
    tree = {}
    for row in rows:
        make_tree(tree, {
            'parent_id': row[0],
            'id': row[1],
            'content': row[2],
            'created': row[3].strftime('%c'),
            'updated': row[4].strftime('%c'),
            'children': [],
        })
    return tree


def make_tree(tree, data):
    if 'id' in tree:
        if tree['id'] == data['parent_id']:
            subtree = {}
            make_tree(subtree, data)
            tree['children'].append(subtree)
        else:
            for child in tree['children']:
                if child['id'] == data['parent_id']:
                    make_tree(child, data)
                    break
    else:
        for k, v in data.items():
            tree[k] = v
