"""
@Author Chanwoo Kwon, Yonsei Univ. Researcher since 2020.05~
"""
from flask import Flask, request, render_template, g
from flask_cors import CORS

import sys

from config import config_by_name, fail_msg
from lib.ip import IPLocation
from routes.ai.ai_api import ai_api
from routes.image.image_api import image_api

from lib.crypto import AESCipher

app = Flask(__name__)
app.register_blueprint(ai_api)
app.register_blueprint(image_api, url_prefix="/abr/image/")

CORS(app, resources={r'/abr/image/*': {'origins': '*'}})


@app.before_request
def before():
    # show ip
    ip = request.remote_addr
    print("location: ", IPLocation.get_region(ip))


# @app.route('/')
# def home():
#     return render_template('react-abr-manager/index.html')


@app.errorhandler(Exception)
def handle_error(e):
    return fail_msg(str(e))


if __name__ == "__main__":
    config_name = sys.argv[2]
    app.config.from_object(config_by_name[config_name])
    app.run(host="0.0.0.0", port=app.config["PORT"])
