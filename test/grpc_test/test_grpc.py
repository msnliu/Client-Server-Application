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
    assert 'Account matched: wayne' in output[2]
def test4():
    # Test listing multiple clients
    assert 'Account matched: wayne,mason' in output[7]
def test5():
    # Test log out
    assert 'You have been successfully logged out!' in output[3]
def test6():
    # Test sent message
    assert 'Your message has been sent!' in output[8]
def test7():
    # Test delete accounts
    assert 'Your account has been deleted!' in output[9]