import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---- Reset database before each test ----
@pytest.fixture(autouse=True)
def reset_db():
    import main
    main.tasks_db.clear()
    main.task_counter = 1
    yield
    main.tasks_db.clear()
    main.task_counter = 1

# ============================================
# ROOT & HEALTH TESTS
# ============================================

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

# ============================================
# TASK CREATION TESTS
# ============================================

def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "priority": "high"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert data["completed"] == False
    assert data["id"] == 1

def test_create_task_default_values():
    response = client.post("/tasks", json={
        "title": "Simple Task"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["priority"] == "medium"
    assert data["description"] == ""

def test_create_multiple_tasks():
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    client.post("/tasks", json={"title": "Task 3"})
    response = client.get("/tasks")
    assert response.json()["total"] == 3

# ============================================
# GET TASKS TESTS
# ============================================

def test_get_all_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json()["total"] == 0

def test_get_task_by_id():
    client.post("/tasks", json={"title": "Find Me"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_filter_by_priority():
    client.post("/tasks", json={"title": "High Task", "priority": "high"})
    client.post("/tasks", json={"title": "Low Task", "priority": "low"})
    response = client.get("/tasks?priority=high")
    assert response.json()["total"] == 1
    assert response.json()["tasks"][0]["priority"] == "high"

def test_filter_by_completed():
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    client.put("/tasks/1", json={"completed": True})
    response = client.get("/tasks?completed=true")
    assert response.json()["total"] == 1

# ============================================
# UPDATE TASK TESTS
# ============================================

def test_update_task():
    client.post("/tasks", json={"title": "Old Title"})
    response = client.put("/tasks/1", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_complete_task():
    client.post("/tasks", json={"title": "Complete Me"})
    response = client.put("/tasks/1", json={"completed": True})
    assert response.json()["completed"] == True

def test_update_task_not_found():
    response = client.put("/tasks/999", json={"title": "Ghost"})
    assert response.status_code == 404

# ============================================
# DELETE TASK TESTS
# ============================================

def test_delete_task():
    client.post("/tasks", json={"title": "Delete Me"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404

def test_delete_removes_task():
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    client.delete("/tasks/1")
    response = client.get("/tasks")
    assert response.json()["total"] == 1

# ============================================
# STATS TESTS
# ============================================

def test_stats_empty():
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["total_tasks"] == 0

def test_stats_with_tasks():
    client.post("/tasks", json={"title": "T1", "priority": "high"})
    client.post("/tasks", json={"title": "T2", "priority": "low"})
    client.put("/tasks/1", json={"completed": True})
    response = client.get("/stats")
    data = response.json()
    assert data["total_tasks"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1
    assert data["by_priority"]["high"] == 1