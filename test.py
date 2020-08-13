"""
test.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import Net

net = Net("./data/Response-result-origin.txt")
for i in range(1, 7):
    avg_loss, res = net.test(i * 100)

    print(avg_loss)
