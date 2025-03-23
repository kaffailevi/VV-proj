import datetime
import pytest # type: ignore
from unittest.mock import Mock, patch

from employee import Employee
from relations_manager import RelationsManager
from employee_manager import EmployeeManager, main

class TestEmployeeManager:
    """
    Test suite for the EmployeeManager class.
    This test suite includes the following tests:
    - test_calculate_salary_basic: Tests the basic salary calculation for a non-leader employee.
    - test_calculate_salary_for_leader: Tests the salary calculation for a leader employee with team members.
    - test_calculate_salary_for_new_employee: Tests the salary calculation for a newly hired employee.
    - test_calculate_salary_and_send_email: Tests the salary calculation and email sending functionality.
    - test_class_variables: Verifies the class variables of EmployeeManager.
    Fixtures:
    - relations_manager_mock: A mock of the RelationsManager class.
    - employee: A sample Employee instance.
    - employee_manager: An instance of EmployeeManager initialized with the relations_manager_mock.
    """
    
    @pytest.fixture
    def relations_manager_mock(self):
        """
        Creates a mock object for the RelationsManager class.

        Returns:
            Mock: A mock object with the same specification as the RelationsManager class.
        """
        return Mock(spec=RelationsManager)
    
    @pytest.fixture
    def employee(self):
        """
        Creates and returns an Employee object with predefined attributes.

        Returns:
            Employee: An Employee object with the following attributes:
                - id (int): The employee's ID.
                - first_name (str): The employee's first name.
                - last_name (str): The employee's last name.
                - base_salary (int): The employee's base salary.
                - birth_date (datetime.date): The employee's birth date.
                - hire_date (datetime.date): The employee's hire date.
        """
        return Employee(
            id=1, 
            first_name="John", 
            last_name="Doe", 
            base_salary=3000,
            birth_date=datetime.date(1970, 1, 31), 
            hire_date=datetime.date(2010, 10, 1)
        )
    
    @pytest.fixture
    def employee_manager(self, relations_manager_mock):
        """
        Creates an instance of EmployeeManager using the provided relations manager mock.

        Args:
            relations_manager_mock: A mock object for the relations manager.

        Returns:
            EmployeeManager: An instance of the EmployeeManager class.
        """
        return EmployeeManager(relations_manager_mock)
    
    def test_calculate_salary_basic(self, employee_manager, employee, relations_manager_mock):
        """
        Test the calculate_salary method for a basic employee scenario.
        This test verifies that the salary calculation for a non-leader employee
        is correct based on their base salary and the number of years they have
        been with the company.
        Args:
            employee_manager (EmployeeManager): The employee manager instance.
            employee (Employee): The employee instance whose salary is being calculated.
            relations_manager_mock (Mock): Mocked instance of the relations manager.
        Setup:
            - Mock the is_leader method of relations_manager_mock to return False.
            - Calculate the current year and the number of years the employee has been with the company.
            - Calculate the expected salary based on the employee's base salary and the yearly bonus.
        Execute:
            - Call the calculate_salary method of employee_manager with the employee instance.
        Verify:
            - Assert that the actual salary matches the expected salary.
            - Assert that the is_leader method of relations_manager_mock was called once with the employee instance.
        """
        # Setup
        relations_manager_mock.is_leader.return_value = False
        current_year = datetime.date.today().year
        years_at_company = current_year - employee.hire_date.year
        expected_salary = employee.base_salary + (years_at_company * EmployeeManager.yearly_bonus)
        
        # Execute
        actual_salary = employee_manager.calculate_salary(employee)
        
        # Verify
        assert actual_salary == expected_salary
        relations_manager_mock.is_leader.assert_called_once_with(employee)
    
    def test_calculate_salary_for_leader(self, employee_manager, employee, relations_manager_mock):
        """
        Test the calculation of salary for a leader employee.
        This test verifies that the salary calculation for a leader employee is correct.
        It mocks the relations manager to simulate the employee being a leader and having
        three team members. The expected salary is calculated based on the employee's base
        salary, the number of years at the company, and the bonuses for being a leader and
        having team members.
        Args:
            employee_manager (EmployeeManager): The employee manager instance.
            employee (Employee): The employee instance.
            relations_manager_mock (Mock): The mock of the relations manager.
        Asserts:
            The actual salary calculated by the employee manager matches the expected salary.
            The relations manager's `is_leader` method is called once with the employee.
            The relations manager's `get_team_members` method is called once with the employee.
        """
        # Setup
        relations_manager_mock.is_leader.return_value = True
        team_members = [Mock(), Mock(), Mock()]  # 3 team members
        relations_manager_mock.get_team_members.return_value = team_members
        
        current_year = datetime.date.today().year
        years_at_company = current_year - employee.hire_date.year
        expected_salary = (
            employee.base_salary + 
            (years_at_company * EmployeeManager.yearly_bonus) + 
            (len(team_members) * EmployeeManager.leader_bonus_per_member)
        )
        
        # Execute
        actual_salary = employee_manager.calculate_salary(employee)
        
        # Verify
        assert actual_salary == expected_salary
        relations_manager_mock.is_leader.assert_called_once_with(employee)
        relations_manager_mock.get_team_members.assert_called_once_with(employee)
    
    def test_calculate_salary_for_new_employee(self, employee_manager, relations_manager_mock):
        """
        Test the calculation of salary for a new employee.
        This test verifies that the salary calculation for a newly hired employee is correct.
        It ensures that the employee's base salary is used without any additional yearly bonuses,
        as the employee has not completed a full year at the company.
        Args:
            self: The test case instance.
            employee_manager (EmployeeManager): The employee manager instance used to calculate the salary.
            relations_manager_mock (Mock): A mock of the relations manager to control the behavior of the is_leader method.
        Setup:
            - Create a new employee with a hire date in the current year.
            - Mock the relations manager to return False for the is_leader method.
        Test:
            - Calculate the expected salary for the new employee (base salary with no yearly bonus).
            - Calculate the actual salary using the employee manager.
            - Assert that the actual salary matches the expected salary.
        """
        # Setup
        current_year = datetime.date.today().year
        new_employee = Employee(
            id=2, 
            first_name="Jane", 
            last_name="Smith", 
            base_salary=3500,
            birth_date=datetime.date(1990, 5, 15), 
            hire_date=datetime.date(current_year, 1, 1)  # Hired this year
        )
        relations_manager_mock.is_leader.return_value = False
        
        # Years at company should be 0 for someone hired this year
        expected_salary = new_employee.base_salary + (0 * EmployeeManager.yearly_bonus)
        
        # Execute
        actual_salary = employee_manager.calculate_salary(new_employee)
        
        # Verify
        assert actual_salary == expected_salary
    
    @patch('builtins.print')
    def test_calculate_salary_and_send_email(self, mock_print, employee_manager, employee, relations_manager_mock):
        """
        Test the calculate_salary_and_send_email method of EmployeeManager.
        This test verifies that the salary is correctly calculated based on the employee's
        base salary and years at the company, and that the appropriate email message is sent.
        Args:
            mock_print (Mock): Mock object for the print function.
            employee_manager (EmployeeManager): Instance of EmployeeManager to be tested.
            employee (Employee): Employee object containing employee details.
            relations_manager_mock (Mock): Mock object for the RelationsManager.
        Setup:
            - Mock the is_leader method of relations_manager_mock to return False.
            - Calculate the expected salary based on the employee's base salary and years at the company.
        Execute:
            - Call the calculate_salary_and_send_email method with the employee.
        Verify:
            - Assert that the print function is called once with the expected message.
        """
        # Setup
        relations_manager_mock.is_leader.return_value = False
        current_year = datetime.date.today().year
        years_at_company = current_year - employee.hire_date.year
        expected_salary = employee.base_salary + (years_at_company * EmployeeManager.yearly_bonus)
        
        # Execute
        employee_manager.calculate_salary_and_send_email(employee)
        
        # Verify
        mock_print.assert_called_once_with(
            f"{employee.first_name} {employee.last_name} your salary: {expected_salary} has been transferred to you."
        )
    
    def test_class_variables(self):
        """
        Test the class variables of the EmployeeManager class.

        This test verifies that the class variables `yearly_bonus` and 
        `leader_bonus_per_member` have the expected values.

        Assertions:
            - EmployeeManager.yearly_bonus is equal to 100.
            - EmployeeManager.leader_bonus_per_member is equal to 200.
        """
        # Verify class variables have expected values
        assert EmployeeManager.yearly_bonus == 100
        assert EmployeeManager.leader_bonus_per_member == 200


    def test_calculate_salary_for_leader_without_team(self, employee_manager, employee, relations_manager_mock):
        """
        Test the calculate_salary method for a leader without a team.
        This test verifies that the salary calculation for an employee who is a leader
        but does not have any team members is correct. The salary should be the base
        salary plus the yearly bonus for each year the employee has been at the company.
        Args:
            employee_manager (EmployeeManager): The employee manager instance.
            employee (Employee): The employee instance being tested.
            relations_manager_mock (Mock): Mocked relations manager to simulate leader status and team members.
        Setup:
            - Mock the relations_manager to return True for is_leader.
            - Mock the relations_manager to return an empty list for get_team_members.
            - Calculate the expected salary based on the employee's base salary and years at the company.
        Execute:
            - Call the calculate_salary method on the employee_manager with the employee.
        Verify:
            - Assert that the actual salary matches the expected salary.
            - Assert that is_leader was called once with the employee.
            - Assert that get_team_members was called once with the employee.
        """

        # Setup
        relations_manager_mock.is_leader.return_value = True
        relations_manager_mock.get_team_members.return_value = []  # No team members

        current_year = datetime.date.today().year
        years_at_company = current_year - employee.hire_date.year
        expected_salary = employee.base_salary + (years_at_company * EmployeeManager.yearly_bonus)

        # Execute
        actual_salary = employee_manager.calculate_salary(employee)

        # Verify
        assert actual_salary == expected_salary
        relations_manager_mock.is_leader.assert_called_once_with(employee)
        relations_manager_mock.get_team_members.assert_called_once_with(employee)

    @patch('builtins.print')
    def test_calculate_salary_and_send_email_for_leader(self, mock_print, employee_manager, employee, relations_manager_mock):
        """
        Test the calculate_salary_and_send_email method for a leader employee.
        This test verifies that the salary is correctly calculated for a leader employee
        and that the appropriate email message is printed.
        Args:
            mock_print (Mock): Mock object for the print function.
            employee_manager (EmployeeManager): Instance of EmployeeManager.
            employee (Employee): Instance of Employee.
            relations_manager_mock (Mock): Mock object for the RelationsManager.
        Setup:
            - Mock the is_leader method to return True.
            - Mock the get_team_members method to return a list of 2 team members.
            - Calculate the expected salary based on the employee's hire date,
            base salary, yearly bonus, and leader bonus per team member.
        Execute:
            - Call the calculate_salary_and_send_email method on the employee_manager
            with the employee as the argument.
        Verify:
            - Assert that the print function is called once with the expected message
            containing the employee's name and calculated salary.
        """
        # Setup
        relations_manager_mock.is_leader.return_value = True
        team_members = [Mock(), Mock()]  # 2 team members
        relations_manager_mock.get_team_members.return_value = team_members

        current_year = datetime.date.today().year
        years_at_company = current_year - employee.hire_date.year
        expected_salary = (
            employee.base_salary +
            (years_at_company * EmployeeManager.yearly_bonus) +
            (len(team_members) * EmployeeManager.leader_bonus_per_member)
        )

        # Execute
        employee_manager.calculate_salary_and_send_email(employee)

        # Verify
        mock_print.assert_called_once_with(
            f"{employee.first_name} {employee.last_name} your salary: {expected_salary} has been transferred to you."
        )

    def test_calculate_salary_for_long_term_employee(self, employee_manager, relations_manager_mock):
        """
        Test the calculation of salary for a long-term employee.
        This test verifies that the `calculate_salary` method of the `EmployeeManager`
        class correctly calculates the salary for an employee who has been with the 
        company for a long period (e.g., 40 years). The test sets up an employee with 
        a base salary and a hire date 40 years in the past, mocks the `relations_manager`
        to return that the employee is not a leader, and then checks that the calculated 
        salary includes the appropriate yearly bonuses.
        Args:
            self: The test case instance.
            employee_manager (EmployeeManager): The instance of EmployeeManager being tested.
            relations_manager_mock (Mock): A mock of the relations manager to control its behavior.
        Setup:
            - Create an `Employee` instance representing a long-term employee.
            - Mock the `is_leader` method of `relations_manager_mock` to return `False`.
            - Calculate the expected salary based on the employee's base salary and years at the company.
        Execute:
            - Call the `calculate_salary` method with the long-term employee.
        Verify:
            - Assert that the actual salary returned by `calculate_salary` matches the expected salary.
        """

        # Setup
        old_employee = Employee(
            id=3,
            first_name="Old",
            last_name="Worker",
            base_salary=4000,
            birth_date=datetime.date(1950, 7, 20),
            hire_date=datetime.date(1985, 3, 15)  # 40 years ago
        )
        relations_manager_mock.is_leader.return_value = False

        years_at_company = 40
        expected_salary = old_employee.base_salary + (years_at_company * EmployeeManager.yearly_bonus)

        # Execute
        actual_salary = employee_manager.calculate_salary(old_employee)

        # Verify
        assert actual_salary == expected_salary

    @patch('builtins.print')
    def test_main(self, mock_print):
        """
        Test the main function to ensure it calls the print function at least once.

        Args:
            mock_print (Mock): A mock object for the print function.
        """
        main()
        # Check that print was called at least once
        assert mock_print.call_count > 0