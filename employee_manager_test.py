import datetime
import pytest # type: ignore
from unittest.mock import Mock, patch

from employee import Employee
from relations_manager import RelationsManager
from employee_manager import EmployeeManager

class TestEmployeeManager:
    
    @pytest.fixture
    def relations_manager_mock(self):
        return Mock(spec=RelationsManager)
    
    @pytest.fixture
    def employee(self):
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
        return EmployeeManager(relations_manager_mock)
    
    def test_calculate_salary_basic(self, employee_manager, employee, relations_manager_mock):
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
        # Verify class variables have expected values
        assert EmployeeManager.yearly_bonus == 100
        assert EmployeeManager.leader_bonus_per_member == 200
