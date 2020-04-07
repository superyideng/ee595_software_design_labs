import numpy as np
from matplotlib import pyplot as plt


def cost_func(w, X, y):
    """
    Compute the mean absolute error on test set given X, y, and model parameter w.
    Inputs:
    - X: A numpy array of shape (num_samples, D) containing test feature.
    - y: A numpy array of shape (num_samples, ) containing test label
    - w: a numpy array of shape (D, )
    Returns:
    - err: the mean absolute error
    """
    y_pred = np.dot(X, w)
    err = np.sum(np.square(y_pred - y)) / (2 * len(y))

    return err


def linear_regression_noreg(X, y):
    """
    Compute the weight parameter given X and y.
    Inputs:
    - X: A numpy array of shape (num_samples, D) containing feature.
    - y: A numpy array of shape (num_samples, ) containing label
    Returns:
    - w: a numpy array of shape (D, )
    """
    X_trans = X.transpose()
    inverse = np.linalg.inv(np.dot(X_trans, X))
    w = inverse.dot(X_trans).dot(y)
    return w


# visualize the output
def plot_mat(w, X, X_orig, y):
    y_pred = np.dot(X, w)
    plt.scatter(X_orig, y, color='b')
    plt.plot(X_orig, y_pred, color='r')
    plt.xlabel('population * 10,000')
    plt.ylabel('profit * 10,000')
    plt.show()


if __name__ == '__main__':
    f = open('candyshop_data.txt', 'r')
    X = list()
    X_orig = list()
    y = list()
    for line in f.readlines():
        line = line.strip()
        X.append(list([1, float(line.split(',')[0])]))
        X_orig.append(float(line.split(',')[0]))
        y.append(float(line.split(',')[1]))

    w = linear_regression_noreg(np.array(X), np.array(y))

    plot_mat(w, X, X_orig, y)
