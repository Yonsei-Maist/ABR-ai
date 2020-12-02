from lib.data import DataMaker

maker = DataMaker()

# maker.batch("/Users/gwonchan-u/Downloads/Infant ABR 1-50/", "./data/train.txt", 660)
# maker.batch("/Users/gwonchan-u/Downloads/Infant ABR 51-110/", "./data/train2.txt", 660)
# maker.batch("/Users/gwonchan-u/Downloads/I111-I145/", "./data/train3.txt", 660)
maker.batch("/Users/gwonchan-u/Downloads/ABR 추가 데이터/", "./data/train4.txt", 660)
