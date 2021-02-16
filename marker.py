import matplotlib.pyplot as plt
import tensorflow as tf
from imagelib.extractor import Extractor
from network.RNN import ABRNet
from network.rnn_core_case_1 import RNNCoreCase1_1
from lib.data import DataMaker
import cv2

# predict
extractor = Extractor()
data_maker = DataMaker()

core = RNNCoreCase1_1("./data/data.2021.01.11.txt", 64)
net = ABRNet("ABR", "./", core)

image = cv2.imread('/Volumes/DATACENTER/학습데이터/I111-I145/I111.png')
cropped_image = data_maker.crop(image)
vector_obj_list = extractor.extract_image_with_peak(cropped_image[0], True)
vector_list = []
length = 660
before_peak_list = [[0] * length]
current_peak_list = []

for i in range(len(vector_obj_list)):
    vector_obj = vector_obj_list[i]

    vector_list.append(vector_obj['graph'])

    if len(vector_obj['peak']) != 0:
        peak_5 = vector_obj['peak'][-1]
        current_peak_list.append(peak_5[0])
        if i < len(vector_obj_list) - 1:
            zeros = [0] * length
            zeros[peak_5[0]] = 1
            before_peak_list.append(zeros)
    elif i < len(vector_obj_list) - 1:
        before_peak_list.append([0] * length)
        current_peak_list.append(0)
    else:
        current_peak_list.append(0)

tensor = net.vector_to_data(vector_list, length)
predict = net.predict(100, [tensor, tf.convert_to_tensor(before_peak_list, dtype=tf.float32)])
predict_max = tf.math.argmax(predict, 1)
graph_list = tensor.numpy()
list_all = [[item[0] for item in graph] for graph in graph_list]

for value in list_all:
    plt.plot(list(range(length)), value, marker='', color='teal', linewidth=2, label='graph')

plt.scatter(
    [peak_index for peak_index in current_peak_list if peak_index != 0],
    [list_all[i][current_peak_list[i]] for i in range(len(list_all)) if current_peak_list[i] != 0],
    edgecolors='green', color='green', label='real')

plt.scatter(
    [predict_max[i] for i in range(len(list_all))],
    [list_all[i][predict_max[i]] for i in range(len(list_all))],
    marker='x', edgecolors='red', color='red', label='predict')

plt.legend(loc='best')
plt.tight_layout()
plt.show()
