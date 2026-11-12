import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import event


from main import app  
from app.db.connect import get_db
from app.models.model import Base, РолиM

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=OFF")
    cursor.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Создает таблицы и предсоздаёт роли перед всеми тестами."""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        db.add_all([
            РолиM(роль_id=1, название_роли="админ"),
            РолиM(роль_id=2, название_роли="менеджер"),
            РолиM(роль_id=3, название_роли="оператор"),
            РолиM(роль_id=4, название_роли="клиент"),
        ])
        db.commit()
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Очищает таблицы перед каждым тестом."""
    yield
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            if table.name == "роли":
                connection.execute(
                    table.delete().where(table.c.роль_id > 4)
                )
            else:
                connection.execute(table.delete())


@pytest.fixture(scope="function")
def client():
    """Возвращает TestClient с подмененной БД."""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()