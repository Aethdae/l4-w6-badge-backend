from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from db import engine

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:*", "http://localhost:*"])

@app.route("/")
def home():
    return {"status": "healthy"}, 200

@app.get("/api/users")
def get_users():
    with Session(engine) as session:
        users = session.scalars(select(User)).all()
        users_to_dict = [user.to_dict() for user in users]
        return {"users": users_to_dict}, 200
    return {"error": "Error fetching users."}, 500

@app.post("/api/users")
def add_user():
    req = request.json
    if User.can_be_user(req):
        with Session(engine) as session:
            user = User(first_name=req.get("first_name"), last_name=req.get("last_name"), role=req.get("role", "user"))
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"user": user.to_dict()}
    else:
        return {"error" : "User missing information."}, 415
    
@app.patch("/api/users/<int:id>")
def update_user(id):
    with Session(engine) as session:
        user = session.get(User, id)

        if (user):
            req = request.json
            user.update(req)
            session.commit()
            return {"user": user.to_dict(), "status": "updated"}, 202
        else:
            return {"error": "User not found."}, 404

@app.delete("/api/users/<int:id>")
def delete_user(id):
    with Session(engine) as session:
        user = session.get(User, id)
        session.delete(user)
        session.commit()
        return {"status": "deleted", "id": id}, 200
    

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
