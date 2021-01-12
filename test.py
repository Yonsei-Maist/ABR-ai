"""
test.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import Net

net = Net("./data/data.2021.01.11.txt")
for i in range(1, 1000):

    try:
        avg_loss, res = net.test(i)

        print(i, avg_loss)
    except:
        pass