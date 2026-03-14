import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

# --- Mock the DB before importing the app ---
mock_db = MagicMock()
mock_db.users.find_one = AsyncMock(return_value=None)
mock_db.users.insert_one = AsyncMock(return_value=MagicMock(inserted_id="abc123"))
mock_db.users.update_one = AsyncMock(return_value=None)
mock_db.projects.find_one = AsyncMock(return_value=None)
mock_db.projects.insert_one = AsyncMock(return_value=MagicMock(inserted_id="proj123"))
mock_db.projects.find = MagicMock(return_value=AsyncMock(__aiter__=MagicMock(return_value=iter([]))))
mock_db.tasks.insert_one = AsyncMock(return_value=MagicMock(inserted_id="task123"))
mock_db.tasks.find_one = AsyncMock(return_value=None)

with patch("app.database.mongodb.get_db", return_value=mock_db), \
     patch("app.database.mongodb.connect_db", new_callable=AsyncMock), \
     patch("app.database.mongodb.disconnect_db", new_callable=AsyncMock):
    from backend.app.main import app

client = TestClient(app)

TEST_USER = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123",
    "skills": ["Python"],
    "role": "Developer"
}

# Valid 24-character hex ObjectId for use in task tests
VALID_TASK_ID = "507f1f77bcf86cd799439011"


# ──────────────────────────────────────────
# Auth is now optional — no token needed.
# Helper kept for routes that still accept one.
# ──────────────────────────────────────────
def get_auth_headers():
    from app.auth.jwt_handler import create_access_token
    token = create_access_token({"sub": "abc123"})
    return {"Authorization": f"Bearer {token}"}


# ──────────────────────────────────────────
# Tests
# ──────────────────────────────────────────
def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Momentum AI API is running"}


def test_register_user():
    mock_db.users.find_one = AsyncMock(return_value=None)  # no existing user
    mock_db.users.insert_one = AsyncMock(return_value=MagicMock(inserted_id="newuser1"))

    # Patch pwd_context.hash to bypass bcrypt>=4.1.0 / passlib incompatibility.
    with patch("app.auth.auth_routes.pwd_context.hash", return_value="hashed_password"):
        r = client.post("/api/auth/register", json=TEST_USER)

    assert r.status_code == 201
    assert "id" in r.json()


def test_register_duplicate():
    # Simulate email already exists
    mock_db.users.find_one = AsyncMock(return_value={"email": TEST_USER["email"]})

    r = client.post("/api/auth/register", json=TEST_USER)
    assert r.status_code == 400
    assert r.json()["detail"] == "Email already registered"


def test_login_invalid_credentials():
    mock_db.users.find_one = AsyncMock(return_value=None)  # user not found

    r = client.post("/api/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpass"
    })
    assert r.status_code == 401


def test_create_project():
    headers = get_auth_headers()
    mock_db.projects.insert_one = AsyncMock(return_value=MagicMock(inserted_id="proj1"))
    mock_db.projects.find_one = AsyncMock(return_value={
        "_id": "proj1",
        "title": "My Project",
        "description": "A test project",
        "creator_id": "abc123",
        "team_members": [],
        "roles": {},
        "idea_survival_score": None,
        "trend_analysis": {"competition_level": "unknown", "suggested_improvements": []},
        "status": "active",
        "created_at": "2024-01-01T00:00:00"
    })

    r = client.post("/api/projects/", json={
        "title": "My Project",
        "description": "A test project"
    }, headers=headers)
    assert r.status_code == 201
    assert r.json()["title"] == "My Project"


def test_list_projects():
    headers = get_auth_headers()

    async def mock_async_iter():
        return
        yield  # makes it an async generator

    mock_db.projects.find = MagicMock(return_value=mock_async_iter())

    r = client.get("/api/projects/", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_task():
    headers = get_auth_headers()
    mock_db.tasks.insert_one = AsyncMock(return_value=MagicMock(inserted_id="task1"))
    mock_db.tasks.find_one = AsyncMock(return_value={
        "_id": "task1",
        "project_id": "proj1",
        "title": "Build login page",
        "description": "Create the login UI",
        "priority": "high",
        "assigned_to": None,
        "status": "To Do",
        "deadline": None,
        "estimated_time": 90,
        "created_by_ai": False,
        "created_at": "2024-01-01T00:00:00"
    })

    r = client.post("/api/tasks/", json={
        "project_id": "proj1",
        "title": "Build login page",
        "description": "Create the login UI",
        "priority": "high",
        "estimated_time": 90
    }, headers=headers)
    assert r.status_code == 201
    assert r.json()["title"] == "Build login page"


def test_update_task_status():
    headers = get_auth_headers()
    mock_db.tasks.update_one = AsyncMock(return_value=None)
    mock_db.tasks.find_one = AsyncMock(return_value={
        # FIX 2: Use a valid 24-character hex ObjectId string instead of "task1".
        # task_service.py calls ObjectId(task_id) which requires a proper hex ObjectId.
        "_id": VALID_TASK_ID,
        "project_id": "proj1",
        "title": "Build login page",
        "description": "",
        "priority": "high",
        "assigned_to": None,
        "status": "In Progress",
        "deadline": None,
        "estimated_time": 90,
        "created_by_ai": False,
        "created_at": "2024-01-01T00:00:00"
    })

    r = client.patch(f"/api/tasks/{VALID_TASK_ID}", json={"status": "In Progress"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "In Progress"