# Joshua Luo
# CS 325 Section 400 Spring 2021
# Homework: Portfolio Project

def getTesla(M):
    m = len(M)
    n = len(M)

    min_energy_map = [[None for x in range(n)] for x in range(m)]
    min_energy_map[m - 1][n - 1] = M[m - 1][n - 1]      # initialize cost of the last space

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # starting space doesn't have above and left spaces
            if i != 0 or j != 0:
                # calculate total cost from above of current space
                if i - 1 >= 0:  # valid space above
                    cost_above = min_energy_map[i][j] + M[i - 1][j]
                    if cost_above > 0:
                        cost_above = 0
                    min_energy_map[i - 1][j] = cost_above

                # calculate total cost from left of current space
                if j - 1 >= 0:  # valid space to the left
                    cost_left = min_energy_map[i][j] + M[i][j - 1]
                    if cost_left > 0:
                        cost_left = 0

                    if i < m - 1:
                        # when not on the bottom row, the left space will have a min energy value from being the top
                        # of a space in the row below, and we will keep the max value between the two
                        min_energy_map[i][j - 1] = max(cost_left, min_energy_map[i][j - 1])
                    else:
                        min_energy_map[i][j - 1] = cost_left

    return abs(min_energy_map[0][0]) + 1
