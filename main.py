"""
main.py
@Author Chanwoo Kwon, Yonsei Univ. researcher since 2020.05~
"""

from network.RNN import ABRNet
from network.rnn_core_case_1 import ABRRegression, RNNCoreCase1_1_1

core = ABRRegression("./data/data_predict.txt", 64)
# core = RNNCoreCase1_1_1("./data/data.2021.04.15.txt", 64)

net = ABRNet("ABR", "./", core)

net.extract_test_all(139, './data/result.2021.06/', ["75", "60", "50", "40", "30", "20", "10"])
# print(net.test(139))
# net.train()
# net.test(100)
