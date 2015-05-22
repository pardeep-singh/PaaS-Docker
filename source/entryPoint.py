from . import utility
from . import githubOperations as github
from . import dockerOperations as docker
import os
from flask import jsonify

def filterRequestData(requestData):
    requestDict = {}
    requestDict['repoName'] = requestData['repository']['name']
    requestDict['ownerName'] = requestData['repository']['owner']['name']
    requestDict['repoFullName'] = requestData['repository']['full_name']
    requestDict['repoCloneUrl'] = requestData['repository']['clone_url']
    requestDict['ref'] = requestData['ref']
    
    requestDict['branchName'] = requestDict['ref'][11:]
   
    requestDict['repoFullName'] = requestDict['repoFullName']+'/'+requestDict['branchName']
    requestDict['localRepoPath'] = utility.getLocalReposPath()+'/'+requestDict['repoFullName']

    requestDict['ownerName'] = requestDict['ownerName'].lower()
    requestDict['ownerName'] = requestDict['ownerName'].replace('-','_')
    requestDict['repoName'] = requestDict['repoName'].lower()
    
    requestDict['dockerImageName'] = requestDict['repoName']+'_'+utility.verifyBranchName(requestDict['branchName'])
    requestDict['dockerImageNamespace'] = requestDict['ownerName']
    return requestDict

def main(requestData):
    requestDataDict = filterRequestData(requestData)
    print(requestDataDict)
    utility.removeDirIfExist(requestDataDict['localRepoPath'])
    
    try:
        github.clone(requestDataDict['branchName'],requestDataDict['repoCloneUrl'],requestDataDict['localRepoPath'])
        portsUsed = docker.getPortsUsed(requestDataDict['dockerImageNamespace'],requestDataDict['dockerImageName'])
        buildResponse = docker.buildImage(requestDataDict['localRepoPath'],requestDataDict['dockerImageNamespace'],requestDataDict['dockerImageName'])
        print(buildResponse)
        portsToBeUsed = utility.getPorts(portsUsed,requestDataDict['localRepoPath'])
        print(portsToBeUsed)
        docker.createContainer(requestDataDict['dockerImageNamespace'],requestDataDict['dockerImageName'],portsToBeUsed)
        return jsonify(success=True),200
    except OSError as osError:
        return jsonify(success=False,error=str(osError)),400
    except TypeError as typeError:
        return jsonify(success=False,error=str(typeError)),400
    except IOError as ioError:
        return jsonify(success=False,error=str(ioError)),400
    

 
        
	