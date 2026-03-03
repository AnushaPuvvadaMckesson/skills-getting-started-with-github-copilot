import pytest

@pytest.mark.asyncio
async def test_activity_listing(async_client):
    response = await async_client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_success(async_client):
    # Use a unique email to avoid duplicate error
    response = await async_client.post("/activities/Chess%20Club/signup?email=tester1@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")

@pytest.mark.asyncio
async def test_signup_duplicate(async_client):
    # First signup
    await async_client.post("/activities/Programming%20Class/signup?email=tester2@mergington.edu")
    # Duplicate signup
    response = await async_client.post("/activities/Programming%20Class/signup?email=tester2@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_signup_nonexistent_activity(async_client):
    response = await async_client.post("/activities/Nonexistent/signup?email=tester3@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json().get("detail", "")
