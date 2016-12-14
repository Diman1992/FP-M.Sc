# coding=utf-8

from numpy import sum, sqrt

# Implementierung einer Funktion für lineare Regression
# Parameter: 2 Arrays (zu fittende x- und y- Werte)

def linregress(x, y):
    # x und y müssen gleich lang sein
    assert(len(x) == len(y))

    # Formeln aus "An Introduction to Error Analysis" (Taylor)
    N = len(y)
    Delta = N * sum(x**2) - (sum(x))**2

    A = (N * sum(x * y) - sum(x) * sum(y)) / Delta
    B = (sum(x**2) * sum(y) - sum(x) * sum(x * y)) / Delta

    sigma_y = sqrt(sum((y - A * x - B)**2) / (N - 2))

    A_error = sigma_y * sqrt(N / Delta)
    B_error = sigma_y * sqrt(sum(x**2) / Delta)

    # f(x) = A * x + B
    return (A, A_error, B, B_error)
