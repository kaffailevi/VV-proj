import pytest # type: ignore
from relations_manager import RelationsManager
from employee import Employee


@pytest.fixture
def relations_manager():
    """Fixture a RelationsManager példány létrehozásához."""
    return RelationsManager()


def test_is_leader(relations_manager):
    """Tesztelje, hogy az is_leader metódus helyesen működik."""
    leader = relations_manager.employee_list[0]  # John Doe (ID=1)
    non_leader = relations_manager.employee_list[1]  # Myrta Torkelson (ID=2)

    assert relations_manager.is_leader(leader) is True
    assert relations_manager.is_leader(non_leader) is False


def test_get_all_employees(relations_manager):
    """Tesztelje, hogy a get_all_employees metódus helyesen adja vissza az összes alkalmazottat."""
    employees = relations_manager.get_all_employees()
    assert len(employees) == 6  # Ellenőrizze, hogy 6 alkalmazott van-e
    assert employees[0].first_name == "John"  # Ellenőrizze az első alkalmazott nevét


def test_get_team_members(relations_manager):
    """Tesztelje, hogy a get_team_members metódus helyesen működik."""
    leader = relations_manager.employee_list[0]  # John Doe (ID=1)
    team_members = relations_manager.get_team_members(leader)

    assert len(team_members) == 2  # John Doe csapatában két tag van
    assert 2 in team_members  # Ellenőrizze, hogy Myrta Torkelson (ID=2) benne van
    assert 3 in team_members  # Ellenőrizze, hogy Jettie Lynch (ID=3) benne van

    non_leader = relations_manager.employee_list[1]  # Myrta Torkelson (ID=2)
    
    # Kezeljük azokat az eseteket, amikor None-t ad vissza
    team_members_of_non_leader = relations_manager.get_team_members(non_leader) or []  
    assert team_members_of_non_leader == []  # Nem vezetőnek nincs csapata

