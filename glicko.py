"""Implementation of Glicko Rating System.

This module is an implementation of the Glicko-1 rating system as specified in
http://www.glicko.net/glicko/glicko.pdf.
"""

import math

def rating_deviation(RD, c, t):
    """Calculates a ratings deviation based on when the last previous ratings deviation"""
    return min([(RD ** 2 + (c ** 2) * t) ** 0.5, 350])

def g(RD):
    """g function used in calculation"""
    q = math.log(10) / 400
    return 1 / (1 + (3 * (q ** 2) * (RD ** 2) / (math.pi) ** 2)) ** 0.5

def E(r0, ri, RD):
    """Conditional expectation used in calculation"""
    return 1 / (1 + 10**(- g(RD) * (r0 - ri) / 400))

def d_squared(r_old, RDs_opp, rs_opp):
    """d squared value used in new_rating and new ratings_deviation calculations"""

    q = math.log(10) / 400
    total = 0
    assert len(RDs_opp) == len(rs_opp)
    for i, _ in enumerate(RDs_opp):
        g_temp = g(RDs_opp[i]) ** 2
        E_temp = E(r_old, rs_opp[i], RDs_opp[i])
        total += g_temp * E_temp * (1 - E_temp)
    return (q ** 2 * total) ** -1

def new_rating(r_old, RD, RDs_opp, rs_opp, results):
    """Calculates a new rating based on results"""
    q = math.log(10) / 400

    total = 0
    assert len(RDs_opp) == len(rs_opp)
    assert len(RDs_opp) == len(results)
    for i, _ in enumerate(RDs_opp):
        total += g(RDs_opp[i]) * (results[i] - E(r_old, rs_opp[i], RDs_opp[i]))

    product = q / ((1 / RD ** 2) + (1 / d_squared(r_old, RDs_opp, rs_opp)))

    return r_old + product * total

def new_RD(r_old, RD_old, rs_opp, RDs_opp):
    """Calculates an updated ratings deviation based on results"""
    d2_temp = d_squared(r_old, RDs_opp, rs_opp)
    return (((1 / RD_old ** 2) + (1 / d2_temp)) ** -1) ** 0.5
