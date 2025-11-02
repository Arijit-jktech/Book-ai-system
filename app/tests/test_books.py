async def get_auth_token(client, username="admin", password="adminpass"):
    resp = await client.post("/api/auth/token", data={"username":username,"password":password})
    return resp.json().get("access_token")

async def test_create_book_and_get(client):
    token = await get_auth_token(client)
    book = {"title":"Wings of Fire","author":"A.P.J Abdul Kalam","genre":"tech","year_published":2003}
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post("/api/books/", json=book, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    book_id = data["id"]

    r2 = await client.get(f"/api/books/{book_id}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Wings of Fire"
