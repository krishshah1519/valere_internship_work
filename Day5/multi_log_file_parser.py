import logging
import csv
import json
import os


def setup_logger(logger_name, log_name):
    logger = logging.getLogger(f"{logger_name}")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"{log_name}")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def txt_parsing():
    logger = setup_logger("txt", "txt.log")
    logger.info("Parsing started")

    lines = file.readlines()

    for line in lines:
        print(line.strip())
    logger.info("File content Displayed")

    file.close()
    logger.info("File Closed")


def csv_parsing():
    logger = setup_logger("csv", "csv.log")
    logger.info("Parsing started")

    for row in file:
        print(row)
    logger.info("File content Displayed")

    file.close()
    logger.info("File Closed")


def csv_write():
    logger = setup_logger("csv", "csv.log")
    logger.info("Writing started")

    content = input("Enter the content to write in the file: ")
    logger.info("Input Taken succesfully")

    csv.writer(file).writerow([content])
    logging.info("The content has been updated")
    print("The content has been updated")

    file.close()
    logger.info("File Closed")


def txt_write():
    logger = setup_logger("txt", "txt.log")
    logger.info("Writing started")

    content = input("Enter the content to write in the file: ")
    logger.info("Input Taken succesfully")

    file.write(f"\n{content}")
    logging.info("The content has been updated")
    print("The content have been updated")

    file.close()
    logger.info("File Closed")


file_path = input("Enter the filepath: ")
operation = int(input("Enter the Operation You want to Perfrom\n"
                      "1).Open the file\n"
                      "2)Add Content to file\n"
                      "3).Delete the file\n"
                      ))
try:
    with open(file_path, "r+") as file:

        if operation == 1:
            if file_path.endswith(".txt"):
                txt_parsing()

            if file_path.endswith(".csv"):
                csv_parsing()

            else:
                print("Other file types not supported yet!")

        if operation == 2:
            if file_path.endswith(".txt"):
                txt_write()

            if file_path.endswith(".csv"):
                csv_write()

            else:
                print("Other file types not supported yet!")

        if operation == 3:
            os.remove(file_path)

except FileNotFoundError:
    print(f"Error!!: file {file_path} not found ")
except Exception as e:
    print(f"Error: {e} for {file_path}")
