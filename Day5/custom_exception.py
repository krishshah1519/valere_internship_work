import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="custom_exception.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InvalidAgeError(Exception):
    def __init__(self, message, age):
        super().__init__(message)
        self.age = age

logging.debug("The program stats running")

try:
    age = int(input("Enter Age: "))
    logging.info(f"Age input taken: {age}")

    if age < 0:
        logging.warning("Negative age is given as input")
        raise InvalidAgeError("The age Cannot be Negative:", age)
    else:
        print("Age taken succesfully")
        logging.debug("Program ends running")
except InvalidAgeError as e:
    logging.warning("Custom exception is raised")
    print(f"Error: {e}")
    print(f"Invalid age: {e.age}")
    logging.debug("Program ends running")
