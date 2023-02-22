import pytest

f = open("output.txt", "r")
li = f.readlines()

output = [x for x in li if x != '\n']

def test1():
    # Test Login message
    assert 'To get started on this chat room' in output[0]
def test2():
    # Test Account Creation
    assert 'new Account ID: mason123' in output[1]
def test3():
    # Test listing account
    assert 'Showing all accounts: mason' in output[2]
def test4():
    # Test delivery underlivered message(when there is None)
    assert 'No new messages' in output[3]
def test5():
    # Test delete account (when there is no message left)
    assert 'Your account has been deleted' in output[4]