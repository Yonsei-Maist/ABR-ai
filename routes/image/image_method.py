from imagelib.extractor import Extractor
from lib.data import DataMaker
from database.datamanager.dao import DataManager
from network.RNN import Net

import os
import cv2

net = Net('./data/Response-result-origin.txt')
extractor = Extractor()
data_maker = DataMaker()


class ImageMethod:
    def __init__(self, app):
        self.app = app

    def upload_origin(self, file):
        fpath = os.path.join(self.app.config["FILE_PATH"], file.filename)
        file.save(fpath)

        image = cv2.imread(fpath)
        data_manager = DataManager(
            self.app.config["DATABASE_HOST"],
            self.app.config["DATABASE"],
            self.app.config["DATABASE_USER"],
            self.app.config["DATABASE_PASSWORD"]
        )
        data_manager.insert_data(fpath)
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
