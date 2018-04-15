from closure_table.auth.db.tables import users


async def user_get(conn, email):
    query = users.select(users.c.email == email)
    result = await conn.execute(query)
    row = await result.fetchone()
    if row:
        return {
            'id': row[0],
            'email': row[1],
            'password': row[2],
        }
    return {}
