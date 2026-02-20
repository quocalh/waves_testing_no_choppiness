"""
create a program that generate unit vectors input n amount of unit vectors, 

generate that much vector input a certain angle, 
    the first waves will be around that vector angle, 
    fluctuating more widly for the latter ones put it in the a proper format, 
so i can paste in this glsl code: const array_of_dir[10] = { // vectors here }

"""
import math
import random

import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__) + "/..")

from running_program.waves import X_UNIT, X_NUM, Y_NUM, Y_UNIT


def generate_vectors(n, base_angle_deg, max_spread_deg):
    _range_2 = min(X_NUM * X_UNIT, Y_NUM * Y_UNIT)
    _range_1 = min(X_UNIT, Y_UNIT)


    base = math.radians(base_angle_deg)
    max_spread = math.radians(max_spread_deg)

    print(f"const vec2 array_of_dirs[{n}] = vec2[{n}](")

    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        spread = max_spread

        angle = base + random.uniform(-spread, spread)

        length = random.uniform(_range_1, _range_2)

        x = length * math.cos(angle)
        y = length * math.sin(angle)

        print(f"    vec2({x:.4f}, {y:.4f})" + ("," if i + 1 < n else "") )

    print(");")


# example
generate_vectors(
    n=200,
    base_angle_deg = 0,   # direction center
    max_spread_deg = 180    # how wide the last ones can go
)