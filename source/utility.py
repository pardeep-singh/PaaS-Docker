import socket
import string
import random
import re
import shutil
import os
import json
from os.path import expanduser
from .RepoContainerMapping import RepoContainerMapping

def load_dockerConfig():
	with open('dockerConfig.json') as config_file:
		return json.load(config_file)

def removeDirIfExist(dirPath):
    if os.path.isdir(dirPath):
        print("dir exit going to remove it")
        shutil.rmtree(dirPath)
    else:
       print("dir doesnt exits")

def getSystemHomePath():
    homePath = expanduser('~')
    print(homePath)
    return homePath
    
def createIfDirDoesntExist(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    return dirPath
        
def getLocalReposPath():
    return createIfDirDoesntExist(getSystemHomePath()+'/GitRepos/')
       
def getAvailablePort():
    dummySocket = socket.socket()
    dummySocket.bind(('',0))
    availablePort = dummySocket.getsockname()[1]
    dummySocket.close()
    print('Avil',' ',availablePort)
    return availablePort

def getExposedPortNumber(dockerFilePath):
    exitFlag = False
    with open(dockerFilePath) as dockerFile:
        for line in dockerFile:
            for word in line.split():
                if exitFlag:
                    privatePortNumber = word
                    return privatePortNumber
                if 'EXPOSE' in line or 'expose' in line:
                    exitFlag=True

def getPorts(portsUsed,localRepoPath):
    portToBeUsed = {}
    if len(portsUsed):
        portToBeUsed = portsUsed
    else:
        portToBeUsed['publicPort'] = getAvailablePort()
        portToBeUsed['privatePort'] = int(getExposedPortNumber(localRepoPath+'/Dockerfile'))
    return portToBeUsed

def branchNameGenerator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
    
def verifyBranchName(ownerName,repoName,branchName):
    repContMapping = RepoContainerMapping()
    mapping = repContMapping.getMapping({'ownerName':ownerName,'repoName':repoName,'branchName':branchName})
    print("verifyng branch Name:",mapping)
    if mapping:
        return mapping['generatedBranchName']
    else:
        branchNameRegex = "^[a-z0-9_.-]+$"
        branchNameValidator = re.compile(branchNameRegex)
        if branchNameValidator.match(branchName):
            return branchName
        else:
            generatedBranchName = branchNameGenerator()
            while repContMapping.getMapping({'generatedBranchName':generatedBranchName}):
                generatedBranchName = branchNameGenerator()             
            return generatedBranchName 

## wordpress poc

def getWordPressLocalRepoPath():
    return createIfDirDoesntExist(getSystemHomePath()+'/wordpressData/sites/')

def getMysqlDBPath():
    return createIfDirDoesntExist(getSystemHomePath()+'/wordpressData/db/')
