"""
main.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import Net

net = Net("./data/data.2021.01.11.txt")
net.train()
