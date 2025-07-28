from datetime import datetime
from sqlalchemy import text


def test_create_task(client, db_session):

    time = datetime.now()

    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (1, 'Pending', 1)"))
    db_session.execute(
        text("INSERT INTO task_list (id, name, active, created_at) VALUES (:id, :name, :active, :created_at)"),
        {"id": 1, "name": "Lista 1", "active": 1, "created_at": time}
    )
    db_session.commit()

    response = client.post("/tasks/", json={
        "title": "Tarea de prueba",
        "description": "Probando el test",
        "status_id": 1,
        "task_list_id": 1
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_task_by_id(client, db_session):

    time = datetime.now()

    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (1, 'Pending', 1)"))
    db_session.execute(
        text("INSERT INTO task_list (id, name, active, created_at) VALUES (:id, :name, :active, :created_at)"),
        {"id": 1, "name": "Lista 1", "active": 1, "created_at": time}
    )
    db_session.commit()

    create_response = client.post("/tasks/", json={
        "title": "Tarea para obtener",
        "description": "Descripción para obtener",
        "status_id": 1,
        "task_list_id": 1
    })
    task_id = create_response.json()["id"]

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == task_id
    assert data["title"] == "Tarea para obtener"
    assert data["description"] == "Descripción para obtener"


def test_get_all_tasks(client, db_session):

    time = datetime.now()

    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (1, 'Pending', 1)"))
    db_session.execute(
        text("INSERT INTO task_list (id, name, active, created_at) VALUES (:id, :name, :active, :created_at)"),
        {"id": 1, "name": "Lista 1", "active": 1, "created_at": time}
    )
    db_session.commit()

    client.post("/tasks/", json={
        "title": "Tarea 1",
        "description": "Descripción 1",
        "status_id": 1,
        "task_list_id": 1
    })
    client.post("/tasks/", json={
        "title": "Tarea 2",
        "description": "Descripción 2",
        "status_id": 1,
        "task_list_id": 1
    })

    response = client.get("/tasks/all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_task_by_filters(client, db_session):

    time = datetime.now()

    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (1, 'Pending', 1)"))
    db_session.execute(
        text("INSERT INTO task_list (id, name, active, created_at) VALUES (:id, :name, :active, :created_at)"),
        {"id": 1, "name": "Lista 1", "active": 1, "created_at": time}
    )
    db_session.commit()

    client.post("/tasks/", json={
        "title": "Filtro Test 1",
        "description": "Descripción filtro test 1",
        "status_id": 1,
        "task_list_id": 1
    })
    client.post("/tasks/", json={
        "title": "Filtro Test 2",
        "description": "Descripción filtro test 2",
        "status_id": 1,
        "task_list_id": 1
    })

    response = client.get("/tasks/", params={"title": "Filtro Test 1"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("Filtro Test 1" in task["title"] for task in data)


def test_update_task(client, db_session):
    time = datetime.now()

    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (1, 'Pending', 1)"))
    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (2, 'In Progress', 1)"))
    db_session.execute(
        text("INSERT INTO task_list (id, name, active, created_at) VALUES (:id, :name, :active, :created_at)"),
        {"id": 1, "name": "Lista 1", "active": 1, "created_at": time}
    )
    db_session.commit()
    create_response = client.post("/tasks/", json={
        "title": "Tarea a actualizar",
        "description": "Descripción antes",
        "status_id": 1,
        "task_list_id": 1
    })
    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={"status_id": 2})

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status_id"] == 2


def test_delete_task(client, db_session):

    time = datetime.now()

    db_session.execute(text("INSERT INTO task_status (id, name, active) VALUES (1, 'Pending', 1)"))
    db_session.execute(
        text("INSERT INTO task_list (id, name, active, created_at) VALUES (:id, :name, :active, :created_at)"),
        {"id": 1, "name": "Lista 1", "active": 1, "created_at": time}
    )
    db_session.commit()

    create_response = client.post("/tasks/", json={
        "title": "Tarea a eliminar",
        "description": "Descripción para borrar",
        "status_id": 1,
        "task_list_id": 1
    })

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Task deleted successfully"}

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
