import logging

logging.basicConfig(
    filename="check_prime.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def checkPrime():
    logging.info("The Program is Running...")
    intNum = int(input("Enter the number to Check if It is Prime: "))
    logging.info("The Input Number is taken succsessfully")
    logging.info(f"The Input Number is: {intNum}")
    is_prime = True

    if intNum <= 1:
        logging.info("The Number is smaller than or equal to 1")
        is_prime = False
    for i in range(2, int(intNum ** 0.5) + 1):
        logging.info("The Program is in for loop")
        if intNum % i == 0:
            logging.info(f"The Number is Either Divisible by {i} ")
            is_prime = False
            break

    if is_prime:
        logging.info("The Number is Found to be a Prime Number")
        print("The Number is a Prime Number")
    if not is_prime:
        logging.info("The Number is Found to Be not a Prime Number")
        print("The Number is not a Prime Number")

    logging.info("The Programs Ends Here")


checkPrime()
