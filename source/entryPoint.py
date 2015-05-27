from . import utility
from . import githubOperations as github
from . import dockerOperations as docker
import os
from flask import jsonify
from .RepoContainerMapping import RepoContainerMapping

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
    
    requestDict['generatedBranchName'] = utility.verifyBranchName(requestDict['branchName'])

    requestDict['dockerImageName'] = requestDict['repoName']+'_'+requestDict['generatedBranchName']
    requestDict['dockerImageNamespace'] = requestDict['ownerName']
    requestDict['dockerImageRepo'] = requestDict['dockerImageNamespace']+'/'+requestDict['dockerImageName']

    return requestDict

def main(requestData):
    requestDataDict = filterRequestData(requestData)
    print(requestDataDict)
    utility.removeDirIfExist(requestDataDict['localRepoPath'])
    
    try:
        
        repContMapping = RepoContainerMapping()
        (portsUsed,containerID) = repContMapping.getPortsNContainerID(requestDataDict)

        print("Ports Used:",portsUsed," Container Id:",containerID)

        github.clone(requestDataDict['branchName'],requestDataDict['repoCloneUrl'],requestDataDict['localRepoPath'])
        
        if len(containerID):
            docker.stopContainer(containerID)
            docker.removeContainer(containerID)
 
#        portsUsed = docker.getPortsUsed(requestDataDict['dockerImageNamespace'],requestDataDict['dockerImageName'])
 
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
    

 
        
	