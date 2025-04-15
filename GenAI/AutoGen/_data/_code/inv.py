import numpy as np

# Create or read in your 2D matrix (example)
matrix = np.array([[3, -4], [1, 5]])

try:
    # Calculate the inverse using numpy.linalg.inv()
    inv_matrix = np.linalg.inv(matrix)
    
    print("Original Matrix:")
    print(matrix)
    print("\nInverse of the Matrix:")
    print(inv_matrix)

except np.linalg.LinAlgError as e:
    print(f"Matrix inversion failed: {e}")