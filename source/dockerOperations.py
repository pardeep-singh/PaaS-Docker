from docker import Client
import docker

def load_dockerConfig():
    with open('dockerConfig.json') as config_file:    
        return json.load(config_file)

def getDockerConn():
	config = load_dockerConfig()
	print("Docker:",config.get('docker_deamon'))
	print("Version:",config.get('docker_server_version'))
	return Client(base_url=config.get('docker_deamon'),version=config.get('docker_server_version'))
	
def getPortsUsed(dockerImageNamespace,dockerImageName):
	conn = getDockerConn()
	containersList = conn.containers()
	portsUsed = []
	for containerInfo in containersList:
		print(containerInfo['Image'],' ',dockerImageNamespace+'/'+dockerImageName+':latest')
		if containerInfo['Image'] == dockerImageNamespace+'/'+dockerImageName+':latest':
			portsUsed = containerInfo['Ports']
			conn.stop(containerInfo['Id'])
			conn.remove_container(containerInfo['Id'])
			return portsUsed
	return portsUsed
	
def buildImage(repoFullName,dockerImageNamespace,dockerImageName):
	conn = getDockerConn()
	buildResponse = [line for line in conn.build(
		path=repoFullName,tag=dockerImageNamespace+'/'+dockerImageName,rm=True
		)]
	return buildResponse
	
def createContainer(dockerImageNamespace,dockerImageName,portsToBeUsed):
	conn = getDockerConn()
	container = conn.create_container(
		image=dockerImageNamespace+'/'+dockerImageName,ports=[portsToBeUsed['privatePort']],
		host_config=docker.utils.create_host_config(
			port_bindings={portsToBeUsed['privatePort']:('0.0.0.0',portsToBeUsed['publicPort'])}
			)
		)
	print(container)
	conn.start(container)

	

