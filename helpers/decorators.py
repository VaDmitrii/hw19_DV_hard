import jwt
from flask import request
from flask_restx import abort

from hw19_DV_hard.helpers.constants import ALGORITHM, SECRET_HERE


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, SECRET_HERE, algorithms=[ALGORITHM])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split('Bearer ')[-1]
        role = None

        try:
            user = jwt.decode(token, SECRET_HERE, algorithms=[ALGORITHM])
            role = user.get("role")
        except Exception as e:
            print(f"JWT exception - {str(e)}")
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
