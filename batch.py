from lib.data import DataMaker
from os import listdir
from os.path import isfile, join
import random

maker = DataMaker()

data_file = "./data/data.2021.06.14.4.txt"
"""
base_paths = [
    "/Volumes/DATACENTER/학습데이터/Infant ABR 1-50/",
    "/Volumes/DATACENTER/학습데이터/Infant ABR 51-110/",
    "/Volumes/DATACENTER/학습데이터/I111-I145/",
    "/Volumes/DATACENTER/학습데이터/ABR 추가 데이터/",
    "/Volumes/DATACENTER/학습데이터/ABR 데이터/",
    "/Volumes/DATACENTER/학습데이터/ABR데이터 2/",
    "/Volumes/DATACENTER/학습데이터/2020_12_18 ABR 이미지/",
    "/Volumes/DATACENTER/학습데이터/ABR데이터(19.01)/",
    "/Volumes/DATACENTER/학습데이터/2020_12_26/",
    "/Volumes/DATACENTER/학습데이터/2020_12_27/"
]
"""

base_paths = [
    "/Volumes/DATACENTER/학습데이터/abr/ABR파형분석/CCC/"
]

files = []

for base_path in base_paths:
    files.extend(["{}{}".format(base_path, f) for f in listdir(base_path) if isfile(join(base_path, f))])

# random.shuffle(files)

maker.batch(files, data_file, 660)
