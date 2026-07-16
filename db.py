from sqlalchemy import create_engine
from models import UserBase

engine = create_engine("sqlite:///users.db")
UserBase.metadata.create_all(engine)
