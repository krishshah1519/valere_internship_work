import logging

logging.basicConfig(
    filename="calculator.log",
    level=logging.DEBUG,
    format="%{asctime}s - %{levelname} - %{message}s"
)

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
    inputNum1 = int(input("Enter First Number: "))
    inputNum2 = int(input("Enter Second Number: "))
    add(inputNum1, inputNum2)
if inputOperator == 2:
    inputNum1 = int(input("Enter First Number: "))
    inputNum2 = int(input("Enter Second Number: "))
    subtract(inputNum1, inputNum2)
if inputOperator == 3:
    inputNum1 = int(input("Enter First Number: "))
    inputNum2 = int(input("Enter Second Number: "))
    multiply(inputNum1, inputNum2)
if inputOperator == 4:
    inputNum1 = int(input("Enter First Number: "))
    inputNum2 = int(input("Enter Second Number: "))
    divide(inputNum1, inputNum2)
if inputOperator > 4:
    raise Exception("Invalid Operation Selected")


