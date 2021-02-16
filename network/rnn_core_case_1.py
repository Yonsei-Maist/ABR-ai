"""
Testing Main Core
@Author Chanwoo Gwon, Yonsei Univ. Researcher, since 2020.05
@date 2021.02.08
"""

from model.core import ModelCore
from model.core import LOSS

import tensorflow as tf


class RNNCoreCase1(ModelCore):
    """
    Main Core of ABR Network
    The case No.1
    reference : https://yonsei-my.sharepoint.com/:p:/g/personal/arknell_o365_yonsei_ac_kr/EQcNAgdMCYtOu5Be_P7rLL4B7T8HtQRmVYdtAiMfp5l5yg?e=kNfFNb
    (page 1)
    """
    def __init__(self, data_path, batch_size=64):
        self._time_step = None
        super().__init__(data_path, batch_size=batch_size, avg_list=['loss', 'mse'], loss=LOSS.COSINE_SIMILARITY)

    def read_data(self):
        """
        override read_data
        """
        data_all = [[], [], []]
        with open(self._data_path) as f:
            lines = f.readlines()

            for i in range(len(lines)):
                line = lines[i]
                data_split = line.split('\t')

                if len(data_split) < 5:
                    continue

                index = int(data_split[1])
                # if index == 0:  # first graph only (2020.09.10)
                # use all of graph
                if index >= 0:
                    graph = data_split[2].split(',')
                    peak = data_split[3].split(',')

                    if len(peak) == 0 or self.check_integer_string(peak[-1]) == -1:
                        continue

                    data_vector = []
                    for j in range(len(graph)):
                        data_vector.append([float(graph[j])])

                    vector = data_vector
                    answer = int(peak[-1])

                    if answer < len(vector):
                        data_all[0].append(data_vector)
                        max_value = max(data_vector)
                        new_list = []
                        for j in range(len(data_vector)):
                            new_list.append([data_vector[j][0] / max_value[0]])  # normalization

                        data_all[2].append(new_list)

                        zeros = [0] * len(data_vector)
                        zeros[answer] = 1
                        data_all[1].append(zeros)

            sp = int(len(data_all[0]) * 0.8)
            print("train data : ", sp)
            print("test data : ", len(data_all[0]) - sp)

            self._train_data.set([tf.convert_to_tensor(data_all[2][:sp], dtype=tf.float32)],
                                 [tf.convert_to_tensor(data_all[1][:sp], dtype=tf.float32)])
            self._test_data.set([tf.convert_to_tensor(data_all[2][sp:], dtype=tf.float32)],
                                [tf.convert_to_tensor(data_all[1][sp:], dtype=tf.float32)])

        self._time_step = len(data_all[2][0])

    def build_model(self):
        """
        build model
        1. Input
        2. Bidirectional RNN(LSTM CELL)
        3. TimeDistributed
        4. Flatten
        5. Dense
        6. Dense (Output, softmax)
        """
        input_layer = tf.keras.layers.Input([self._time_step, 1])

        output = tf.keras.layers.Bidirectional(layer=tf.keras.layers.LSTM(128, return_sequences=True))(input_layer)
        # output = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(32))(output)
        output = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(1))(output)
        output = tf.keras.layers.Flatten()(output)
        # output = tf.keras.layers.Dense(time_step)(output)
        output = tf.keras.layers.Dense(self._time_step)(output)
        # output = tf.keras.layers.Dropout(0.3)(output)
        output = tf.keras.layers.Dense(self._time_step, activation=tf.keras.activations.softmax)(output)
        # output = tf.keras.activations.softmax(output)
        self.model = tf.keras.Model(inputs=[input_layer], outputs=[output])

    def get_time_step(self):
        """
        return time step of this Network's RNN
        :return:
        """
        return self._time_step


class RNNCoreCase1_1(RNNCoreCase1):
    """
    Main Core of ABR Network
    The case No.1
    reference : https://yonsei-my.sharepoint.com/:p:/g/personal/arknell_o365_yonsei_ac_kr/EQcNAgdMCYtOu5Be_P7rLL4B7T8HtQRmVYdtAiMfp5l5yg?e=kNfFNb
    (page 2)
    """
    def read_data(self):
        """
        override read_data
        """
        data_all = [[], [], []]
        with open(self._data_path) as f:
            lines = f.readlines()
            max_value = 0
            for i in range(len(lines)):
                line = lines[i]
                data_split = line.split('\t')

                if len(data_split) < 5:
                    continue

                index = int(data_split[1])
                # if index == 0:  # first graph only (2020.09.10)
                if index >= 0:
                    graph = data_split[2].split(',')
                    peak = data_split[3].split(',')
                    before_peak = data_split[4].split(',')

                    if len(peak) == 0 or self.check_integer_string(peak[-1]) == -1:
                        continue

                    data_vector = []
                    zero_count = 0
                    for j in range(len(graph)):
                        value_one = float(graph[j])
                        if value_one == 0.0:
                            zero_count += 1
                        data_vector.append([value_one])

                    if zero_count > 2:
                        continue

                    vector = data_vector
                    answer = int(peak[-1])

                    if answer < len(vector):
                        data_all[0].append(data_vector)

                        if index == 0:
                            zeros = [0] * len(data_vector)
                            max_value = max(data_vector)
                        elif len(before_peak) > 0 and self.check_integer_string(before_peak[-1]) > -1:
                            before_index = int(before_peak[-1])
                            zeros[before_index] = 1
                        else:
                            continue

                        new_list = []
                        for j in range(len(data_vector)):
                            new_list.append([data_vector[j][0] / max_value[0]])  # normalization

                        data_all[2].append([new_list, zeros])

                        zeros = [0] * len(data_vector)
                        zeros[answer] = 1
                        data_all[1].append(zeros)

        sp = int(len(data_all[0]) * 0.8)

        self._train_data.set([
            tf.convert_to_tensor([item[0] for item in data_all[2][:sp]], dtype=tf.float32),
            tf.convert_to_tensor([item[1] for item in data_all[2][:sp]], dtype=tf.float32)
        ], [tf.convert_to_tensor(data_all[1][:sp], dtype=tf.float32)])

        self._test_data.set([
            tf.convert_to_tensor([item[0] for item in data_all[2][sp:]], dtype=tf.float32),
            tf.convert_to_tensor([item[1] for item in data_all[2][sp:]], dtype=tf.float32)
        ], [tf.convert_to_tensor(data_all[1][sp:], dtype=tf.float32)])

        print("train data : ", len(self._train_data))
        print("test data : ", len(self._test_data))

        self._time_step = len(data_all[2][0][0])

    def build_model(self):
        """
        build model
        1. Input1, Input2
        2. Bidirectional RNN(LSTM CELL), Dense
        3. TimeDistributed, Reshape
        4. Concatenate
        5. Dense
        6. Dense (Output, softmax)
        """
        input_layer_1 = tf.keras.layers.Input([self._time_step, 1])
        input_layer_2 = tf.keras.layers.Input([self._time_step])

        output_1 = tf.keras.layers.Bidirectional(layer=tf.keras.layers.LSTM(128, return_sequences=True))(input_layer_1)

        output_1 = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(1))(output_1)

        output_2 = tf.keras.layers.Dense(self._time_step)(input_layer_2)

        output_2 = tf.keras.layers.Reshape([self._time_step, 1])(output_2)

        output = tf.keras.layers.Concatenate(axis=2)([output_1, output_2])

        output = tf.keras.layers.Dense(1)(output)
        output = tf.keras.layers.Flatten()(output)

        output = tf.keras.layers.Dense(self._time_step, activation=tf.keras.activations.softmax)(output)

        self.model = tf.keras.Model(inputs=[input_layer_1, input_layer_2], outputs=[output])

