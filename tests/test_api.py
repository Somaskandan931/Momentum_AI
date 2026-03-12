"""
API integration tests using pytest + httpx.
Run: pytest tests/test_api.py -v
"""
import pytest
import httpx

BASE_URL = "http://localhost:8000/api"
TEST_USER = {"username": "test@example.com", "password": "testpassword123"}
ACCESS_TOKEN = None


@pytest.fixture(scope="session")
def auth_headers():
    """Register and login to get auth token."""
    # Register
    httpx.post(f"{BASE_URL}/auth/register", json={
        "name": "Test User",
        "email": TEST_USER["username"],
        "password": TEST_USER["password"],
        "skills": ["Python"],
        "role": "Developer"
    })
    # Login
    response = httpx.post(f"{BASE_URL}/auth/login", data=TEST_USER)
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


def test_root():
    r = httpx.get("http://localhost:8000/")
    assert r.status_code == 200
    assert "running" in r.json()["message"]


def test_register_duplicate(auth_headers):
    r = httpx.post(f"{BASE_URL}/auth/register", json={
        "name": "Test User",
        "email": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    assert r.status_code == 400


def test_create_project(auth_headers):
    r = httpx.post(f"{BASE_URL}/projects/", json={
        "title": "Test Project",
        "description": "A test project for unit testing"
    }, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test Project"
    return data["id"]


def test_list_projects(auth_headers):
    r = httpx.get(f"{BASE_URL}/projects/", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_task(auth_headers):
    # First create a project
    pr = httpx.post(f"{BASE_URL}/projects/", json={
        "title": "Task Test Project", "description": "desc"
    }, headers=auth_headers)
    project_id = pr.json()["id"]

    r = httpx.post(f"{BASE_URL}/tasks/", json={
        "project_id": project_id,
        "title": "Test Task",
        "description": "A test task",
        "priority": "high",
        "estimated_time": 60
    }, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["title"] == "Test Task"


def test_update_task_status(auth_headers):
    pr = httpx.post(f"{BASE_URL}/projects/", json={"title": "P", "description": "D"}, headers=auth_headers)
    project_id = pr.json()["id"]
    tr = httpx.post(f"{BASE_URL}/tasks/", json={
        "project_id": project_id, "title": "T", "estimated_time": 30
    }, headers=auth_headers)
    task_id = tr.json()["id"]

    r = httpx.patch(f"{BASE_URL}/tasks/{task_id}", json={"status": "In Progress"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "In Progress"
