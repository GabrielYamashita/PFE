
import numpy as np

# Define the weights, individual variances, and covariance matrix
w = np.array([1, 2, 3, 4])  # Replace with your weights
variances = np.array([2, 3, 4, 5])  # Replace with individual variances
covariance_matrix = np.array(
    [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6],
        [4, 5, 6, 7]
    ]
)  # Replace with covariance matrix

# Create the diagonal matrix of individual variances
D = np.diag(variances)

# Calculate the portfolio variance using the matricial equation
portfolio_variance = np.dot(w, np.dot(D, w)) + np.dot(w, np.dot(covariance_matrix, w))

print(portfolio_variance)