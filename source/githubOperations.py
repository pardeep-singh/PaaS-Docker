import subprocess
import os

def clone(branchName,repoCloneUrl,repoFullName):
	subprocess.call(['git','clone','-b',branchName,repoCloneUrl,repoFullName])
		