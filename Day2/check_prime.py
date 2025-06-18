import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="check_prime.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def checkPrime(intNum):
    logger.info("The Program is Running...")

    logger.info("The Input Number is taken successfully")
    logger.info(f"The Input Number is: {intNum}")
    is_prime = True

    if intNum <= 1:
        logger.info("The Number is smaller than or equal to 1")
        print('The number is not a prime number')
        return False

    for i in range(2, int(intNum ** 0.5) + 1):
        logger.info("The Program is in for loop")
        if intNum % i == 0:
            logger.info(f"The Number is Either Divisible by {i} ")
            is_prime = False
            break

    if is_prime:
        logger.info("The Number is Found to be a Prime Number")
        print("The Number is a Prime Number")
        logger.info("The Programs Ends Here")
        return True

    if not is_prime:
        logger.info("The Number is Found to Be not a Prime Number")
        print("The Number is not a Prime Number")
        logger.info("The Programs Ends Here")
        return False
    return None


intNum = int(input("Enter the number to Check if It is Prime: "))
checkPrime(intNum)
