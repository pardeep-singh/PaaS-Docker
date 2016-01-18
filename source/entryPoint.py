from . import utility
from . import githubOperations as github
from . import dockerOperations as docker
import os
import subprocess
from flask import jsonify
from .RepoContainerMapping import RepoContainerMapping
from .wordpressMapping import WordpressMapping

def filterRequestData(requestData):
    requestDict = {}
    requestDict['repoName'] = requestData['repository']['name']
    requestDict['ownerName'] = requestData['repository']['owner']['name']
    requestDict['repoFullName'] = requestData['repository']['full_name']
    requestDict['repoCloneUrl'] = requestData['repository']['clone_url']
    requestDict['ref'] = requestData['ref']
    
    requestDict['branchName'] = requestDict['ref'][11:]
   
    requestDict['repoFullName'] = requestDict['repoFullName']+'/'+requestDict['branchName']
    requestDict['localRepoPath'] = utility.getLocalReposPath()+requestDict['repoFullName']

    requestDict['ownerName'] = requestDict['ownerName'].lower()
    requestDict['ownerName'] = requestDict['ownerName'].replace('-','_')
    requestDict['repoName'] = requestDict['repoName'].lower()
    
    requestDict['generatedBranchName'] = utility.verifyBranchName(requestDict['ownerName'],requestDict['repoName'],requestDict['branchName'])

    requestDict['dockerImageName'] = requestDict['repoName']+'_'+requestDict['generatedBranchName']
    requestDict['dockerImageNamespace'] = requestDict['ownerName']
    requestDict['dockerImageRepo'] = requestDict['dockerImageNamespace']+'/'+requestDict['dockerImageName']

    return requestDict

def main(requestData):
    
    try:
        
        requestDataDict = filterRequestData(requestData)
        print(requestDataDict)
        utility.removeDirIfExist(requestDataDict['localRepoPath'])
        
        repContMapping = RepoContainerMapping()
        (portsUsed,containerID) = repContMapping.getPortsNContainerID(requestDataDict)

        print("Ports Used:",portsUsed," Container Id:",containerID)

        github.clone(requestDataDict['branchName'],requestDataDict['repoCloneUrl'],requestDataDict['localRepoPath'])

        if containerID:
            docker.stopContainer(containerID)
            docker.removeContainer(containerID)
 
        buildResponse = docker.buildImage(requestDataDict['localRepoPath'],requestDataDict['dockerImageRepo'])
        print(buildResponse)
 
        portsToBeUsed = utility.getPorts(portsUsed,requestDataDict['localRepoPath'])
        print("New Ports:",portsToBeUsed)
 
        containerID = docker.createContainer(requestDataDict['dockerImageRepo'],portsToBeUsed)
        repContMapping.addPortsNContainerID(requestDataDict['dockerImageRepo'],portsToBeUsed,containerID)
        
        
        return jsonify(success=True),200
    except OSError as osError:
        return jsonify(success=False,error=str(osError)),400
    except TypeError as typeError:
        return jsonify(success=False,error=str(typeError)),400
    except IOError as ioError:
        return jsonify(success=False,error=str(ioError)),400
    
## wordpress poc 

def wordpressRequestFilter(requestData):
    requestDict = {}
    requestDict['repoName'] = requestData['repository']['name']
    requestDict['ownerName'] = requestData['repository']['owner']['name']
    requestDict['repoFullName'] = requestData['repository']['full_name']
    requestDict['repoCloneUrl'] = requestData['repository']['clone_url']
    requestDict['ref'] = requestData['ref']
    
    requestDict['branchName'] = requestDict['ref'][11:]
   
    requestDict['repoFullName'] = requestDict['repoFullName']+'/'+requestDict['branchName']
    requestDict['localRepoPath'] = utility.getWordPressLocalRepoPath()+requestDict['repoFullName']

    return requestDict
    
def wordpressMain(requestData):
    requestDataDict = wordpressRequestFilter(requestData)
    print(requestDataDict)
    
    wordpressMapping = WordpressMapping()
    mapping = wordpressMapping.getExistingMapping(requestDataDict['ownerName'],requestDataDict['repoName'],requestDataDict['branchName'])

    newRequest = True
 
    if mapping:
        print("request from exiting branch")
        newRequest = False
        docker.stopContainer(mapping['containerID'])
        docker.removeContainer(mapping['containerID'])
        utility.removeDirIfExist(requestDataDict['localRepoPath'])
        availablePort = mapping['publicPort']
        mysqlDBName = mapping['dbInfo']['dbName']
        print("container removed")
    else:
        print("new branch request")
        availablePort = utility.getAvailablePort()
        mysqlDBpath = utility.getMysqlDBPath()+requestDataDict['repoFullName']
        utility.createIfDirDoesntExist(mysqlDBpath)
        mysqlContainerId = docker.createMysqlContainer(mysqlDBpath)
        mysqlContainerInfo = docker.inspectContainer(mysqlContainerId)
        mysqlDBName = mysqlContainerInfo['Name'][1:len(mysqlContainerInfo['Name'])]
        print(mysqlDBName)
        dbDict = {'dbName':mysqlDBName,'containerId':mysqlContainerId,'dbPath':mysqlDBpath}
        print(dbDict)
        requestDataDict['dbInfo'] = dbDict

    github.clone(requestDataDict['branchName'],requestDataDict['repoCloneUrl'],requestDataDict['localRepoPath'])
    subprocess.call(['chmod','-R','777',requestDataDict['localRepoPath']])
    containerID = docker.createWordPressContainer(availablePort,requestDataDict['localRepoPath'],mysqlDBName)

    print(containerID)

    if newRequest:
        requestDataDict['publicPort'] = availablePort
        requestDataDict['containerID'] = containerID
        wordpressMapping.saveNewMapping(requestDataDict)
    else:
        mapping['publicPort'] = availablePort
        mapping['containerID'] = containerID
        wordpressMapping.updatePortNContainerID(mapping)

    print("yeah it worked")

    return jsonify(success=True),200

 
        
	