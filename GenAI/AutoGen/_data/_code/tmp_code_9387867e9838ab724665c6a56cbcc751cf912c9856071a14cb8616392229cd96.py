
import numpy as np

# Define the example 2D matrix
# Make sure the matrix is square and non-singular (invertible)
example_matrix = np.array([[1, 2],
                           [3, 4]])

print(f"Original Matrix:\n{example_matrix}")

try:
    # Calculate the inverse using numpy's linalg.inv function
    inverse_matrix = np.linalg.inv(example_matrix)
    print(f"\nInverse Matrix:\n{inverse_matrix}")

    # Optional: Verification step
    # Multiplying a matrix by its inverse should result in the identity matrix
    identity_check = np.dot(example_matrix, inverse_matrix)
    print(f"\nVerification (Original * Inverse):\n{identity_check}")
    # Check if the result is close to the identity matrix (within floating point tolerance)
    is_identity = np.allclose(identity_check, np.eye(example_matrix.shape[0]))
    print(f"\nIs the verification result close to the identity matrix? {is_identity}")

except np.linalg.LinAlgError as e:
    print(f"\nError: {e}. The matrix is likely singular and cannot be inverted.")

