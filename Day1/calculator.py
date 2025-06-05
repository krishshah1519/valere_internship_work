import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="calculator.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def add(x, y):
    logger.info("Successfully!! Entered Add Function")
    print("Result: ", x+y)
    logging.info(f"The Sum of {x} and {y} is: {x + y}")


def subtract(x, y):
    logger.info("Successfully!! Entered Subtract Function")
    print("Result: ", x-y)
    logger.info(f"The Difference of {x} and {y} is: {x - y}")


def multiply(x, y):
    logger.info("Successfully!! Entered Multiply Function")
    print("Result: ", x*y)
    logger.info(f"The Product of {x} and {y} is: {x * y}")


def divide(x, y):
    logger.info("Successfully!! Entered Divide Function")
    try:
        print("Result: ", x/y)
        logger.info(f"The Remainder of {x} and {y} is: {x / y}")
    except ZeroDivisionError:
        print("Cannot Divide a digit with 0")
        logger.warning("The user tried to divided a number by Zero ")


while True:
    logger.info("Program Starts")
    print("Please Select a Operation")

    inputOperator = int(input("1).Add \n2).Subtract \n3).Multiply \n4).Divide "
                              "\n5).Exit Program \n"))
    logger.info("Operator Selected Succesfully")

    try:
        if inputOperator > 5 or inputOperator == 0:
            logger.error("Error raised due to invalid Operation Selection")
            raise Exception("Invalid Operation Selected")

        if inputOperator == 5:
            logger.info("User Wants to Quit the Program")
            print("The Program is Ending")
            break

        else:
            inputNum1 = int(input("Enter First Number: "))
            logger.info("Input Number one taken Successfully")
            inputNum2 = int(input("Enter Second Number: "))
            logger.info("Input Number second taken Successfully")
            logger.info(f"The Number one is: {inputNum1} ,"
                        f" The Number two is: {inputNum2}")

    except Exception as E:
        print("Invalid Operation selected")

    if inputOperator == 1:
        logger.info("Addition is Chosen")
        add(inputNum1, inputNum2)

    if inputOperator == 2:
        logger.info("Subtraction is Chosen")
        subtract(inputNum1, inputNum2)

    if inputOperator == 3:
        logger.info("Multiplication is Chosen")
        multiply(inputNum1, inputNum2)

    if inputOperator == 4:
        logger.info("Divison is Chosen")
        divide(inputNum1, inputNum2)
