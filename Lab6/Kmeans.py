import sys
import numpy as np
import struct
import sklearn.cluster


# extract the first N images from the file and reshape each image to 1D space
def load_images(file_name, N):
    binfile = open(file_name, 'rb')
    buffers = binfile.read()
    magic, num, rows, cols = struct.unpack_from('>IIII', buffers, 0)
    bits = N * rows * cols
    imgs = struct.unpack_from('>' + str(bits) + 'B', buffers, struct.calcsize('>IIII'))
    binfile.close()
    imgs = np.reshape(imgs, [N, rows * cols])

    return imgs


# extract initial centers from file
def init_centers_from_file(file_name):
    centers = []
    infile = open(file_name, 'r')
    for cur_line in infile.readlines():
        if len(cur_line) == 0:
            continue
        cur_line = cur_line.strip()
        temp_list = cur_line.split(",")
        center = [float(i) for i in temp_list]
        centers.append(center)
    infile.close()
    return np.array(centers)


# generate initial centers randomly
def init_centers_randomly(imgs, num_ctrs):
    index = np.random.choice(imgs.shape[0], num_ctrs, replace=False)
    centers = imgs[index]
    return centers


# write the output of kmeans into file_name
def write_output(file_name, membership):
    open(file_name, 'w').close()
    cur_file = open(file_name, 'a')
    for item in membership:
        cur_file.write(str(item) + '\n')


class KMeans():
    '''
        Class KMeans:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int)
            e - error tolerance (Float)
    '''
    def __init__(self, n_cluster, max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e
        self.centers = []

    def fit(self, x, centers):

        '''
            Finds n_cluster in the data x
            params:
                x - N X D numpy array
                centroid_func - To specify which algorithm we are using to compute the centers(Lloyd(regular) or Kmeans++)
            returns:
                A tuple
                (centroids a n_cluster X D numpy array,
                 y a length (N,) numpy array where cell i is the ith sample's assigned cluster,
                 number_of_updates a Int)
            Note: Number of iterations is the number of time you update the assignment
        '''
        assert len(x.shape) == 2, "fit function takes 2-D numpy arrays as input"

        # N = # data points, D = len of every point
        N, D = x.shape

        self.centers = centers

        # - Initialize means by picking self.n_cluster from N data points
        # - Update means and membership until convergence or until you have made self.max_iter updates.
        # - return (means, membership, number_of_updates)
        Q_pre = -1
        y = np.zeros(N, dtype=int)
        num_of_updates = 0

        while num_of_updates < self.max_iter:
            norm2 = np.sum(((x - np.expand_dims(self.centers, axis=1)) ** 2), axis=2)
            y = np.argmin(norm2, axis=0)

            l = []
            for k in range(self.n_cluster):
                l.append([np.sum((x[y == k] - self.centers[k]) ** 2)])
            Q_cur = np.sum(l) / N

            num_of_updates += 1

            if (abs(Q_cur - Q_pre)) <= self.e and Q_pre >= 0:
                break

            Q_pre = Q_cur

            muk_update = np.zeros((self.n_cluster, D))
            for n_cluster in range(self.n_cluster):
                if len(x[y == n_cluster]) == 0:
                    continue
                muk_update[n_cluster] = np.sum(x[y == n_cluster], axis=0) / len(x[y == n_cluster])
            if np.isnan(muk_update).any():
                index = np.where(np.isnan(self.centers))
                muk_update[index] = self.centers[index]
            self.centers = muk_update

        # DO NOT CHANGE CODE BELOW THIS LINE
        return self.centers, y, num_of_updates


if __name__ == '__main__':
    # store the input N and flag of reading
    N = int(sys.argv[1])
    flag_of_reading = int(sys.argv[2])

    filename_train_img = 'train-images.idx3-ubyte'
    train_imgs = load_images(filename_train_img, N)

    # normalize
    normalized_train_imgs = train_imgs / 255.0

    # do kmeans
    k_means = KMeans(n_cluster=7, max_iter=100, e=1e-8)

    # generate the initial centers according to flag of reading
    if flag_of_reading == 1:
        centers = init_centers_from_file("input.txt")
    else:
        centers = init_centers_randomly(normalized_train_imgs, 7)

    centroids, membership, i = k_means.fit(normalized_train_imgs, centers)
    write_output("results.txt", membership)

    membership_skl = sklearn.cluster.KMeans(n_clusters=7, init=centers, n_init=1).fit_predict(normalized_train_imgs)
    write_output("results_sklearn.txt", membership_skl)
