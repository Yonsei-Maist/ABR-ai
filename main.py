"""
main.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import ABRNet
from network.rnn_core_case_1 import RNNCoreCase1_1, RNNCoreCase1, RNNCoreCase1_1_1

core = RNNCoreCase1_1("./data/data.2021.04.15.txt", 64)
# core = RNNCoreCase1_1_1("./data/data.2021.04.15.txt", 64)
# core = RNNCoreCase1("./data/data.2021.01.11.txt", 64)
net = ABRNet("ABR", "./", core)

net.extract_test_all(139, './data/result.2021.04/', ["75L", "60L", "50L", "40L", "30L", "20L", "10L"])
# print(net.test(139))
# net.train()
# net.test(100)
