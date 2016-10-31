import os


def then_do(path, command):
	path = "cd "+ path
	cmd = path + ';' + command
	stream = os.popen(cmd)
	return stream


def then_print(path, command):
	for l in then_do(path, command): print l

