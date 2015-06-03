PaaS-Docker
===========
PaaS-Docker is a service to deploy applications on your servers.

Just add a webhook to github repository having a dockerfile and see every push made on repository be deployed in a seconds.

PaaS-Docker is a service written in python using flask framework which listen to github repository events. Whenever a new push is made to github repository, PaaS-Docker will fetch a github repository and build a new docker image. The newly built image will be deployed to server running this service.

As of now PaaS-Docker supports single container applications.

### Requirements <hr>

PaaS-Docker is compatible with Python version 2 and 3; and require Flask,Docker,Docker-py and git to be installed.

PaaS-Docker currently supports linux enviroments.

Install Project dependencies

    pip install -r requirements.txt

Install docker and git depending upon your enviroment.

### Usage <hr>

1) Clone the repository on your local machine

    git clone https://github.com/pardeep-paxcel/PaaS-Docker.git
2) Change to the cloned directory

    cd Paas-Docker
3) Running the service

    sudo python app.py
4) Add a webhook to github repository having Dockerfile and enter your host address and port number in payload url 

    http://ip:port/hook
  
  Keep the content type to application/json  
  




  

  






