"""
Testing ABR Network
@Author Chanwoo Gwon, Yonsei Univ. Researcher, since 2020.05
@date 2021.02.08
"""
import tensorflow as tf
from model.core import Net, Dataset
import os
import matplotlib.pyplot as plt


class ABRNet(Net):
    """
    Main Network Class
    extend Net Class from maist model core
    reference : https://github.com/Yonsei-Maist/maist-model-core.git
    """

    def __init__(self, model_name, base_path, model_core):
        super().__init__(model_name, base_path, model_core)
        self.__curr_loss_mse = None
        self.__before_loss_mse = None

    def get_value_train_step(self, outputs, labels):
        """
        override to do something during train step
        :param outputs: output of model
        :param labels: real answer
        :return: mse result
        """
        if isinstance(outputs, list):
            predict_index = tf.math.argmax(outputs[0], 1)
        else:
            predict_index = tf.math.argmax(outputs, 1)

        if isinstance(labels, list):
            label_val = tf.math.argmax(labels[0], 1)
        else:
            label_val = tf.math.argmax(labels, 1)

        mse = tf.keras.losses.MSE(label_val, predict_index)

        return [mse]

    def vector_to_data(self, vector_list, x_limit):
        """
        change vector to data format
        :param vector_list: vector values of real data
        :param x_limit: max time step value (must same to train data)
        :return: tensor object for model
        """
        tensor_list = []
        max_value = max(vector_list[0])
        for vector in vector_list:
            change = [x / max_value for x in vector]

            tensor_list.append(change[: x_limit] if len(change) >= x_limit else change + [0 for x in range(x_limit - len(change))])

        tensor = tf.convert_to_tensor(tensor_list)

        tensor = tf.reshape(tensor, (len(tensor_list), len(tensor_list[0]), 1))

        return tensor

    def to_top_predict(self, prediction):
        """
        return predicted result for response
        :param prediction: raw data from model
        :return: formatted response
        """
        top_list = []

        index_list = tf.math.argmax(prediction, 1).numpy()
        for i in range(len(index_list)):
            index = index_list[i]
            top_list.append({
                "prediction": int(index),
                "score": float(prediction[i, index].numpy())
            })

        return top_list

    def save_when(self, epoch, result_values):
        mse = result_values[1]
        if epoch > 100:
            self.__before_loss_mse = self.__curr_loss_mse
            self.__curr_loss_mse = mse
        return self.__before_loss_mse is not None and self.__before_loss_mse > self.__curr_loss_mse

    def extract_test_all(self, index, base_path):
        self._model_core.build_model()
        self._model_core.model.load_weights(os.path.join(self._base_path,
                                                         './checkpoints/{}_{}.tf'.format(self.name, index)))

        model = self._model_core.model
        train_data = self._model_core.get_train_data()
        test_data = self._model_core.get_test_data()

        self._model_core.avg_logger.refresh()
        file = []

        csv_file_content = 'No.,Origin File Name,IsLeft,Index,IsTestData,Peak (ms),Predict (ms),Percentage (%),Real Value File Name,Predict File Name'

        def read(csv, data: Dataset, is_testdata):
            gen = list(data.get())
            gen_origin = list(data.get_origin())
            for data, origin in zip(gen, gen_origin):
                inputs = data[0]
                labels = data[1]
                outputs = model(inputs, training=False)

                for i in range(len(labels)):

                    data_one = [inputs[0][i], labels[i]]
                    origin_one = origin[i]
                    exist = None
                    for item in file:
                        if item['file'] == origin_one['origin_file'] and item['isRight'] == origin_one['isRight']:
                            exist = item
                            break
                    graph_item = {'data': data_one, 'output': outputs[i], 'max_value': origin_one['max_value'], 'is_testdata': is_testdata}
                    if exist is None:
                        file.append({'file': origin_one['origin_file'], 'out': [graph_item], 'isRight': origin_one['isRight']})
                    else:
                        exist['out'].append(graph_item)

                    predict_max_index = tf.math.argmax(outputs[i]).numpy()
                    csv = '{0}\n{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(
                        csv,
                        i + 1,
                        '/'.join(origin_one['origin_file'].split('/')[-2:]),
                        'Y' if origin_one['isRight'] is False else 'N',
                        origin_one['index'] + 1,
                        'Y' if is_testdata else 'N',
                        round(tf.math.argmax(data_one[1]).numpy() / 660 * 15, 2),
                        round(predict_max_index / 660 * 15, 2),
                        round(outputs[i][predict_max_index].numpy() * 100, 2),
                        '{0}-{1}'.format('/'.join(origin_one['origin_file'].split('/')[-2:]), 'real_value.png'),
                        '{0}-{1}'.format('/'.join(origin_one['origin_file'].split('/')[-2:]), 'predict_value.png')
                    )
            return csv

        csv_file_content = read(csv_file_content, train_data, False)
        csv_file_content = read(csv_file_content, test_data, True)

        with open(os.path.join(base_path, 'result_report.csv'), 'w') as f:
            f.write(csv_file_content)

        model.reset_states()
        # print(len(file))
        for i in range(len(file)):
            file_one = file[i]
            file_name = file_one['file']
            save_file_name_parent = os.path.join(base_path, file_name.split('/')[-2])
            if not os.path.exists(save_file_name_parent):
                os.makedirs(save_file_name_parent)
            save_file_name = '{0}-{1}'.format(file_name.split('/')[-1], 'Left' if file_one['isRight'] is False else 'Right')
            # print(save_file_name, file_one['isRight'], len(file_one['out']))
            predict = [item['output'] for item in file_one['out']]
            graph_list = [item['data'][0].numpy() for item in file_one['out']]
            max_value_list = [item['max_value'] for item in file_one['out']]
            current_peak_list = [tf.math.argmax(item['data'][1]).numpy() for item in file_one['out']]
            is_testdata_list = [item['is_testdata'] for item in file_one['out']]
            # print(current_peak_list)
            self.draw_predict(predict, graph_list, is_testdata_list, max_value_list, current_peak_list, os.path.join(save_file_name_parent, save_file_name))

    def draw_predict(self, predict, graph_list, is_testdata_list, max_value_list, current_peak_list, extract_image_path):
        length = 660
        predict_max = tf.math.argmax(predict, 1).numpy()
        predict_percentage = [round(predict[i][item].numpy() * 100, 2) for i, item in enumerate(predict_max)]
        list_all = [[item[0] for item in graph] for graph in graph_list]
        plt.figure(figsize=(8, 8))

        for i, value in enumerate(list_all):
            if is_testdata_list[i]:
                color = '#65D685'
            else:
                color = '#65C5D6'
            plt.plot(
                [i / 660 * 15 for i in range(length)],
                [item * max_value_list[i] for item in value], marker='', color=color, linewidth=2)

        plt.scatter(
            [peak_index / 660 * 15 for peak_index in current_peak_list if peak_index != 0],
            [list_all[i][current_peak_list[i]] * max_value_list[i] for i in range(len(list_all)) if
             current_peak_list[i] != 0],
            edgecolors='green', color='green', label='real')

        for i, peak in enumerate(current_peak_list):
            if peak == 0:
                continue

            plt.text(peak / 660 * 15, list_all[i][peak] * max_value_list[i] + 10,
                     "{0} ms".format(round(peak / 660 * 15, 2)),
                     fontsize=10,
                     color='blue',
                     horizontalalignment='center',
                     verticalalignment='bottom')

        plt.xlabel('peak_actual (ms)')
        plt.yticks([])
        plt.savefig('{0}-{1}'.format(extract_image_path, 'real_value.png'), dpi=300, facecolor='white')
        # plt.show()
        plt.close('all')

        plt.figure(figsize=(8, 8))

        for i, value in enumerate(list_all):

            if is_testdata_list[i]:
                color = '#65D685'
            else:
                color = '#65C5D6'
            plt.plot(
                [i / 660 * 15 for i in range(length)],
                [item * max_value_list[i] for item in value], marker='', color=color, linewidth=2)

        # print(predict_max)
        # print(max_value_list)
        plt.scatter(
            [predict_max[i] / 660 * 15 for i in range(len(list_all))],
            [list_all[i][predict_max[i]] * max_value_list[i] for i in range(len(list_all))],
            marker='x', edgecolors='red', color='red', label='predict')

        for i, peak in enumerate(predict_max):
            plt.text(peak / 660 * 15, list_all[i][peak] * max_value_list[i] + 10,
                     "{0} ms, {1} %".format(round(peak / 660 * 15, 2), predict_percentage[i]),
                     fontsize=10,
                     color='blue',
                     horizontalalignment='center',
                     verticalalignment='bottom')

        plt.xlabel('peak_predict (ms)')
        plt.yticks([])
        plt.savefig('{0}-{1}'.format(extract_image_path, 'predict_value.png'), dpi=300, facecolor='white')
        plt.close('all')
        # plt.show()

    #
    # def capture_image(self, checkpoint_index, image_path):
    #     ldl_c_d_for_graph = []
    #     data_for_graph = []
    #     avg_loss, res = self.test(checkpoint_index)
    #
    #     for i in range(len(res)):
    #         predict_index = int(tf.math.argmax(res[i]))
    #         ldl_c_d_for_graph.append(predict_index)
    #
    #     for i in range(len(self.get_test_data()[1])):
    #         data_for_graph.append(int(tf.math.argmax(self.get_test_data()[1][i])))
    #
    #     plt.figure(figsize=(8, 8))
    #     # multiple line plot
    #     plt.scatter(data_for_graph, ldl_c_d_for_graph, label="Peak", s=3)
    #
    #     # X축 이름
    #     plt.xlabel('peak_actual')
    #     # Y축 이름
    #     plt.ylabel('peak_predicted')
    #
    #     plt.legend()
    #     plt.savefig(image_path)
