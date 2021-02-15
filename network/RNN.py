"""
Testing ABR Network
@Author Chanwoo Gwon, Yonsei Univ. Researcher, since 2020.05
@date 2021.02.08
"""
import tensorflow as tf
from model.core import Net


class ABRNet(Net):
    """
    Main Network Class
    extend Net Class from maist model core
    reference : https://github.com/Yonsei-Maist/maist-model-core.git
    """

    def get_value_train_step(self, outputs, labels):
        """
        override to do something during train step
        :param outputs: output of model
        :param labels: real answer
        :return: mse result
        """
        predict_index = tf.math.argmax(outputs, 1)

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
        for vector in vector_list:
            max_value = max(vector)
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
