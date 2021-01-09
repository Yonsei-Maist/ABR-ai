from flask import Blueprint, render_template, session,abort

ai_api = Blueprint('ai_api',__name__)
@ai_api.route("/world")
def world():
    return "Hello World from app 2!"