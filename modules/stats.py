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
