# Unit Test Documentation

## Project Overview
This project involves unit testing for an employee management system. The primary goal is to ensure the reliability and correctness of the codebase by testing individual units of functionality.

---

## Tools and Frameworks
- **Programming Language**: Python 3.5+
- **Testing Framework**: Pytest
  - Pytest was chosen for its simplicity, extensibility, and active community support.
  - Plugins such as `pytest-mock` and `pytest-cov` can be utilized for mocking and coverage analysis.

---

## Unit Test Structure
Unit tests are organized into separate test files for clarity and maintainability. Each test file corresponds to a module in the codebase:
- `relations_manager_test.py`: Tests for the `RelationsManager` class.
- `employee_manager_test.py`: Tests for the `EmployeeManager` class.

---

## Test Cases

### **RelationsManager Tests**
#### Purpose:
Verify team leader assignments, team memberships, and employee database integrity.

#### Test Cases:
1. **Check Team Leader Details**
   - *Input*: Employee named John Doe (birthdate: 31.01.1970).
   - *Expected Output*: John Doe is identified as a team leader.
   
2. **Validate Team Members**
   - *Input*: John Doe’s team members.
   - *Expected Output*: Myrta Torkelson and Jettie Lynch are valid team members.
   
3. **Ensure Non-Membership**
   - *Input*: Tomas Andre.
   - *Expected Output*: Tomas Andre is not a member of John Doe’s team.
   
4. **Verify Base Salary**
   - *Input*: Gretchen Walford.
   - *Expected Output*: Base salary equals $4000.
   
5. **Non-Leader Validation**
   - *Input*: Tomas Andre.
   - *Expected Output*: Tomas Andre is not a team leader; attempting to retrieve his team members throws an exception or returns empty data.
   
6. **Check Database Integrity**
   - *Input*: Jude Overcash.
   - *Expected Output*: Jude Overcash is not stored in the database.

---

### **EmployeeManager Tests**
#### Purpose:
Test salary calculations based on employment details, leader status, and email notifications.

#### Test Cases:
1. **Calculate Basic Salary**
   - *Input*: Non-leader employee hired on 10.10.1998 with a base salary of $1000.
   - *Expected Output*: Total salary = $3000 ($1000 + 20 years × $100 yearly bonus).
   
2. **Calculate Leader Salary**
   - *Input*: Team leader with 3 members, hired on 10.10.2008, base salary $2000.
   - *Expected Output*: Total salary = $3600 ($2000 + 10 years × $100 yearly bonus + 3 members × $200 leader bonus/member).
   
3. **Handle New Employee Salary**
   - *Input*: Employee hired in the current year with a base salary of $3500.
   - *Expected Output*: Total salary = $3500 (no bonuses applied).
   
4. **Salary Notification Email**
   - *Input*: Employee details for salary calculation and email notification.
   - *Expected Output*: Correct email message sent with calculated salary details.

5. **Class Variables Validation**
   - *Purpose*: Ensure constants like `yearly_bonus` and `leader_bonus_per_member` are correctly defined.

---

## Best Practices Followed
- **Descriptive Test Names**: Each test clearly describes its purpose and expected behavior.
- **Atomic Tests**: Each test focuses on a single functionality to ensure clarity and maintainability.
- **Mocking**: External dependencies such as database queries or email services are mocked to isolate unit functionality.
- **Edge Case Coverage**: Tests include scenarios like new employees or non-leader validations to ensure robustness.

---

## Running the Tests
1. Activate virtual environment:
    ```
    source pytest-env/bin/activate
    ```
2. Execute all tests:
    ```
    pytest -v
    ```
3. View detailed output for failed tests:
    ```
    pytest --tb=short
    ```

---

