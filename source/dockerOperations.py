from docker import Client
import docker
from . import utility

def getDockerConn():
	config = utility.load_dockerConfig()
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
	
def stopContainer(containerID):
	conn = getDockerConn()
	conn.stop(containerID)
	
def removeContainer(containerID):
	conn = getDockerConn()
	conn.remove_container(containerID)
	
def buildImage(localRepoPath,dockerImageRepo):
	conn = getDockerConn()
	buildResponse = [line for line in conn.build(
		path=localRepoPath,tag=dockerImageRepo,rm=True
		)]
	return buildResponse
	
def createContainer(dockerImageRepo,portsToBeUsed):
	conn = getDockerConn()
	container = conn.create_container(
		image=dockerImageRepo,ports=[portsToBeUsed['privatePort']],
		host_config=docker.utils.create_host_config(
			port_bindings={portsToBeUsed['privatePort']:('0.0.0.0',portsToBeUsed['publicPort'])}
			)
		)
	print(container)
	conn.start(container)
	return container['Id']

## wordpress poc
def createWordPressContainer(systemPort,systemRepoPath,dbName):
	conn = getDockerConn()
	container = conn.create_container(
		image="phpwithmysql:v2",ports=[80],volumes=["/var/www/html"],environment=["WORDPRESS_DB_PASSWORD=password"],
		host_config=docker.utils.create_host_config(
			port_bindings={80:('0.0.0.0',systemPort)},
			binds={systemRepoPath:{'bind':'/var/www/html'}},
			links={(dbName,'mysql')}
			)
	)
	conn.start(container['Id'])
	return container['Id']

def createMysqlContainer(systemDBpath):
	conn = getDockerConn()
	container = conn.create_container(
		image="mysql:5.7",detach=True,volumes=["/var/lib/mysql"],
		environment=["MYSQL_ROOT_PASSWORD=password","MYSQL_DATABASE=wordpress","MYSQL_USERNAME=root"],
		host_config=docker.utils.create_host_config(
			binds={systemDBpath:{'bind':'/var/lib/mysql'}}
			)
	)
	conn.start(container['Id'])
	return container['Id']

def inspectContainer(containerID):
	conn = getDockerConn()
	containerInfo = conn.inspect_container(containerID)
	return containerInfo
	

