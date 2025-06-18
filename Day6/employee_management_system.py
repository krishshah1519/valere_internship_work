from openpyxl.styles.builtins import output


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
        expected = ("-------------------------------\n"
                    f"Employee ID: {self.emp_id}\n"
                    f"Name: {self.name}\n"
                    f"Age: {self.age}\n"
                    f"Gender: {self.gender}\n"
                    f"Position: {self.position}\n"
                    f"Salary: {self.salary}\n"
                    f"Phone Number: {self.phone_number}\n"
                    "-------------------------------\n")

        return print(expected)


class EmployeeManagement():
    def __init__(self):
        self.employee = []

    def add_employee(self):

        fields = [
            'name',
            'age',
            'gender',
            'position',
            'salary',
            'phone_number']
        inp = []
        for i in fields:

            value = input(f"Enter the {i}: ")
            while value == '':
                print(f"Please!!! enter the {i}")
                value = input(f"Enter the {i}: ")
            inp.append(value)
        emp_id = Employee.emp_id

        name = Employee(
            int(emp_id), inp[0], int(
                inp[1]), inp[2], inp[3], int(
                inp[4]), int(
                inp[5]))
        self.employee.append(name)
        Employee.emp_id += 1
        print(f"employee {inp[0]} created successfully ")

    def display_employee(self):
        if not self.employee:
            print('No employee data found')
            return 'No employee data found'
        print(len(self.employee))
        for emp in self.employee:
            emp.display()

        return None

    def find(self, name):
        for emp in self.employee:
            if emp.name.lower() == name.lower():
                return emp.display()
        print('No employee data found')
        return 'No employee data found'

    def remove(self, name):
        for emp in self.employee:
            if emp.name.lower() == name.lower():
                self.employee.remove(emp)
                print(f"Employee {name} removed successfully.")
                return
        print('No employee data found')
        return 'No employee data found'

    def update(self, name):
        for emp in self.employee:
            if emp.name.lower() == name.lower():
                age = input('Enter age(leave blank to skip): ')
                gender = input('Enter gender(leave blank to skip): ')
                salary = input('Enter salary(leave blank to skip): ')
                position = input('Enter position(leave blank to skip): ')
                phone_number = input(
                    'Enter phone number(leave blank to skip): ')

                if age != '':
                    emp.age = age
                if gender != '':
                    emp.gender = gender
                if salary != '':
                    emp.salary = int(salary)
                if position != '':
                    emp.position = position
                if phone_number != '':
                    emp.phone_number = int(phone_number)
            return print(f'Employee {emp.name} data Updated\n', emp.display())
        return print('Employee not found')

    def clear(self):
        self.employee.clear()
        if len(self.employee) == 0:
            return print('All Data cleared')
        return print("Failed to clear all employees records")

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
                self.add_employee()
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
    ems = EmployeeManagement()
    ems.run()
