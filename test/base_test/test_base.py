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
    assert 'Account matched: mason' in output[2]
def test4():
    # Test delivery underlivered message(when there is None)
    assert 'No new messages' in output[3]
def test5():
    # Test list all accounts
    assert 'Showing all accounts: mason,wayne' in output[6]
def test6():
    # Test logoff and mailbox
    assert 'message from wayne has been delivered to mason' in output[7]
def test7():
    # Test account delete
    assert 'Your account has been deleted' in output[8]

def test8():
    # Test finding accoutings after delete
    assert 'Account matched to: w.yne doesn' in output[9]

def test9():
    # Test login after logoff
    assert 'user : mason is now logged in' in output[11]

def test10():
    # Test login after logoff
    assert 'undelivered message for user ID mason123' in output[12] and 'wayne sends: hi' in output[13]

def test11():
    # Test send message to someone that has been deleted
    assert 'Receiver: wayne doesn\'t exist ' in output[14]
