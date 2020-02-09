'''
This is a script tool for running demo and examples made with pylash.
With this tool, you can run demo and examples without installing pylash.
'''

import runpy, sys, os

__author__ = "Yuehao Wang"

ENTRANCE_FILE = "Main.py"
PYLASH_ROOT_DIR = os.path.dirname(__file__)
AVAILABLE_TARGET_NAME = [
	"%s.%s" % (os.path.basename(path), f) \
	for path in [os.path.join(PYLASH_ROOT_DIR, "demo"), os.path.join(PYLASH_ROOT_DIR, "examples")] \
	for f in os.listdir(path) \
	if os.path.isdir(os.path.join(path, f))
]

HELP_TEXT = '''
usage: python run.py TARGET_NAME

Available TARGET_NAME:

  %s
''' % ("\n  ".join(AVAILABLE_TARGET_NAME))

def main():
	if len(sys.argv) <= 1:
		print(HELP_TEXT)
		return
	
	argv = sys.argv[1:]
	target_name = argv[0].strip()

	if target_name in AVAILABLE_TARGET_NAME:
		pathList = target_name.split(".")
		dirPath = os.path.join(PYLASH_ROOT_DIR, *pathList)
		entrancePath = os.path.join(dirPath, ENTRANCE_FILE)

		if not os.path.isdir(dirPath) or not os.path.isfile(entrancePath):
			print(HELP_TEXT)
		else:
			os.chdir(dirPath)
			sys.path.insert(0, PYLASH_ROOT_DIR)

			runpy.run_path(ENTRANCE_FILE, run_name = "__main__")
	else:
		print(HELP_TEXT)

main()
