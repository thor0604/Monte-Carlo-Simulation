#! /usr/bin/env python3
"""
A program to estimate the value of pi using the Monte-Carlo method
"""
import sys
import math
import random

def in_circle(point):
    """return True if point is in circle"""
    return math.sqrt(point[0] ** 2 + point[1] ** 2) <= 1


def generate_random_point():
    """return a random point in square with specific size"""
    abscisse = random.uniform(-1, 1)
    ordonnee = random.uniform(-1, 1)
    return (abscisse, ordonnee)

def approx_pi(repeat):
    """approximate the value of pi"""
    compteur = 0
    for _ in range(repeat):
        rpoint = generate_random_point()
        if in_circle(rpoint):
            compteur += 1
    return 4 * compteur / repeat


def main():
    """
    returns the approximaated value of pi takes in an integer as argument
    """
    if len(sys.argv) != 2:
        raise IndexError("Please add an integer as second argument")
    try:
        repeat = int(sys.argv[1])
    except ValueError:
        raise ValueError("Please add an integer as second argument") from None
    valeur_pi = approx_pi(repeat)
    print(valeur_pi)

if __name__ == '__main__':
    main()
