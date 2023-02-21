import subprocess
bashCommand = 'cd ~ < ls '
print(subprocess.check_output(bashCommand, shell=True))