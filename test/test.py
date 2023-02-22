import pytest

f = open("output.txt", "r")
li = f.readlines()

output = [x for x in li if x != '\n']

def test1():
    assert 'To get started on this chat room' in output[0]
def test2():
    assert 'new Account ID: mason123' in output[1]
def test3():
    assert 'Showing all accounts: mason' in output[2]
def test4():
    assert 'No new messages' in output[3]