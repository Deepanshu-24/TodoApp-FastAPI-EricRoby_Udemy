from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from ..main import app
from ..database import Base
from ..models import Todos, Users
from ..routers.todos import get_db, get_current_user
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context



SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                        connect_args= {"check_same_thread": False}, 
                        poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# ----------------------------
# DB Override
# ----------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# ----------------------------
# Auth Override
# ----------------------------
def override_get_current_user():
    return {"username": "Deepanshutest", "id": 1, "user_role": "admin"}

app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)



@pytest.fixture
def test_todo():


    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()

    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="Deepanshutest",
        email="Deepanshutest@email.com",
        first_name="Deepanshu",
        last_name="Saini",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()