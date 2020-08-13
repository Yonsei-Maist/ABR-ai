"""
Compare DNN LDL Cholesterol MSE, The Friedelwald equation MSE
@Author Chanwoo Kwon, Yonsei Univ. Researcher. since 2020.05~
"""

from network.RNN import Net
import matplotlib.pyplot as plt

ldl_c_d_for_graph = []
data_for_graph = []
net = Net("./data/Response-result-origin.txt")
avg_loss, res = net.test(200)

for i in range(len(res)):
    ldl_c_d_for_graph.append(res[i][0])

for i in range(len(net.get_test_data()[1])):
    data_for_graph.append(net.get_test_data()[1][i][0])

print(ldl_c_d_for_graph)
print(data_for_graph)
# multiple line plot
plt.plot(range(len(net.get_test_data()[0])), ldl_c_d_for_graph, marker='', color='teal', linewidth=2, label="DNN Regression")
plt.plot(range(len(net.get_test_data()[0])), data_for_graph, marker='', color='coral', linewidth=2, label="Measured LDL")
plt.legend()
plt.show()

