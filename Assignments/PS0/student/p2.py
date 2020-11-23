# CS231A Homework 0, Problem 2
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt


def main():
    # ===== Problem 2a =====
    # Define Matrix M and Vectors a,b,c in Python with NumPy

    M, a, b, c = None, None, None, None

    # BEGIN YOUR CODE HERE
    M = np.array([[1,2,3], [4,5,6], [7,8,9], [0,2,2]])
    a = np.array([1,1,0])
    b = np.array([-1,2,5])
    c = np.array([0,2,3,2])
    # END YOUR CODE HERE

    # ===== Problem 2b =====
    # Find the dot product of vectors a and b, save the value to aDotb

    aDotb = None

    # BEGIN YOUR CODE HERE
    aDotb = a.dot(b)
    print "(b) aDotb =", aDotb
    # END YOUR CODE HERE

    # ===== Problem 2c =====
    # Find the element-wise product of a and b

    # BEGIN YOUR CODE HERE
    aMultib = np.multiply(a, b)
    print "(c) aMultib =", aMultib
    # END YOUR CODE HERE

    # ===== Problem 2d =====
    # Find (a^T b)Ma

    # BEGIN YOUR CODE HERE
    dResult = aDotb * M.dot(a)
    print "(d) (a^T b)Ma =", dResult
    # END YOUR CODE HERE

    # ===== Problem 2e =====
    # Without using a loop, multiply each row of M element-wise by a.
    # Hint: The function repmat() may come in handy.

    newM = None

    # BEGIN YOUR CODE HERE
    a_repmat = np.matlib.repmat(a, 4, 1)
    newM = np.multiply(M, a_repmat)

    # with broadcasting, we can simply calculate: newM = np.multiply(M, a)
    print "(e) result =\n", newM
    # END YOUR CODE HERE

    # ===== Problem 2f =====
    # Without using a loop, sort all of the values 
    # of M in increasing order and plot them.
    # Note we want you to use newM from e.

    # BEGIN YOUR CODE HERE
    sortedM = np.sort(newM, axis=None)
    N = len(sortedM)
    x = range(N)

    # plot settings
    plt.xlabel("Vector Index")
    plt.ylabel("Values")
    plt.title("Plot of Values in Sorted M")
    plt.plot(x, sortedM, 'ro--')
    plt.axis([0, N, np.min(sortedM), np.max(sortedM)])
    plt.show()
    # END YOUR CODE HERE


if __name__ == '__main__':
    main()
