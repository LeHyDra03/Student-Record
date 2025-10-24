import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    # The app's startup will create tables if DB available. Ensure DB is set, otherwise tests fail.
    pass


def test_create_and_get_student():
    payload = {"name": "Test User", "age": 18, "grade": "A", "email": "test@example.com"}
    r = client.post("/students/", json=payload)
    assert r.status_code == 200 or r.status_code == 201
    created = r.json()
    assert created["name"] == payload["name"]


    student_id = created["id"]
    r2 = client.get(f"/students/{student_id}")
    assert r2.status_code == 200
    assert r2.json()["email"] == payload["email"]


def test_update_and_delete_student():
    payload = {"name": "To Update", "age": 20, "grade": "B", "email": "upd@example.com"}
    r = client.post("/students/", json=payload)
    assert r.status_code in (200, 201)
    created = r.json()
    sid = created["id"]


    upd = {"name": "Updated Name"}
    r2 = client.put(f"/students/{sid}", json=upd)
    assert r2.status_code == 200
    assert r2.json()["name"] == "Updated Name"


    r3 = client.delete(f"/students/{sid}")
    assert r3.status_code == 200


    r4 = client.get(f"/students/{sid}")
    assert r4.status_code == 404