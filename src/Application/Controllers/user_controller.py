from flask import request
from src.Application.Service.user_service import UserService

service = UserService()

def register():
    data = request.json
    return service.register_user(data)

def activate():
    data = request.json
    return service.activate_user(data['email'], data['code'])

def login():
    data = request.json
    return service.login(data)
