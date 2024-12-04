def euclids_algo(num1, num2):
    """Finds the GCD between two numbers"""
    while num1 != 0 and num2 != 0:
        num1, num2 = max(num1, num2), min(num1, num2)
        num1 = num1 - num2
        print(num1, num2)
    return max(num1, num2)
