from flask import Blueprint, request, jsonify, current_app

from flask_cors import cross_origin
from config import success_msg, fail_msg

from routes.image.image_method import ImageMethod

image_api = Blueprint('image_api', __name__)

image_method = ImageMethod(current_app)


@image_api.route("/abr/image/origin/upload", methods=['POST'])
@cross_origin()
def upload_origin():
    file = request.files['file']

    if file:
        image_method.upload_origin(file)
        return jsonify(success_msg(request.values['id']))
    else:
        return fail_msg(request.values["id"], "file is not exist")


@image_api.route("/abr/image/network", methods=["GET"])
def capture():
    image_method.capture_network()

    return success_msg(request.values['id'])


@image_api.route("/abr/image/predict", methods=['POST'])
def predict_image():
    file = request.files['file']

    if file:
        result = image_method.predict_image(file)

        return success_msg(request.values["id"], {"extract": result})
    else:
        return fail_msg(request.values["id"], "file is not exist")
