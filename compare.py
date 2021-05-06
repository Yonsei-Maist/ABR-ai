"""
Compare DNN LDL Cholesterol MSE, The Friedelwald equation MSE
@Author Chanwoo Kwon, Yonsei Univ. Researcher. since 2020.05~
"""

from network.RNN import ABRNet
from network.rnn_core_case_1 import ABRRegression
import matplotlib.pyplot as plt
import tensorflow as tf

ldl_c_d_for_graph = []
data_for_graph = []

core = ABRRegression("./data/data.2021.01.11.txt", 64)
net = ABRNet("ABR", "./", core)
avg_loss, res = net.test(100)

for i in range(len(res)):
    predict_index = int(tf.math.argmax(res[i]))
    ldl_c_d_for_graph.append(predict_index)

for i in range(len(net.get_test_data()[1])):
    data_for_graph.append(int(tf.math.argmax(net.get_test_data()[1][i])))

print(ldl_c_d_for_graph)
print(data_for_graph)
plt.figure(figsize=(8, 8))
# multiple line plot
plt.scatter(data_for_graph, ldl_c_d_for_graph, label="Peak", s=3)

# X축 이름
plt.xlabel('peak_actual')
# Y축 이름
plt.ylabel('peak_predicted')

plt.legend()
plt.show()

