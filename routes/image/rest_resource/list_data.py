from flask import current_app
from config import success_msg, fail_msg
from flask_cors import cross_origin
from flask_restful import Resource

from routes.image.image_method import ImageMethod
image_method = ImageMethod(current_app)


class ListData(Resource):
    @cross_origin()
    def get(self, page, per_page):
        data = image_method.read_data_list(int(page), int(per_page))
        return success_msg(data), 200
