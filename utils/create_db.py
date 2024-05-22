from models.Base import *
from services.db import engine

def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)