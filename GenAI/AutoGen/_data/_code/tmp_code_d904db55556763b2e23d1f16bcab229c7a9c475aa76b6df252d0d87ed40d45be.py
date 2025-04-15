# Importing necessary library
import numpy as np
def calculate_inverse(matrix):
    # Calculating Inverse of a Matrix using NumPy's linalg.inv function which is optimized.
    inverse_matrix = np.linalg.inv(matrix)
    return inverse_matrix
# Example matrix for demonstration purposes (2x2 general case).
matrix_example=np.array([[4, 7],[3 ,6]])
inverted_result=calculate_inverse(matrix_example) # Calling the calculate_inverse() function with example data.
print('Inverse of Matrix:\n', inverted_result)