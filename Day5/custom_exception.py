class InvalidAgeError(Exception):
    def __init__(self, message, age):
        super().__init__(message)
        self.age = age


try:
    age = int(input("Enter Age: "))
    if age < 0:
        raise InvalidAgeError("The age Cannot be Negative:", age)
except InvalidAgeError as e:
    print(f"Error:{e} The age Cannot be Negative:{e.age}")
