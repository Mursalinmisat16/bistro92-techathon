from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./bistro.db"  # Or your PostgreSQL/MySQL URL
engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    with Session(engine) as db:
        yield db
