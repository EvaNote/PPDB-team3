from flask import request
from flask_restful import Resource, abort
from werkzeug.datastructures import MultiDict

from src.dbmodels.User import User
from src.utils import bcrypt, user_access
from src.users.forms import RegistrationForm


class RegisterApi(Resource):
    def post(self):
        if not all(key in request.json for key in ("username", "firstname", "lastname", "password")):
            abort(400, message="missing parameter(s) in body.")
        # create a MultiDict using the parameters in request.json. We use this data structure to easily
        # create a form and check if the input is valid
        form_data = MultiDict(mapping={
            "email": request.json.get("username") + "@campuscarpool.com",
            "first_name": request.json.get("firstname"),
            "last_name": request.json.get("lastname"),
            "password": request.json.get("password"),
            "confirm_password": request.json.get("password")
        })
        form = RegistrationForm(form_data, meta={'csrf': False})
        if form.validate():
            # if the form is valid, hash the password, add the user to the database and return its id
            user_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user_obj = User(form.first_name.data, form.last_name.data, form.email.data, user_password)
            user_access.add_user(user_obj)
            return {"id": user_access.get_user(form.email.data).id}, 201
        else:
            abort(400, message=form.errors)


class AuthApi(Resource):
    def post(self):
        if not all(key in request.json for key in ("username", "password")):
            abort(400, message="missing parameter(s) in body.")
        user = user_access.get_user(request.json.get("username") + "@campuscarpool.com")
        if user and bcrypt.check_password_hash(user.password, request.json.get("password")):
            # if user in database and password is correct, generate authentication token
            token = user.generate_auth_token()
            return {"token": token.decode("ascii")}
        return abort(401)
