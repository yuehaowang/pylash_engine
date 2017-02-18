import runpy, sys, os

import pylash

argv = sys.argv[1:]
pathList = argv[0].split(".")

if len(pathList) >= 2:
	dirPath = "./%s/%s" % (pathList[0], pathList[1])

	os.chdir(dirPath)

	runpy.run_path("./Main.py", run_name = "__main__")