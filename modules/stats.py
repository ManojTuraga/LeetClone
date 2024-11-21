'''
Module: stats.py
Creation Date: November 15th, 2024
Author: Ceres Botkin
Contributors: Ceres Botkin

Description:
    This module is used to generate code statistics from runs from the dre.
    The code takes in an execution time table and returns several code
    statistics including total runtime, average runtime, and approx
    time complexity. 

Inputs:
    n_table: list of integer input vectors 
    time_table: list of execution time

Outputs:
    total_t: Total time complexity
    average_t: Average time complexity
    approx_t_complexity: Approx. time complexity as a string

Preconditions:
    None

Postconditions:
    None

Error Conditions:
    None

Side Effects:
    None

Invariants:
    None

Known Faults
    None
'''
import time
import numpy as np

# Represents percent of total coefficients a degree needs to be seen as
# effectivley non-zero
# Set at 10% from experimentation but feel free to change if you wish
COMPLEXITY_THRESHOLD = 0.1

# Class which represents code statistics generated from a time table
class CodeStatistics:
    def __init__(self, n_table, time_table):
        # Initialize variables
        self.n_table = n_table
        self.time_table = time_table

        # Generate statistics
        self.generate_statistics()

    # Generate statistics
    def generate_statistics(self):
        self.calc_total_runtime()
        self.calc_average_runtime()
        self.calc_approx_t_complex()

    # Calculate total runtime
    def calc_total_runtime(self):
        self.total_runtime = sum(self.time_table)

    # Calculate average runtime
    def calc_average_runtime(self):
        self.average_runtime = sum(self.time_table) / len(self.time_table)

    # Calculate approx. time complexity
    def calc_approx_t_complex(self):
        # Generate a 5th degree polynomial fit to see what is the most significant
        # leading coefficient
        poly_deg = np.polyfit(self.n_table, self.time_table, 5)

        # Normalize coefficients
        poly_deg = np.array(list(map(abs, poly_deg)))
        poly_deg = poly_deg / sum(poly_deg)

        # If the 5th degree is the most significant, say the time complexity
        # is essentially exponential (technically true as long as the program
        # isn't like factorial time due to the fact that O is an upper bound)
        if (poly_deg[0] > COMPLEXITY_THRESHOLD):
            self.approx_t_complex = "O(e ** n)"
            return

        # Check each degree larger than 0
        for i in range(len(poly_deg[:-1])):
            degree = len(poly_deg) - i - 1
            coeff = poly_deg[i]

            if (coeff > COMPLEXITY_THRESHOLD):
                self.approx_t_complex = f'O(n ** {degree})'
                return

        # If no coefficients pass the threshold, we can basically assume
        # the code is basically constant time. Aka the constant term is so
        # much bigger than the variable term we can basically ignore the
        # variable term
        self.approx_t_complex = 'O(1)'

    # Print results
    # Only for debugging purposes
    def print_statistics(self):
        print(f'Total Execution Time: {self.total_runtime}')
        print(f'Average Execution Time: {self.average_runtime}')
        print(f'Approximate Time Complexity: {self.approx_t_complex}')
