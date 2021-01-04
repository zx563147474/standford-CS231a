import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.misc import imread
from scipy.spatial.distance import cdist


'''
KMEANS_SEGMENTATION: Image segmentation using kmeans 
Arguments:
    im - the image being segmented, given as a (H, W, 3) ndarray

    features - ndarray of size (#pixels, M) that are the feature vectors 
        associated with each pixel. The #pixels are arranged in such a way
        that calling reshape((H,W)) will correspond to the image im.

    num_clusters - The parameter "K" in K-means that tells the number of 
        clusters we will be using.

Returns:
    pixel_clusters - H by W matrix where each index tells what cluster the
        pixel belongs to. The clusters must range from 0 to N-1, where N is
        the total number of clusters.

The K-means algorithm can be done in the following steps:
(1) Randomly choose the initial centroids from the features
(2) Repeat until convergence:
    - Assign each feature vector to its nearest centroid
    - Compute the new centroids as the average of all features assigned to it
    - Convergence happens when the centroids do not change
'''
def kmeans_segmentation(im, features, num_clusters):
    # initialize some parameters
    pixel_num = features.shape[0]
    centeroid_indices = np.random.randint(pixel_num, size=num_clusters)
    # randomly choose the initial centroids
    current_centeroids = features[centeroid_indices]

    # repeat until convergence
    while True:
        # find the distances of one pixel relative to all centeroids
        dist = np.zeros((pixel_num, num_clusters))
        for i in xrange(num_clusters):
            dist[:, i] = np.linalg.norm(features - current_centeroids[i, :], axis=1)

        # find the nearest cluster
        nearest_clusters = np.argmin(dist, axis=1)
        # update centeroids
        prev_centeroids = current_centeroids
        for i in xrange(num_clusters):
            pixel_index = np.where(nearest_clusters == i)
            cluster_features = features[pixel_index]
            current_centeroids[i, :] = np.mean(cluster_features, axis=0)

        # break when converged
        if np.array_equal(current_centeroids, prev_centeroids):
            break

    pixel_clusters = np.reshape(nearest_clusters, (im.shape[0], im.shape[1]))
    return pixel_clusters


'''
MEANSHIFT_SEGMENTATION: Image segmentation using meanshift
Arguments:
    im - the image being segmented, given as a (H, W, 3) ndarray

    features - ndarray of size (#pixels, M) that are the feature vectors 
        associated with each pixel. The #pixels are arranged in such a way
        that calling reshape((H,W)) will correspond to the image im.

    bandwidth - A parameter that determines the radius of what participates
       in the mean computation

Returns:
    pixel_clusters - H by W matrix where each index tells what cluster the
        pixel belongs to. The clusters must range from 0 to N-1, where N is
        the total number of clusters.

The meanshift algorithm can be done in the following steps:
(1) Keep track of an array whether we have seen each pixel or not.
Initialize it such that we haven't seen any.
(2) While there are still pixels we haven't seen do the following:
    - Pick a random pixel we haven't seen
    - Until convergence (mean is within 1 of the bandwidth of the old
        mean), mean shift. The output of this step will be a mean vector.
        For each iteration of the meanshift, if another pixel is within the
        bandwidth circle (in feature space), then that pixel should also be
        marked as seen
    - If the output mean vector from the mean shift step is
        sufficiently close (within half a bandwidth) to another cluster
        center, say it's part of that cluster
    - If it's not sufficiently close to any other cluster center, make
        a new cluster
(3) After finding all clusters, assign every pixel to the nearest cluster
in feature space.

To perform mean shift:
    - Once a random pixel has been selected, pretend it is the current mean
        vector.
    - Find the feature vectors of the other pixels that are within the
        bandwidth distance from the mean feature vector according to EUCLIDEAN
        distance (in feature space).
    - Compute the mean feature vector among all feature vectors within the
        bandwidth.
    - Repeat until convergence, using the newly computed mean feature vector
        as the current mean feature vector.
'''
def meanshift_segmentation(im, features, bandwidth):
    # initialize some parameters
    H, W = im.shape[0], im.shape[1]
    pixel_num, M = features.shape
    mask = np.ones(pixel_num)
    clusters = []

    while np.sum(mask) > 0:
        loc = np.argwhere(mask > 0)
        idx = loc[int(np.random.choice(loc.shape[0], 1)[0])][0]
        mask[idx] = 0

        current_mean = features[idx]
        prev_mean = current_mean

        while True:
            dist = np.linalg.norm(features - prev_mean, axis=1)
            incircle = dist < bandwidth
            mask[incircle] = 0
            # update current_mean
            current_mean = np.mean(features[incircle], axis=0)
            if np.linalg.norm(current_mean - prev_mean) < 0.01 * bandwidth:
                break
            prev_mean = current_mean

        isValid = True
        for cluster in clusters:
            if np.linalg.norm(cluster - current_mean) < 0.5 * bandwidth:
                isValid = False
        if isValid:
            clusters.append(current_mean)

    pixel_clusters = np.zeros((H, W))
    clusters = np.array(clusters)
    for i in range(pixel_num):
        idx = np.argmin(np.linalg.norm(features[i, :] - clusters, axis=1))
        pixel_clusters[i / W, i % W] = idx
    return pixel_clusters.astype(int)


def draw_clusters_on_image(im, pixel_clusters):
    num_clusters = int(pixel_clusters.max()) + 1
    average_color = np.zeros((num_clusters, 3))
    cluster_count = np.zeros(num_clusters)

    for i in xrange(im.shape[0]):
        for j in xrange(im.shape[1]):
            c = pixel_clusters[i,j]
            cluster_count[c] += 1
            average_color[c, :] += im[i, j, :]

    for c in xrange(num_clusters):
        average_color[c,:] /= float(cluster_count[c])
        
    out_im = np.zeros_like(im)
    for i in xrange(im.shape[0]):
        for j in xrange(im.shape[1]):
            c = pixel_clusters[i,j]
            out_im[i,j,:] = average_color[c,:]

    return out_im


if __name__ == '__main__':
    
    # Change these parameters to see the effects of K-means and Meanshift
    num_clusters = [5, 10, 15, 20]
    bandwidths = [0.3]


    for filename in ['lake', 'rocks', 'plates']:
        img = imread('data/%s.jpeg' % filename) 

        # Create the feature vector for the images
        features = np.zeros((img.shape[0] * img.shape[1], 5))
        for row in xrange(img.shape[0]):
            for col in xrange(img.shape[1]):
                features[row*img.shape[1] + col, :] = np.array([row, col, 
                    img[row, col, 0], img[row, col, 1], img[row, col, 2]])
        features_normalized = features / features.max(axis = 0)

        # Part I: Segmentation using K-Means
        for nc in num_clusters:
            clustered_pixels = kmeans_segmentation(img, features_normalized, nc)
            cluster_im = draw_clusters_on_image(img, clustered_pixels)
            plt.imshow(cluster_im)
            plt.title('K-means with %d clusters on %s.jpeg' % (int(nc), filename))
            plt.show()


        # Part II: Segmentation using Meanshift
        for bandwidth in bandwidths:
            clustered_pixels = meanshift_segmentation(img, features_normalized, bandwidth)
            cluster_im = draw_clusters_on_image(img, clustered_pixels)
            plt.imshow(cluster_im)
            plt.title('Meanshift with bandwidth %.2f on %s.jpeg' % (bandwidth, filename))
            plt.show()
