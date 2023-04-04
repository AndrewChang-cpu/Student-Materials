import pytest
import System


# username = 'calyam'
# password =  '#yeet'
# username2 = 'hdjsr7'
# username3 = 'yted91'
# course = 'cloud_computing'
# assignment = 'assignment1'
# profUser = 'goggins'
# profPass = 'augurrox'
#
# # Tests if the program can handle a wrong username
# def test_login(grading_system):
#     username = 'thtrhg'
#     password =  'fhjhjdhjdfh'
#     grading_system.login(username,password)
#
# def test_check_password(grading_system):
#     test = grading_system.check_password(username,password)
#     test2 = grading_system.check_password(username,'#yeet')
#     test3 = grading_system.check_password(username,'#YEET')
#     if test == test3 or test2 == test3:
#         assert False
#     if test != test2:
#         assert False

def test_login(grading_system):
    username = "testuser"
    password = "12345678"
    grading_system.login(username,password)
    grading_system.reload_data()
    assert grading_system.check_password(username,password)

def test_check_password(grading_system):
    username = "hdjsr7"
    check1 = grading_system.check_password(username, "pass1234")
    check2 = grading_system.check_password(username, "PASS1234")
    check3 = grading_system.check_password(username, "  pass1234")
    assert check1 and not check2 and not check3

def test_change_grade(grading_system):
    grading_system.login('cmhbf5', 'bestTA')
    grading_system.usr.change_grade('yted91', 'software_engineering', 'assignment1', 0)
    grading_system.reload_data()
    assert dict(grading_system.usr.check_grades('yted91', 'software_engineering'))['assignment1'] == 0

    grading_system.login('cmhbf5', 'bestTA')
    grading_system.usr.change_grade('yted91', 'software_engineering', 'assignment1', 43)
    grading_system.reload_data()
    assert dict(grading_system.usr.check_grades('yted91', 'software_engineering'))['assignment1'] == 43

def test_create_assignment(grading_system):
    grading_system.login('cmhbf5', 'bestTA')
    grading_system.usr.create_assignment('test_assignment', '04/01/20', 'software_engineering')
    grading_system.reload_data()
    assert 'test_assignment' in grading_system.courses['software_engineering']['assignments'] and \
           grading_system.courses['software_engineering']['assignments']['test_assignment']['due_date'] == '04/01/20'

    del grading_system.usr.all_courses['software_engineering']['assignments']['test_assignment']
    grading_system.usr.update_course_db()

def test_add_student(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.add_student('yted91', 'databases')
    grading_system.reload_data()
    assert 'databases' in grading_system.usr.users['yted91']['courses']

    del grading_system.usr.users['yted91']['courses']['databases']
    grading_system.usr.update_course_db()

def test_drop_student(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.users['yted91']['courses'].update({"databases": {}})
    grading_system.usr.update_course_db()

    grading_system.usr.drop_student('yted91', 'databases')
    grading_system.reload_data()
    assert 'databases' not in grading_system.usr.users['yted91']['courses']

def test_submit_assignment(grading_system):
    grading_system.login('hdjsr7', 'pass1234')
    grading_system.usr.submit_assignment('cloud_computing', 'assignment1','Blahhhhh', '03/01/20')
    grading_system.reload_data()
    assert grading_system.usr.courses['cloud_computing']['assignment1']['submission_date'] == '03/01/20' and \
           grading_system.usr.courses['cloud_computing']['assignment1']['submission'] == 'Blahhhhh'

    default = {"assignment1": {
        "grade": 100,
        "submission_date": "1/3/20",
        "submission": "Blah Blah Blah",
        "ontime": True
    }}
    grading_system.usr.users['hdjsr7']['courses']['cloud_computing'].update(default)
    grading_system.usr.update_user_db()

def test_check_ontime(grading_system):
    grading_system.login('hdjsr7', 'pass1234')
    assert grading_system.usr.check_ontime('01/01/20','01/01/20') and \
           not grading_system.usr.check_ontime('01/01/20','01/02/20')

def test_check_grades(grading_system): #faulty test data for hdjsr7?
    grading_system.login('akend3', '123454321')
    grades = grading_system.usr.check_grades('databases')
    assignments = grading_system.usr.users['akend3']['courses']['databases']
    for i in range(len(grades)):
        assert grades[i][1] == assignments[grades[i][0]]['grade']

def test_view_assignments(grading_system):
    grading_system.login('akend3', '123454321')
    dates = grading_system.usr.view_assignments('databases')
    assignments = grading_system.usr.all_courses['databases']['assignments']
    for i in range(len(dates)):
        assert dates[i][1] == assignments[dates[i][0]]['due_date']

# def test_(grading_system):
#     1 + 1
#     assert True

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
