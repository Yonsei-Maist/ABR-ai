"""
main.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import ABRNet
from network.rnn_core_case_1 import RNNCoreCase1_1, RNNCoreCase1

core = RNNCoreCase1_1("./data/data.2021.01.11.txt", 64)
# core = RNNCoreCase1("./data/data.2021.01.11.txt", 64)
net = ABRNet("ABR", "./", core)

net.train()
# net.test(100)
