"""
Compare DNN LDL Cholesterol MSE, The Friedelwald equation MSE
@Author Chanwoo Kwon, Yonsei Univ. Researcher. since 2020.05~
"""

from network.RNN import Net
import matplotlib.pyplot as plt
import tensorflow as tf

ldl_c_d_for_graph = []
data_for_graph = []
net = Net("./data/Response-result-origin.txt")
avg_loss, res = net.test(196)

for i in range(len(res)):
    predict_index = int(tf.math.argmax(res[i]))
    ldl_c_d_for_graph.append(predict_index)

for i in range(len(net.get_test_data()[1])):
    data_for_graph.append(int(tf.math.argmax(net.get_test_data()[1][i])))

print(ldl_c_d_for_graph)
print(data_for_graph)
plt.figure(figsize=(8, 8))
# multiple line plot
# plt.plot(range(len(net.get_test_data()[0])), data_for_graph, marker='', color='coral', linewidth=2, label="Measured Peak")
# plt.plot(range(len(net.get_test_data()[0])), ldl_c_d_for_graph, marker='', color='teal', linewidth=2, label="DNN Regression")
plt.scatter(data_for_graph, ldl_c_d_for_graph, label="Peak", s=3)

# X축 이름
plt.xlabel('peak_actual')
# Y축 이름
plt.ylabel('peak_predicted')

plt.legend()
plt.show()

