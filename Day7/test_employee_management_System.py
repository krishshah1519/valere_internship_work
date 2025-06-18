import unittest
from Day6.employee_management_system import EmployeeManagement, Employee
from mock import patch


class TestEmployeeManagement(unittest.TestCase):
    def dis(self, emp):
        expected_outcome = ("-------------------------------\n"
                            f"Employee ID: {emp.emp_id}\n"
                            f"Name: {emp.name}\n"
                            f"Age: {emp.age}\n"
                            f"Gender: {emp.gender}\n"
                            f"Position: {emp.position}\n"
                            f"Salary: {emp.salary}\n"
                            f"Phone Number: {emp.phone_number}\n"
                            "-------------------------------\n")
        self.assertEqual(emp.display(), expected_outcome)

    def test_init(self):
        emp = Employee(
            Employee.emp_id,
            'Krish',
            20,
            'M',
            'Intern',
            0,
            9301671789)
        self.assertEqual(emp.emp_id, 1)
        self.assertEqual(emp.name, 'Krish')
        self.assertEqual(emp.age, 20)
        self.assertEqual(emp.gender, 'M')
        self.assertEqual(emp.position, 'Intern')
        self.assertEqual(emp.salary, 0)
        self.assertEqual(emp.phone_number, 9301671789)

    def test_display(self):
        emp = Employee(
            Employee.emp_id,
            'Krish',
            20,
            'M',
            'Intern',
            0,
            9301671789)

        self.dis(emp)

        emp = Employee('', 'Krish', 20, 'M', 'Intern', 0, 9301671789)

        self.dis(emp)

        emp = Employee(Employee.emp_id, '', 20, 'M', 'Intern', 0, 9301671789)

        self.dis(emp)

        emp = Employee(
            Employee.emp_id,
            'Krish',
            '',
            'M',
            'Intern',
            0,
            9301671789)

        self.dis(emp)

        emp = Employee(
            Employee.emp_id,
            'Krish',
            20,
            '',
            'Intern',
            0,
            9301671789)

        self.dis(emp)

        emp = Employee(Employee.emp_id, 'Krish', 20, 'M', '', 0, 9301671789)

        self.dis(emp)

        emp = Employee(
            Employee.emp_id,
            'Krish',
            20,
            'M',
            'Intern',
            '',
            9301671789)

        self.dis(emp)

        emp = Employee(Employee.emp_id, 'Krish', 20, 'M', 'Intern', 0, '')

        self.dis(emp)

        emp = Employee('', '', None, '', '', None, None)
        self.dis(emp)

    def test_find(self):
        emp = Employee(
            Employee.emp_id,
            'Krish',
            20,
            'M',
            'Intern',
            0,
            9301671789)
        EmployeeManagement().employee.append(emp)
        for i in EmployeeManagement().employee:
            print(i.name)

        # self.assertEqual(EmployeeManagement.find(EmployeeManagement(), emp.name), emp.display())
        self.assertEqual(
            EmployeeManagement.find(
                EmployeeManagement(),
                'dsfaf'),
            'No employee data found')

    def test_remove(self):
        emp = Employee(
            Employee.emp_id,
            'Krish Shah',
            20,
            'M',
            'Intern',
            0,
            9301671789)
        EmployeeManagement().employee.append(emp)
        self.assertEqual(
            EmployeeManagement.remove(
                EmployeeManagement(), emp.name), EmployeeManagement.find(
                EmployeeManagement(), emp.name))

    @patch('builtins.input',
           side_effect=['25', 'F', '100000', 'Manager', '1234'])
    def test_update(self, mock_input):
        EmployeeManagement()
        emp = Employee(
            Employee.emp_id,
            'Kris',
            20,
            'M',
            'Intern',
            0,
            9301671789)
        EmployeeManagement().employee.append(emp)

        EmployeeManagement().update('Kris')

        self.assertEqual(emp.age, '25')
        self.assertEqual(emp.gender, 'F')
        self.assertEqual(emp.salary, 100000)
        self.assertEqual(emp.position, 'Manager')
        self.assertEqual(emp.phone_number, 1234)

    def test_clear(self):
        self.assertEqual(
            EmployeeManagement.clear(
                EmployeeManagement()),
            'All Data cleared')


if __name__ == '__main__':
    unittest.main()
