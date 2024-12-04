from flask import Blueprint, redirect, render_template, request, make_response, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5')
def lab():
    return render_template('lab5/lab5.html')