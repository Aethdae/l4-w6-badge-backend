from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

UserBase = declarative_base()

class User(UserBase):
    def __init__(self, first_name, last_name, role="user", id=None ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role
        }
    
    def update(self, json):
        self.first_name = json.get("first_name", self.first_name)
        self.last_name = json.get("last_name", self.last_name)
        self.role = json.get("role", self.role)
    
    @staticmethod
    def can_be_user(json):
        return json.get("first_name") and json.get("last_name") 
