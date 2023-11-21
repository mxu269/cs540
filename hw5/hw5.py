import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_X(df):
    num_row = df.shape[0]
    start_year = df.iloc[0, 0]
    X = np.zeros((num_row, 2), dtype="int64")
    X[:, 0] = 1
    X[:, 1] = np.arange(start_year, start_year+num_row)
    return X;

def get_Y(df):
    return df["days"].to_numpy(dtype="int64")

def get_Z(X):
    return np.matmul(np.transpose(X), X)

def get_I(Z):
    return np.linalg.inv(Z)

def get_PI(I, X):
    return np.matmul(I, np.transpose(X))

def get_beta_hat(PI, Y):
    return np.matmul(PI, Y)

def main():
    df = pd.read_csv(sys.argv[1])
    plt.figure(figsize=(10, 5))
    plt.plot(df['year'], df['days'], linestyle='-')
    plt.xlabel('Year')
    plt.ylabel('Number of Frozen Days')
    plt.savefig("plot.jpg")

    print("Q3a:")
    X = get_X(df)
    print(X)

    print("Q3b:")
    Y = get_Y(df)
    print(Y) 

    print("Q3c:")
    Z = get_Z(X)
    print(Z)

    print("Q3d:")
    I = get_I(Z)
    print(I)

    print("Q3e:")
    PI = get_PI(I, X)
    print(PI)

    print("Q3f:")
    beta_hat = get_beta_hat(PI, Y)
    print(beta_hat)

    x_test = np.array([1, 2022])
    y_test = np.matmul(np.transpose(x_test), beta_hat)
    print("Q4: " + str(y_test))

    print("Q5a: <")
    print("Q5b: As years progress, the number of frozen lake days is decreasing")

    
    # Beta [ 4.83665815e+02 -1.96965793e-01]
    prediction = beta_hat[0] / -(beta_hat[1])
    print("Q6a: " + str(prediction))
    print("Q6b: Not likely, because the relationship is probably not linear, so you can't extrapolate that far into the future. There might exist an asymptote.")

if __name__ == "__main__":
    main()
