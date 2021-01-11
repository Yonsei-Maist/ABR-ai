from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api

from flask_cors import cross_origin
from config import success_msg, fail_msg

from routes.image.image_method import ImageMethod

image_api = Blueprint('image_api', __name__)

api = Api(image_api)

image_method = ImageMethod(current_app)


@image_api.route("/origin/upload", methods=['POST'])
@cross_origin()
def upload_origin():
    file = request.files['file']

    if file:
        image_method.upload_origin(file)

        return jsonify(success_msg())
    else:
        return fail_msg("file is not exist")


@image_api.route("/network", methods=["GET"])
def capture():
    image_method.capture_network()

    return success_msg()


@image_api.route("/predict", methods=['POST'])
def predict_image():
    file = request.files['file']

    if file:
        result = image_method.predict_image(file)

        return success_msg({"extract": result})
    else:
        return fail_msg("file is not exist")


@image_api.route("/data/<int:page>/<int:per_page>")
@cross_origin()
def read_data_list(page, per_page):
    data = image_method.read_data_list(int(page), int(per_page))

    return success_msg(data)


@image_api.route("/data/one/<int:id_data>")
@cross_origin()
def read_data_detail(id_data):
    data = image_method.read_data_detail(id_data)

    if data is None or len(data) == 0:
        return fail_msg("Not Exists.")
    return success_msg({"valueList": data})
