"""Calculate total demand with the Leontief model: x = A @ x + d."""

import numpy as np


def read_vector(prompt, size):
    """Read the required number of non-negative values from one input line."""
    while True:
        try:
            values = np.array([float(value) for value in input(prompt).split()])
        except ValueError:
            print("Warning: Enter numbers separated by spaces.")
            continue

        if values.size != size:
            print(f"Warning: Enter exactly {size} values.")
        elif not np.all(np.isfinite(values)):
            print("Warning: Values must be finite numbers; nan and inf are not allowed.")
        elif np.any(values < 0):
            print("Warning: Consumption and final demand cannot be negative.")
        else:
            return values


def main():
    print("Leontief Input-Output Model")
    print("x = A @ x + d, so (I - A) @ x = d")

    try:
        rows = int(input("Number of rows in consumption matrix A: "))
        columns = int(input("Number of columns in consumption matrix A: "))
    except ValueError:
        print("Warning: Matrix dimensions must be positive whole numbers.")
        return

    if rows <= 0 or columns <= 0:
        print("Warning: Matrix dimensions must be positive whole numbers.")
        return

    if rows != columns:
        print(f"Warning: The consumption matrix is not square ({rows} x {columns}).")
        print("It must have the same number of rows and columns.")
        return

    print("\nEnter each row of A, separating its values with spaces.")
    print("A[i, j] is the input from sector i needed for one unit of sector j's output.")
    A = np.array([read_vector(f"Row {i + 1}: ", columns) for i in range(rows)])
    d = read_vector(f"\nEnter {rows} final-demand values (d): ", rows)

    # I is the identity matrix. Solve (I - A)x = d for total demand x.
    I = np.eye(rows)
    try:
        x = np.linalg.solve(I - A, d)
    except np.linalg.LinAlgError:
        print("Warning: I - A is singular, so the model has no unique solution.")
        return

    if not np.all(np.isfinite(x)):
        print("Warning: The calculation produced non-finite values. Check the inputs.")
        return

    if np.any(x < 0):
        print("Warning: The calculated total demand includes negative values.")
        print("Check the consumption coefficients; negative output is not feasible.")

    header = f"{'Sector':<8} | {'x (total demand)':>18} | {'d (final demand)':>18}"
    print("\n" + header)
    print("-" * len(header))
    for i in range(rows):
        print(f"{i + 1:<8} | {x[i]:>18.2f} | {d[i]:>18.2f}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
