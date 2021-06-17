# Joshua Luo
# CS 325 Section 400 Spring 2021
# Homework: Portfolio Project

def patternMatch(string, p):
    m = len(string)
    n = len(p)

    # 2D m x n matrix of whether the string matches the pattern up to a number of letters
    cache = [[None for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            # note: accessing the letters require i - 1 and j - 1 because
            # 0 indicates empty string/pattern, not the first letter of string/pattern
            if i == 0 and j == 0:                       # string = '', pattern = ''
                cache[i][j] = True                          # empty strings match
            elif j == 0:                                # string = non-empty string, pattern = ''
                cache[i][j] = False                         # never matches
            elif i == 0 and p[j - 1] == "*":            # string = '', pattern[j - 1] = '*'
                cache[i][j] = cache[i][j - 1]               # True if pattern up to now is all *
            elif p[j - 1] == "?" or (string[i - 1] == p[j - 1]):    # pattern = '?' or string and pattern index values match
                cache[i][j] = cache[i - 1][j - 1]                       # depends if string and pattern without this char matched
            elif p[j - 1] == "*":                                   # pattern = '*'
                cache[i][j] = cache[i - 1][j] or cache[i][j - 1]        # * is replacing multiple or 0 letters
            else:                                                   # index values don't match
                cache[i][j] = False                                     # automatically does not match

    return cache[m][n]
