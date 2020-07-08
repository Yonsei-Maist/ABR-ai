"""
main.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

import tensorflow as tf
import matplotlib.pyplot as plt

# read data
data_all = [[], []]
with open("./data/Response-result-origin.txt") as f:
    lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]
        data_split = line.split(',')
        data_vector = []
        for j in range(1, len(data_split) - 2):
            data_vector.append(int(data_split[j]))

        vector = data_vector
        answer = int(data_split[len(data_split) - 2][2:])

        if answer < len(vector):
            data_all[0].append(data_vector)
            data_all[1].append(answer)

    sp = int(len(data_all[0]) * 0.8)
    train_data = [data_all[0][:sp], data_all[1][:sp]]
    test_data = [data_all[0][sp:], data_all[1][sp:]]

print(train_data)
print(test_data)

input_layer = tf.keras.layers.InputLayer([495])



