# Joshua Luo
# CS 325 Section 400 Spring 2021
# Homework: Portfolio Project

def checkPalindrome_1(string, k):
    return helper_1(string, k, string)


def helper_1(string, k, cur_string):
    is_palindrome = False

    # if cur_string is the correct length i.e. has 0-k letters removed
    if len(string) - k <= len(cur_string) <= len(string):
        # check if cur_string is a palindrome
        is_palindrome = is_palindrome or cur_string == cur_string[::-1]

    # base case: cur_string has length of 0, no more letters to remove (for loop will not execute)
    # recursive case: cur_string has letters to remove, test each substring with a letter removed
    for i in range(len(cur_string)):
        # make a new cur_string that removes the letter at index i
        next_string = cur_string[0:i] + cur_string[i + 1: len(cur_string)]
        next_string_is_palindrome = helper_1(string, k, next_string)
        is_palindrome = is_palindrome or next_string_is_palindrome

    return is_palindrome


def checkPalindrome_2(string, k):
    memo = {}
    helper_2(string, k, string, memo)
    return memo[string]


def helper_2(string, k, cur_string, memo):
    # exceeded k letters removed, don't need to keep removing letters
    if len(cur_string) < len(string) - k:
        return False

    # cur_string has already been processed before, use its result
    if cur_string in memo:
        return memo[cur_string]

    has_k_palindrome = False        # store if cur_string and its subsequent substrings are a k-palindrome
    if len(string) - k <= len(cur_string) <= len(string):
        # use OR for any found k-palindrome
        has_k_palindrome = cur_string == cur_string[::-1]

        # once finding any k-palindrome, just return True, don't need to keep exploring
        if has_k_palindrome:
            return True

    # explore a substring with each letter removed
    for i in range(len(cur_string)):
        # new string with the letter at index i removed
        next_string = cur_string[0:i] + cur_string[i + 1: len(cur_string)]

        # recursive call to check cur_string's substrings for a k-palindrome
        # will also not have recursive calls once a k-palindrome is found, since we just need to find 1 k-palindrome
        has_k_palindrome = has_k_palindrome or helper_2(string, k, next_string, memo)

    # store cur_string's result in memo
    memo[cur_string] = has_k_palindrome

    return has_k_palindrome
