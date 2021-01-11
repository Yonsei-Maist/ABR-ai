from imagelib.extractor import Extractor
from lib.data import DataMaker
from database.datamanager.dao import DataManager
from network.RNN import Net

import os
import cv2
import datetime
import uuid

net = Net('./data/Response-result-origin.txt')
extractor = Extractor()
data_maker = DataMaker()


class ImageMethod:
    def __init__(self, app):
        self.app = app

    def create_dao(self):
        return DataManager(
            self.app.config["DATABASE_HOST"],
            self.app.config["DATABASE"],
            self.app.config["DATABASE_USER"],
            self.app.config["DATABASE_PASSWORD"]
        )

    def upload_origin(self, file):
        new_filename = uuid.uuid4().hex + "." + file.filename.split('.')[1]
        now = datetime.datetime.now()
        frpath = os.path.join(str(now.year), str(now.month), str(now.day))
        full_frpath = os.path.join(self.app.config["FILE_PATH"], frpath)
        if not os.path.exists(full_frpath):
            os.makedirs(full_frpath)

        rpath = os.path.join(frpath, new_filename)
        fpath = os.path.join(self.app.config["FILE_PATH"], rpath)
        file.save(fpath)

        image = cv2.imread(fpath)
        data_manager = self.create_dao()
        data_manager.insert_data(rpath, file.filename)
        cropped_image = data_maker.crop(image)
        left_graph, right_graph = data_maker.get_graph(cropped_image)

        result = []
        result.extend(data_maker.to_obj_list(left_graph, False, 660))
        result.extend(data_maker.to_obj_list(right_graph, True, 660))

        data_manager.insert_values(result, fpath)

    def predict_image(self, file):
        fpath = os.path.join(self.app.config["FILE_PATH"], file.filename)
        file.save(fpath)

        vector = extractor.extract(fpath, 667, True)
        tensor = net.vector_to_data(vector, 660)
        predict = net.predict(196, tensor)

        pred = net.to_top_predict(predict)

        result = []
        for i in range(len(vector)):
            result.append({
                "graph": vector[i],
                "peak": pred[i]
            })

        return result

    def capture_network(self):
        net.capture_image(196, "")

    def read_data_list(self, page, per_page):

        data_manager = self.create_dao()
        return data_manager.select_data_list(page, per_page)

    def read_data_detail(self, id_data):
        data_manager = self.create_dao()
        return data_manager.select_data_one(id_data)
