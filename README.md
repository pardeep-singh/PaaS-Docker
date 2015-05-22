PaaS-Docker
===========
A PaaS tool to deploy applications on your servers.

Just add a webhook to github repository having a dockerfile and see every push made on repository be deployed in a seconds. 

### Requirements <hr>

PaaS-Docker is compatible with Python version 2 and 3; and require Flask,Docker,Docker-py and git cli to be installed.

PaaS-Docker currently supports linux enviroments.

Install Flask

    pip install flask
Install Docker-py

    pip install docker-py
Install docker and git cli depending upon your enviroment.

### Usage <hr>

1) Clone the repository on your local machine

    git clone https://github.com/pardeep-paxcel/PaaS-Docker.git
2) Change to the cloned directory

    cd Paas-Docker
3) Run the app.py file

    python app.py
4) Add a webhook to github repository having Dockerfile and enter your host address and port number in payload url 

    http://ip:port/hook
  
  Keep the content type to application/json  
  




  

  






