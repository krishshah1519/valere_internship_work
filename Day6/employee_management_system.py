
class Employee:

    emp_id = 1

    def __init__(
            self,
            emp_id,
            name,
            age,
            gender,
            position,
            salary,
            phone_number):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.gender = gender
        self.position = position
        self.salary = salary
        self.phone_number = phone_number

    def display(self):
        print("-------------------------------")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Position: {self.position}")
        print(f"Salary: {self.salary}")
        print(f"Phone Number: {self.phone_number}")
        print("-------------------------------")


def add_employee():
    name = input('Enter employee full name: ')
    age = input('Enter employee age: ')
    gender = input('Enter employee gender (M or F) :')
    position = input('Enter employee position: ')
    salary = input('Enter the salary: ')
    phone_number = input('Enter employee number: ')

    emp_id = Employee.emp_id
    name = Employee(emp_id, name, age, gender, position, salary, phone_number)
    Employee_Management.employee.append(name)


class Employee_Management():
    def __init__(self):
        pass
    employee = []

    def display_employee(self):
        if not self.employee:
            print('No employee data found')
            return

        for emp in self.employee:
            emp.display()

    def find(self, name):
        for emp in self.employee:
            if emp.name.lower() == name.lower():
                emp.display()
                return
            else:
                print('Employee not found')

    def remove(self, name):
        for emp in self.employee:
            if emp.name.lower() == name.lower():
                self.employee.remove(emp)
                print(f"Employee {name} removed successfully.")
                return
            else:
                print('Employee not found')

    def update(self, name):
        for emp in self.employee:
            if emp.name.lower() == name.lower():
                age = input('Enter age(leave blank to skip): ')
                salary = input('Enter salary(leave blank to skip): ')
                position = input('Enter position(leave blank to skip): ')
                phone_number = input(
                    'Enter phone number(leave blank to skip): ')

                if age is not None:
                    emp.age = age
                if salary is not None:
                    emp.salary = salary
                if position is not None:
                    emp.position = position
                if phone_number is not None:
                    emp.phone_number = phone_number

    def clear(self):
        self.employee.clear()

    def run(self):
        while True:
            print("\nEmployee Management System\n"
                  "1. Add Employee\n"
                  "2. Display Employees\n"
                  "3. Find Employee\n"
                  "4. Remove Employee\n"
                  "5. Update Employee\n"
                  "6. Clear All Employees\n"
                  "7. Exit")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_employee()
            elif choice == 2:
                self.display_employee()
            elif choice == 3:
                name = input('Enter full name to search')
                self.find(name)
            elif choice == 4:
                name = input('Enter full name to search')
                self.remove(name)
            elif choice == 5:
                name = input('Enter full name to search')
                self.update(name)
            elif choice == 6:
                self.clear()
            elif choice == 7:
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    ems = Employee_Management()
    ems.run()
