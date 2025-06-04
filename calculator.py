def add(x, y):
    print("Result: ", x+y)


def subtract(x, y):
    print("Result: ", x-y)


def multiply(x, y):
    print("Result: ", x*y)


def divide(x, y):
    if y == 0:
        raise Exception("Error! Cannot divide by zero")
    else:
        print("Result: ", x/y)


print("Please Select a Operation")


inputOperator = int(input("1).Add \n2).Subtract \n3).Multiply \n4).Divide\n"))


if inputOperator == 1:
    add(inputNum1, inputNum2)
if inputOperator == 2:
    subtract(inputNum1, inputNum2)
if inputOperator == 3:
    multiply(inputNum1, inputNum2)
if inputOperator == 4:
    divide(inputNum1, inputNum2)
else:
    raise Exception("Invalid Operation Selected")
inputNum1 = int(input("Enter First Number: "))
inputNum2 = int(input("Enter Second Number: "))
