from flask import current_app, request
from config import success_msg, fail_msg
from flask_cors import cross_origin
from flask_restful import Resource

from routes.image.image_method import ImageMethod
image_method = ImageMethod(current_app)


class DetailData(Resource):
    @cross_origin
    def get(self, id_data):
        data = image_method.read_data_detail(id_data)

        return success_msg(data), 200
