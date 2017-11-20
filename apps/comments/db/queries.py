from sqlalchemy import select, and_

from .tables import comments, comments_tree


async def create_comment(conn, content, parent_id=None):
    comment_id = await conn.scalar(comments.insert().values(content=content))
    await conn.execute(comments_tree.insert().values(
        ancestor_id=comment_id, descendant_id=comment_id, level=0
    ))
    if parent_id:
        ct1 = comments_tree.alias('ct1')
        ct2 = comments_tree.alias('ct2')
        query = select([
            ct1.c.ancestor_id,
            ct2.c.descendant_id,
            ct1.c.level + ct2.c.level + 1
        ]).where(and_(
            ct1.c.descendant_id == parent_id,
            ct2.c.ancestor_id == comment_id,
        ))
        query = comments_tree.insert().from_select(select=query, names=[
            'ancestor_id',
            'descendant_id',
            'level'
        ])
        await conn.execute(query)
    return comment_id


async def get_tree(conn, comment_id):
    join = comments_tree.join(
        comments, comments_tree.c.descendant_id == comments.c.id
    )
    query = select([comments_tree.c.level, comments]).select_from(join) \
        .where(comments_tree.c.ancestor_id == comment_id)
    tree = {}
    rows = await conn.execute(query).fetchall()
    for row in rows:
        make_tree(tree, level=row[0], comment_id=row[1], content=row[2])
    return tree


def make_tree(tree, comment_id, content, level):
    if level == 0:
        tree['id'] = comment_id
        tree['content'] = content
        tree['children'] = []
    else:
        subtree = {}
        make_tree(subtree, comment_id, content, level - 1)
        tree['children'].append(subtree)
