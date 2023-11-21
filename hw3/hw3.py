from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    # Your implementation goes here!
    x = np.load(filename)
    x = x - np.mean(x, axis=0)
    return x

def get_covariance(dataset):
    # Your implementation goes here!
    return np.dot(np.transpose(dataset), dataset) * (1/(len(dataset)-1))

def get_eig(S, m):
    # Your implementation goes here!
    n = len(S)
    w, v = eigh(S, subset_by_index=[n-m, n-1])
    w = w[::-1]
    v = v[:, ::-1]
    w = np.diag(w)
    return w, v

def get_eig_prop(S, prop):
    # Your implementation goes here!
    w = eigh(S, eigvals_only=True)
    sum = np.sum(w)
    w, v = eigh(S, subset_by_value=[prop*sum, np.inf])
    w = w[::-1]
    v = v[:, ::-1]
    w = np.diag(w)
    return w, v

def project_image(image, U):
    # Your implementation goes here!
    proj = np.matmul(np.transpose(U), image)
    proj = np.matmul(U, proj)
    return proj

def display_image(orig, proj):
    # Your implementation goes here!
    # Please use the format below to ensure grading consistency
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)
    orig = np.transpose(orig.reshape(32, 32))
    proj = np.transpose(proj.reshape(32, 32))
    pos1 = ax1.imshow(orig, aspect='equal')
    ax1.set_title("Original")
    pos2 = ax2.imshow(proj, aspect='equal')
    ax2.set_title("Projection")

    fig.colorbar(pos1, ax=ax1)
    fig.colorbar(pos2, ax=ax2)
    plt.show()
    return fig, ax1, ax2
    

def main():
    x = load_and_center_dataset('YaleB_32x32.npy')
    S = get_covariance(x)
    Lambda, U = get_eig(S, 2)
    # Lambda, U = get_eig_prop(S, 0.07)
    projection = project_image(x[0], U)
    fig, ax1, ax2 = display_image(x[0], projection)
if __name__ == "__main__":
    main()