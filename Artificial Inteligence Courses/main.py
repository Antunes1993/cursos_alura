#%%
#Doing a web search to get the possible math criterias for check if a triangle is non-degenerated
# 1. Check the colinearity of the points
#    1.1. If area of triangle is zero, the triangle is degenerated.
# 2. Check the determinant of coordinates of the points
# 3. Check if the sum of the sides is greater than the third side
# 4. Check if the difference of the sides is less than the third side


#%%
#First Solution:  Making combinations of 3 points and getting the determinant of the coordinates.
#Time complexity: O(n^3)
from itertools import combinations
non_degenerated_triangles = 0
points = [(0, 0), (1, 1), (2, 2), (0, 1), (1, 0)]

def first_solution(points, non_degenerated_triangles):
    n = len(points)    
    if n < 3:
        return 0

    for p1, p2, p3 in combinations(points,3):
        #Getting the determinant of the points coordinates
        if(p2[0] - p1[0]) * (p3[1] - p1[1]) != (p3[0] - p1[0]) * (p2[1] - p1[1]):
            non_degenerated_triangles += 1 
    return non_degenerated_triangles


result = first_solution(points, non_degenerated_triangles)
print(result)

#%%
#Second Solution: For each point, I considered it as the reference point and get the slope of other points.
#Then created a dictionary with the slope as key and the number of points with the same slope as values.
#For least, I get the number of degenerated triangles calculating the combinations of 3 points with the same slope
# and reduced it from the number of possible triangles.
#Time complexity: O(n^2 logn)
import math
from itertools import combinations

import math
from itertools import combinations

def second_solution(points):
    total_triangles = len(list(combinations(points, 3)))  # Total possible triangles
    collinear_count = 0  # Counter for collinear triangles
    n = len(points)        
    if n < 3:
        return 0
    
    # A set to store unique collinear groups to avoid duplicate counting
    unique_groups = set()

    for i, p0 in enumerate(points):
        slope_dict = {}

        for j, p1 in enumerate(points):
            if i == j:
                continue  # Skip the same point

            # Slope calculation
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]

            if dx == 0:  # Vertical line
                slope = ('inf', 1)
            elif dy == 0:  # Horizontal line
                slope = (0, 1)
            else:
                g = math.gcd(dx, dy)
                slope = (dx // g, dy // g)
            
            # Normalize slope direction to ensure consistency
            if slope[1] < 0:
                slope = (-slope[0], -slope[1])

            # Add the point to the slope dictionary
            if slope not in slope_dict:
                slope_dict[slope] = []
            slope_dict[slope].append(p1)

        # Count collinear triangles for the current reference point
        for slope, group in slope_dict.items():
            k = len(group) + 1  # Include the reference point (p0)
            if k >= 3:
                # Create a unique identifier for the collinear group
                group_set = frozenset(group + [p0])
                if group_set not in unique_groups:
                    unique_groups.add(group_set)
                    collinear_count += (k - 1) * (k - 2) // 2  # Count pairs of points collinear with p0

    # Subtract collinear triangles from total to get non-degenerate triangles
    return total_triangles - collinear_count, total_triangles


# Test case
points = [(0, 0), (1, 1), (2, 2), (0, 1), (1, 0)]
print(second_solution(points))




#%%
#Third Solution: For each point, I considered it as the reference point and calculated the slope of other points.
#Than created a default_dictionary (hash table) with the slope as key and the number of points with the same slope as values.
#Additionally, a set is used to ensure each collinear group of points is only counted once, avoiding duplicates.

#For each slope group, I calculated the combinations of 3 collinear points to count degenerate triangles.
#Finally, the number of degenerate triangles was subtracted from the total possible triangles to get the non-degenerate ones.
#Time complexity: O(n^2)

from math import gcd
from collections import defaultdict

def third_solution(points):
    n = len(points)    
    if n < 3:
        return 0

    total_triangles = n * (n - 1) * (n - 2) // 6  # Total number of combinations of 3 points
    collinear_count = 0  # Count of degenerate (collinear) triangles

    # Set to track unique collinear groups
    unique_groups = set()

    # Step 1: For each point, calculate the slopes with every other point
    for i, p0 in enumerate(points):
        slope_dict = defaultdict(list)  # Dictionary to store points with the same slope

        for j, p1 in enumerate(points):
            if i == j:
                continue  # Skip the same point

            # Calculate slope between p0 and p1
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]

            # Normalize the slope
            if dx == 0:  # Vertical line
                slope = ('inf', 1)
            elif dy == 0:  # Horizontal line
                slope = (0, 1)
            else:
                g = gcd(dx, dy)
                slope = (dx // g, dy // g)

            # Normalize slope direction to ensure consistency
            if slope[1] < 0:
                slope = (-slope[0], -slope[1])

            # Add the point to the slope dictionary
            slope_dict[slope].append(p1)

        # Step 2: Count degenerate triangles for each slope group
        for slope, group in slope_dict.items():
            group_set = frozenset(group + [p0])  # Include the reference point in the group
            if group_set not in unique_groups:
                unique_groups.add(group_set)
                k = len(group) + 1  # Include the reference point (p0)
                if k >= 3:
                    collinear_count += (k - 1) * (k - 2) // 2  # Count pairs of collinear points

    # Step 3: Subtract degenerate triangles from the total
    non_degenerate_triangles = total_triangles - collinear_count
    return non_degenerate_triangles, total_triangles

points = [(0, 0), (1, 1), (2, 2), (0, 1), (1, 0)]
print(third_solution(points))