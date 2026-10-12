# Linear Algebra

This repo implements linear algebra equations using Python and C++.

## Leontief Input-Output Model

`leontief-model.py` uses Python and NumPy to solve `(I - A)x = d`, where:

- `A` is the consumption matrix.
- `I` is the identity matrix.
- `x` is total demand, including the output needed by other sectors.
- `d` is final demand from consumers outside the production system.

The program accepts terminal input and displays `x` and `d` together in one
table. It warns if the consumption matrix is not square or the system has no
unique solution. Matrix and demand values must be finite and non-negative.

## Run

From this directory, install NumPy and run the program:

```bash
python -m pip install numpy
python leontief-model.py
```

Enter the number of rows, the number of columns, each matrix row, and the final
demand values. For example, enter these lines in order:

```text
2
2
0.2 0.1
0.3 0.2
70 50
```

This example gives total demand `x = [100, 100]` and displays it alongside
final demand `d = [70, 50]`. Results are rounded to two decimal places for display.
