from fastapi import Depends, FastAPI
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()
fakeDatabase = {
    1: {'user': 'Daniel'},
    2: {'user': 'João'},
    3: {'user': 'Antonio'},
}


##### Rotas da API #####

@app.get("/users")
def users(session: Session = Depends(get_session)):
    users = session.query(models.User).all()
    return users


@app.get("/users/{id}")
def get_user(id: int):
    return fakeDatabase[id]


@app.post("/users")
def add_user(user: schemas.User, session: Session = Depends(get_session)):
    user = models.User(name=user.name)
    session.add(user)
    session.commit()
    session .refresh(user)
    return user


@app.put("users/{id}")
def update_user(id: int, user: schemas.User, session: Session = Depends(get_session)):
    userObject = session.query(models.User).get(id)
    userObject.name = user.name
    session.commit()
    return userObject


@app.delete("/users/{id}")
def delete_user(id: int):
    del fakeDatabase[id]
    return fakeDatabase
