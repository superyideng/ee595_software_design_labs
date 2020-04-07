import sys
import pickle
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


# Extract 1000 data and labels from batch1
# Divide into training set and testing set
def load_CIFAR_batch(filename, N):
    """
    :param filename: str
    :param N: int, number of images
    :return: divided sets
    """

    with open(filename, 'rb') as f:
        datadict = pickle.load(f, encoding='latin1')
        data = datadict['data'][0:1000, :]
        labels = datadict['labels'][0:1000]
        training_set = data[0:N].reshape(N, 3, 1024)
        training_labels = labels[0:N]
        testing_set = data[N:].reshape(1000 - N, 3, 1024)
        testing_labels = labels[N:]

        return training_set, training_labels, testing_set, testing_labels


# Convert the RGB images into grayscale
def preprocess_image(data):
    """
    :param data: List[List[List[float]]]
    :return: List[List[float]]
    """

    X, Y, Z = np.shape(data)
    set_r = data[:, 0:1, :].reshape(X, Z)
    set_g = data[:, 1:2, :].reshape(X, Z)
    set_b = data[:, 2:3, :].reshape(X, Z)
    result = 0.299 * set_r + 0.587 * set_g + 0.114 * set_b

    return result


# Use PCA package to do PCA transformation
def PCA_transformation(D, data):
    """
    :param D: number of components of the output
    :param data: data to be transformed
    :return: transformed data
    """
    pca = PCA(n_components=D, svd_solver="full")
    traned_data = pca.transform(data)
    return traned_data


# Do KNN from sklearn package
def do_sklearn_KNN(training_data, training_label, testing_data, k):
    """
    :param k: KNN parameter
    :return: predicted labels
    """
    knn = KNeighborsClassifier(n_neighbors=k, weights='distance', p=1)
    knn.fit(training_data, training_label)
    predict_labels = knn.predict(testing_data)
    return predict_labels


# Write output into file
def write_output(file_name, predicted, true):
    """
    :param file_name: Str
    :param predicted: input predicted labels
    :param true: input true labels
    :return: void
    """
    open(file_name, 'w').close()
    cur_file = open(file_name, 'a')
    len_labels = len(predicted_labels)
    acc = 0
    for i in range(len_labels):
        if predicted[i] == true[i]:
            acc += 1
        cur_file.writelines(str(predicted[i]) + '  ' + str(true[i]))
        cur_file.write('\n')
    acc = acc / len_labels
    cur_file.writelines(str(acc))


class KNN:
    def __init__(self, k):
        """
        :param k: int, number of neighbors considered when applying KNN
        """

        self.k = k
        self.features = None
        self.labels = None

    # Save features and label to self
    def train(self, features, labels):
        """
        For KNN, the training process is just loading of training data. Thus, all we need to do in this function
        is create some local variable in KNN class to store this data so you can use the data in later process.
        :param features: List[List[float]]
        :param labels: List[int]
        """

        self.features = np.array(features)
        self.labels = np.array(labels)

    # Predict labels of a list of points
    def predict(self, features):
        """
        :param features: List[List[float]]
        :return: List[int]
        """

        predicted_labels = []
        for feature in features:
            predicted_result = self.voting_result_from_k_neighbors(feature)
            predicted_labels.append(predicted_result)

        return predicted_labels

    # Compute Manhattan distance
    def manhattan_distance(self, point1, point2):
        """
        :param point1: List[float]
        :param point2: List[float]
        :return: float, mahattan distance of point1 and point2
        """
        return np.sum(np.abs(point1 - point2))

    # Compute the voting result based on k neighbors
    def voting_result_from_k_neighbors(self, point):
        """
        :param point: List[float]
        :return: predicted label of this point
        """

        distances = []

        for i in range(len(self.features)):
            distances.append(self.manhattan_distance(point, self.features[i]))

        distances = np.array(distances)
        k_neighbors_idx = distances.argsort()[0:self.k]
        k_neighbors_dist = distances[k_neighbors_idx]
        k_neighbors_label = self.labels[k_neighbors_idx]

        max_vote = 0
        predict_label = None
        for label in np.unique(k_neighbors_label):
            cur_index = np.where(k_neighbors_label == label)
            cur_distance = k_neighbors_dist[cur_index]
            cur_metric = np.array([(1 / dist) for dist in cur_distance])
            cur_vote = np.sum(cur_metric)
            if cur_vote > max_vote:
                max_vote = cur_vote
                predict_label = label

        return predict_label


if __name__ == '__main__':
    # extract input data
    KNN_param = int(sys.argv[1])
    PCA_param = int(sys.argv[2])
    training_num = int(sys.argv[3])
    PATH_TO_DATA = sys.argv[4]

    # load CIFAR batch 1 and do preprocess
    training_set, training_labels, testing_set, testing_labels = load_CIFAR_batch(PATH_TO_DATA, training_num)
    preprocessed_train = preprocess_image(training_set)
    PCAed_train = PCA_transformation(PCA_param, preprocessed_train)

    # do KNN written by myself
    knn = KNN(KNN_param)
    knn.train(PCAed_train, training_labels)
    preprocessed_test = preprocess_image(testing_set)
    PCAed_test = PCA_transformation(PCA_param, preprocessed_test)
    predicted_labels = knn.predict(PCAed_test)
    write_output("knn_results.txt", predicted_labels, testing_labels)

    # do KNN in sklearn
    predicted_labels_from_sklearn = do_sklearn_KNN(PCAed_train, training_labels, PCAed_test, KNN_param)
    write_output("knn_results_sklearn.txt", predicted_labels_from_sklearn, testing_labels)

