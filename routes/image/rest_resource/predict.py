from flask import current_app, request
from config import success_msg, fail_msg
from flask_cors import cross_origin
from flask_restful import Resource

from routes.image.image_method import ImageMethod
image_method = ImageMethod(current_app)


class Predict(Resource):
    @cross_origin
    def post(self):
        file = request.files['file']

        if file:
            result = image_method.predict_image(file)

            return success_msg({"extract": result}), 200
        else:
            return fail_msg("file is not exist"), 200
