from lib.data import DataMaker

maker = DataMaker()

data_file = "./data/data.2021.01.11.txt"
maker.batch("/Volumes/DATACENTER/학습데이터/Infant ABR 1-50/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/Infant ABR 51-110/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/I111-I145/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/ABR 추가 데이터/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/ABR 데이터/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/ABR데이터 2/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/2020_12_18 ABR 이미지/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/ABR데이터(19.01)/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/2020_12_26/", data_file, 660)
maker.batch("/Volumes/DATACENTER/학습데이터/2020_12_27/", data_file, 660)
