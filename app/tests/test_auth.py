async def test_token_bad_credentials(client):
    resp = await client.post("/api/auth/token", data={"username":"no","password":"bad"})
    assert resp.status_code == 400

async def test_token_ok(client):
    resp = await client.post("/api/auth/token", data={"username":"admin","password":"adminpass"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
