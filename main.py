"""
main.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import Net

net = Net("./data/Response-result-origin.txt")
net.train()
