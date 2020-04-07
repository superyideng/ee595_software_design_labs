import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import accuracy_score
import time


# Extract features and labels from given file
# Divide into training set and testing set
def load_dataset(filename):
    """
    :param filename: str
    :return: divided sets
    """

    lines = []
    f = open(filename, 'r')
    for line in f.readlines():
        lines.append(line)

    np.random.shuffle(lines)

    features = []
    labels = []

    for line in lines:
        arr = line.strip().split()
        cur_feature = [float(curr) for curr in arr[:len(arr) - 1]]
        features.append(cur_feature)
        labels.append(int(arr[-1]))

    ttsize = len(lines)
    training_fts = np.array(features[:int(0.8 * ttsize)])
    training_lbs = np.array(labels[:int(0.8 * ttsize)])
    testing_fts = np.array(features[int(0.8 * ttsize):])
    testing_lbs = np.array(labels[int(0.8 * ttsize):])

    return training_fts, training_lbs, testing_fts, testing_lbs


# do Gaussian Naive Bayes using sklearn
def do_sklearn_GNB(train_ft, train_lb, test_ft, test_lb):
    """
    :param train_ft: training features
    :param train_lb: training labels
    :param test_ft: testing features
    :param test_lb: testing labels
    :return: predicted labels, accuracy, and runtime
    """
    gnb = GaussianNB()

    start1 = time.time()
    gnb.fit(train_ft, train_lb)
    end1 = time.time()
    train_time = str(end1 - start1)

    pred_train_lbs = gnb.predict(train_ft)
    train_acc = accuracy_score(training_labels, pred_train_lbs)

    start2 = time.time()
    pred_test_lbs = gnb.predict(test_ft)
    test_acc = accuracy_score(test_lb, pred_test_lbs)
    end2 = time.time()
    test_time = str(end2 - start2)
    return pred_test_lbs, train_acc, test_acc, train_time, test_time


# do SVM using sklearn
def do_sklearn_SVM(train_ft, train_lb, test_ft, test_lb):
    """
    :param train_ft: training features
    :param train_lb: training labels
    :param test_ft: testing features
    :param test_lb: testing labels
    :return: predicted labels, accuracy, and runtime
    """
    clf = svm.SVC()

    start1 = time.time()
    clf.fit(train_ft, train_lb)
    end1 = time.time()
    train_time = str(end1 - start1)

    pred_train_lbs = clf.predict(train_ft)
    train_acc = accuracy_score(training_labels, pred_train_lbs)

    start2 = time.time()
    pred_test_lbs = clf.predict(test_ft)
    test_acc = accuracy_score(test_lb, pred_test_lbs)
    end2 = time.time()
    test_time = str(end2 - start2)
    return pred_test_lbs, train_acc, test_acc, train_time, test_time


class myGNB:
    def __init__(self):
        self.features = None
        self.labels = None
        self.mean = [0, 0, 0]
        self.variance = [0, 0, 0]
        self.label_pos = [0, 0, 0]

    # Compute model parameters and store to self
    def train(self, features, labels):
        """
        :param features: training features
        :param labels: training labels
        :return: training runtime
        """
        start = time.time()
        self.features = np.array(features)
        self.labels = np.array(labels)
        for label in np.unique(labels):
            cur_index = np.where(labels == label)
            cur_mean = np.sum(features[cur_index], axis=0) / len(cur_index[0])
            cur_variance = np.sum(np.square(features[cur_index] - cur_mean)) / (len(cur_index[0]))
            self.mean[label - 1] = cur_mean
            self.variance[label - 1] = cur_variance
            self.label_pos[label - 1] = len(cur_index[0]) / len(features)
        end = time.time()
        runtime = str(end - start)
        return runtime

    # Compute predicted labels using current model
    def predict(self, features, labels):
        """
        :param features: testing features
        :param labels: true testing labels
        :return: predicted labels, accuracy and runtime
        """
        start = time.time()
        predicted_labels = []
        predict_acc = 0
        for i in range(len(features)):
            probabilities = [np.log(self.conditional_gaussian(features[i], l + 1)) + np.log(self.label_pos[l])
                             for l in range(3)]
            cur_label = np.argmax(probabilities) + 1
            predicted_labels.append(cur_label)
            if cur_label == labels[i]:
                predict_acc += 1
        predict_acc /= len(features)
        end = time.time()
        runtime = str(end - start)
        return predicted_labels, predict_acc, runtime

    # Compute conditional probability of each feature
    def conditional_gaussian(self, feature, label):
        """
        :param feature: feature to be predicted
        :param label: conditional label
        :return: gaussian value
        """
        mean = self.mean[label - 1]
        variance = self.variance[label - 1]
        if variance == 0:
            return 1
        coefficient = 1 / np.sqrt(2 * np.pi * variance)
        expo = np.exp(-np.square(feature - mean) / variance)
        gaussion_matrix = coefficient * expo
        return np.sum(gaussion_matrix)


if __name__ == '__main__':
    # load data
    training_features, training_labels, testing_features, testing_labels = load_dataset("seeds_dataset.txt")

    # do gaussian naive bayes built by myself
    print("My Naive Bayes:")
    my_gnb = myGNB()
    my_gnb.train(training_features, training_labels)
    pred_train_lb, pred_train_acc, train_runtime = my_gnb.predict(training_features, training_labels)
    print("Training acc: %0.2f%%  Training time: %s s" % (pred_train_acc * 100, train_runtime))
    pred_test_lb, pred_test_acc, test_runtime = my_gnb.predict(testing_features, testing_labels)
    print("Testing acc: %0.2f%%  Testing time: %s s" % (pred_test_acc * 100, test_runtime))

    # do gaussian naive bayes in sklearn
    print("Sklearn Naive Bayes:")
    sk_pred_test_lb, sk_train_acc, sk_test_acc, sk_train_time, sk_test_time = \
        do_sklearn_GNB(training_features, training_labels, testing_features, testing_labels)
    print("Training acc: %0.2f%%  Training time: %s s" % (sk_train_acc * 100, sk_train_time))
    print("Testing acc: %0.2f%%  Testing time: %s s" % (sk_test_acc * 100, sk_test_time))

    # do SVM in sklearn
    print("Sklearn SVM:")
    svm_pred_test_lb, svm_train_acc, svm_test_acc, svm_train_time, svm_test_time = \
        do_sklearn_SVM(training_features, training_labels, testing_features, testing_labels)
    print("Training acc: %0.2f%%  Training time: %s s" % (svm_train_acc * 100, svm_train_time))
    print("Testing acc: %0.2f%%  Testing time: %s s" % (svm_test_acc * 100, svm_test_time))










