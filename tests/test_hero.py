from fastapi import status

from sqlmodel import delete
from app.models import Hero
from app.utils.hashing import generate_hashed_password




def test_create_hero(client_fixture):
    response = client_fixture.post(
        "/heroes/",
        json={"name": "Deadpond", "secret_name": "Wade Wilson", "password": "chimichanga"},
    )
    
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Wade Wilson"
    assert data["age"] is None
    assert "id" in data
    assert isinstance(data["id"], int)


def test_create_hero_incomplete(client_fixture):
    response = client_fixture.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_hero_invalid(client_fixture):
    response = client_fixture.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": {"message": "Do you know your identity?"},
        "hashed_password": generate_hashed_password("chimichanga")
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_heroes(session_fixture, client_fixture):
    # Clear the database before test
    session_fixture.exec(delete(Hero))
    session_fixture.commit()

    # Add 2 test heroes to the database
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", hashed_password=generate_hashed_password("dead@pond"))
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, hashed_password=generate_hashed_password("rusty@man"))
    session_fixture.add(hero_1)
    session_fixture.add(hero_2)
    session_fixture.commit()


    response = client_fixture.get("/heroes/")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert isinstance(data, list)
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] is None
    assert "id" in data[0]
    assert isinstance(data[0]["id"], int)

    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert "id" in data[1]
    assert isinstance(data[1]["id"], int)

def test_read_hero(session_fixture, client_fixture):
    session_fixture.exec(delete(Hero))
    session_fixture.commit()

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", hashed_password=generate_hashed_password("dead@pond"))
    session_fixture.add(hero_1)
    session_fixture.commit()

    response = client_fixture.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] is None
    assert "id" in data
    assert isinstance(data["id"], int)


def test_update_hero(session_fixture, client_fixture):
    session_fixture.exec(delete(Hero))
    session_fixture.commit()

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", hashed_password=generate_hashed_password("dead@pond"))
    session_fixture.add(hero_1)
    session_fixture.commit()

    response = client_fixture.patch(
        f"/heroes/{hero_1.id}",
        json={"age": 30},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] == 30
    assert "id" in data
    assert isinstance(data["id"], int)

def test_delete_hero(session_fixture, client_fixture):
    session_fixture.exec(delete(Hero))
    session_fixture.commit()

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", hashed_password=generate_hashed_password("dead@pond"))
    session_fixture.add(hero_1)
    session_fixture.commit()

    response = client_fixture.delete(f"/heroes/{hero_1.id}")
    hero_in_db = session_fixture.get(Hero, hero_1.id)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert hero_in_db is None

    response = client_fixture.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == "Hero not found"
