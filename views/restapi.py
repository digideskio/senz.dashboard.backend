from flask import Blueprint, render_template, request, session

restapi = Blueprint('restapi', __name__, template_folder='templates')
