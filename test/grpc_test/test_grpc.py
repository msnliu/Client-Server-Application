import pytest

f = open("output.txt", "r")
li = f.readlines()

output = [x for x in li if x != '\n']

def test1():
    # Test Login message
    assert 'Welcome to the chatroom! ' in output[0]
def test2():
    # Test Account Creation
    assert 'Account wayne has been created!' in output[1]
def test3():
    # Test listing account
    assert 'Account matched:' in output[2]
# def test5():
#     # Test log out
#     assert 'You have been successfully logged out!' in output[4]