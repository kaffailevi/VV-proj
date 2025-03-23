import pytest # type: ignore
from relations_manager import RelationsManager
from employee import Employee


@pytest.fixture
def relations_manager():
    """
    Creates and returns an instance of the RelationsManager class.

    Returns:
        RelationsManager: An instance of the RelationsManager class.
    """
    return RelationsManager()


def test_is_leader(relations_manager):
    """
    Test the is_leader method of the RelationsManager class.
    This test verifies that the is_leader method correctly identifies
    whether an employee is a leader or not.
    Args:
        relations_manager (RelationsManager): An instance of the RelationsManager class.
    Test Cases:
        1. The first employee in the employee_list is a leader.
        2. The second employee in the employee_list is not a leader.
    Assertions:
        - Asserts that the is_leader method returns True for the leader.
        - Asserts that the is_leader method returns False for the non-leader.
    """
    leader = relations_manager.employee_list[0]  # John Doe (ID=1)
    non_leader = relations_manager.employee_list[1]  # Myrta Torkelson (ID=2)

    assert relations_manager.is_leader(leader) is True
    assert relations_manager.is_leader(non_leader) is False


def test_get_all_employees(relations_manager):
    """
    Test the get_all_employees method of the relations_manager.

    This test checks the following:
    1. The total number of employees returned by the method is 6.
    2. The first name of the first employee in the list is "John".

    Args:
        relations_manager (RelationsManager): An instance of the RelationsManager class.

    Assertions:
        - The length of the employees list is 6.
        - The first name of the first employee is "John".
    """
    employees = relations_manager.get_all_employees()
    assert len(employees) == 6 
    assert employees[0].first_name == "John"  


def test_get_team_members(relations_manager):
    """
    Test the `get_team_members` method of the `RelationsManager` class.
    This test verifies that the `get_team_members` method correctly identifies
    the team members of a given leader and handles cases where the employee is
    not a leader.
    Test cases:
    1. Verify that the leader (John Doe, ID=1) has exactly two team members.
    2. Check that Myrta Torkelson (ID=2) is a member of John Doe's team.
    3. Check that Jettie Lynch (ID=3) is a member of John Doe's team.
    4. Verify that a non-leader (Myrta Torkelson, ID=2) has no team members.
    Args:
        relations_manager (RelationsManager): An instance of the RelationsManager class.
    """
    leader = relations_manager.employee_list[0]  # John Doe (ID=1)
    team_members = relations_manager.get_team_members(leader)

    assert len(team_members) == 2  
    assert 2 in team_members  #  Myrta Torkelson (ID=2) benne van
    assert 3 in team_members  #  Jettie Lynch (ID=3) benne van

    non_leader = relations_manager.employee_list[1]  # Myrta Torkelson (ID=2)
    
    # Kezeljük azokat az eseteket, amikor None-t ad vissza
    team_members_of_non_leader = relations_manager.get_team_members(non_leader) or []  
    assert team_members_of_non_leader == []  # Nem vezetőnek nincs csapata

