import logging
import os
import csv

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="file_parser.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger.info("The Parser has Started Running")
file_path = input("Enter The file path: ")
logger.info(f"file path taken {file_path}")

operation = int(input("Enter the Operation You want to Perfrom\n"
                      "1).Open the file\n"
                      "2)Add Content to file\n"
                      "3).Delete the file\n"
                      ))
logger.info(f"Operation is taken {operation}")

if operation == 1:
    logger.info("successfully entered operation 1")
    try:
        with open(f"{file_path}", "r") as file:
            logger.info("Found the file")

            if file_path.endswith(".txt"):
                logger.info("The file is text document")

                lines = file.readlines()
                logger.info("Reading the text file")

                for line in lines:
                    print(line.strip())

                logger.info("Printed the file data")
                file.close()
                logger.info("File closed")

            if file_path.endswith(".csv"):
                logger.info("This is a csv file")

                for row in file:
                    print(row)

                logger.info("Printed the file Data")
                file.close()
                logger.info("File closed")

    except FileNotFoundError:
        print(f"Error!!: file {file_path} not found ")
        logger.error("File Not Found Error")

    except Exception as e:
        print(f"Error!!: Cannot open the file {file_path} due to {e}")
        logger.error(f"ERROR: {e} ")

if operation == 2:
    logger.info("successfully entered operation 2")
    try:
        with open(f"{file_path}", "a+") as file:
            if file_path.endswith(".txt"):
                logger.info("The file is text document")
                content = input("Enter the content to write in the file: ")

                logger.info("The input is taken successfully")
                file.write(f"\n{content}")
                print("The content have been updated")
                file.close()

            if file_path.endswith(".csv"):
                print("This is a csv file ")
                content = input("Enter the content to write in the file: ")

                csv.writer(file).writerow([content])
                print("The content has been updated")
            else:
                print("Other file types not supported yet!")

    except FileNotFoundError:
        print(f"Error!!: file {file_path} not found ")
        logger.error("File Not Found Error")

    except Exception as e:
        print(f"Error!!: Cannot append the file {file_path} due to {e}")
        logger.error(f"ERROR: {e} ")
if operation == 3:
    try:
        os.remove(file_path)

    except FileNotFoundError:
        print(f"Error: file {file_path} not found ")

    except OSError as e:
        print(f"Error: Unable to delete file- {file_path} due to {e}")
