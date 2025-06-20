from sqlmodel import SQLModel, Field, create_engine

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

engine = create_engine('sqlite:///users.db', connect_args={"check_same_thread": False})
