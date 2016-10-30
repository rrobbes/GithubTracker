import os


def then_do(path, command):
	oldPath = os.getcwd()
	os.chdir(path)
	stream = os.popen(command)
	os.chdir(oldPath)
	return stream


def then_print(path, command):
	for l in then_do(path, command): print l

