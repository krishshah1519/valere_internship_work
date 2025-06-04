import logging

logging.basicConfig(
    filename="calculator.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def add(x, y):
    logging.info("Successfully!! Entered Add Function")
    print("Result: ", x+y)
    logging.info(f"The Sum of {x} and {y} is: {x + y}")


def subtract(x, y):
    logging.info("Successfully!! Entered Subtract Function")
    print("Result: ", x-y)
    logging.info(f"The Difference of {x} and {y} is: {x - y}")


def multiply(x, y):
    logging.info("Successfully!! Entered Multiply Function")
    print("Result: ", x*y)
    logging.info(f"The Product of {x} and {y} is: {x * y}")


def divide(x, y):
    logging.info("Successfully!! Entered Divide Function")
    if y == 0:
        logging.warning("Invalid input resulting in error")
        raise Exception("Error! Cannot divide by zero")
    else:
        print("Result: ", x/y)
        logging.info(f"The Remainder of {x} and {y} is: {x / y}")


logging.info("Program Starts")
print("Please Select a Operation")


inputOperator = int(input("1).Add \n2).Subtract \n3).Multiply \n4).Divide\n"))
logging.info("Operator Selected Succesfully")

if inputOperator > 4 or inputOperator == 0:
    logging.warning("Error raised due to invalid Operation Selection")
    raise Exception("Invalid Operation Selected")

inputNum1 = int(input("Enter First Number: "))
logging.info("Input Number one taken Successfully")
inputNum2 = int(input("Enter Second Number: "))
logging.info("Input Number second taken Successfully")
logging.info(f"The Number one is: {inputNum1} ,"
             f" The Number two is: {inputNum2}")

if inputOperator == 1:
    logging.info("Addition is Chosen")
    add(inputNum1, inputNum2)

if inputOperator == 2:
    logging.info("Subtraction is Chosen")
    subtract(inputNum1, inputNum2)

if inputOperator == 3:
    logging.info("Multiplication is Chosen")
    multiply(inputNum1, inputNum2)

if inputOperator == 4:
    logging.info("Divison is Chosen")
    divide(inputNum1, inputNum2)
