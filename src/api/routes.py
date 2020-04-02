from flask import Blueprint, request, jsonify, abort
from werkzeug.datastructures import MultiDict

from src.dbmodels.User import User
from src.utils import user_access, bcrypt
from users.forms import RegistrationForm

api = Blueprint('app', __name__, url_prefix='/api')


@api.route("/users/register", methods=['GET', 'POST'])
def register():
    if not request.json or "firstname" not in request.json or "lastname" not in request.json or "password" not in request.json:
        abort(400)
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
        return jsonify({"id": user_access.get_user(form.email.data).id}), 201
    else:
        abort(400, form.errors)
