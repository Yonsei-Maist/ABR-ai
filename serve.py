"""
@Author Chanwoo Kwon, Yonsei Univ. Researcher since 2020.05~
"""
from flask import Flask, jsonify, request
from network.RNN import Net
from imagelib.extractor import Extractor
from Crypto.Cipher import AES
from config import configure

import os

app = Flask(__name__)

net = Net('./data/Response-result-origin.txt')
extractor = Extractor()
version = "0.1"
key = "maistabr"
iv = "initvector"


@app.route("/")
def hello():
    return "Hello World"


@app.route("/abr/image/save", methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        try:
            fpath = os.path.join(configure["file_path"], file.filename)
            file.save(fpath)
            encrypt = AES.new(key, AES.MODE_CBC, iv)

            return jsonify({
                "id": id,
                "version": version,
                "result": "success",
                "data": {
                    "imagepath": encrypt.encrypt(fpath)
                }
            })
        except Exception as e:
            return jsonify({
                "id": id,
                "version": version,
                "result": "fail",
                "message": e
            })
    else:
        return jsonify({
            "id": id,
            "version": version,
            "result": "fail",
            "message": "No file"
        })


@app.route("/abr/ai/predict", methods=['POST'])
def predict():
    value = request.get_json()
    id = value["id"]
    image_path = value["imagepath"]
    decrypt = AES.new(key, AES.MODE_CBC, iv)
    real_path = decrypt.decrypt(image_path)
    try:
        vector, end_of_x, img_mat = extractor.extract(real_path, True)
        predict = net.predict(200, vector)

        return jsonify({
            "id": id,
            "version": version,
            "result": "success",
            "data": {
                "graph": vector,
                "peak": [
                    {
                        "prediction": predict,
                        "score": -1
                    }
                ]
            }
        })
    except Exception as e:
        return jsonify({
            "id": id,
            "version": version,
            "result": "fail",
            "message": e
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=configure["port"])
