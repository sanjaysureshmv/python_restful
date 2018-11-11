# python_restful

The app uses pythons flak framework for the REST API implementation. The database used is MySQL database. For entering messages, a simple html form is used. The messages entered by the users will be stored on the DB and using various api calls this messages can be viewed, searched and deleted. 
For the provisioning of servers, Terraform is used. Upon execution of the main.tf file, an ec2 instance, security group, and a loadbalancer will be provisioned. The instance will get attached to the classic loadbalancer after the loadbalancer is provisioned. 
For configuring the packages and satisying dependencies needed by the application, Ansible is used. Ansible will be called immediately after the instance is provisioned. Ansible will configure MySQL, python environment and run the app. 




Howto

Build app - python3.x app.py 

Deployment of the app
---------------------
Dependencies: Terraform, Ansible, boto (for dynamic inventory), aws credentials configured properly for the deployment user

Clone this repo to the local machine or any instance. Take the terraform directory as a module and create a main.tf file by providing proper values specific to the aws account. An example for using this terraform script as a template for building aws account specific instance is given below,


module "module_name" {
  
  source             = "../../common/" #/path/to/terraform/directory
  Region	           = "us-west-1"
  ami_id	           = "ami-sample"
  pem_key	           = "/path/to/pem/key"
  compute            = "t2.large"
  key                = "pem_key"
  num_instance       = 1
  app_vpc            = "vpc_id"
  sg                 = "name of security group to be given"
  az                 = ["us-west-1a"]
}

The vairables in the var.tf file present in this repo will be the input to the main.tf to be created.

To run this script aws access key and secret key is required which will be passed at run time due to security reasons. while in the terraform directory, run the following

Validate the script: terraform validate -var 'AccessKey=xxxxxxxxxxxxxxx' -var 'SecretKey=xxxxxxxxxxxxxxxxxxx'

Plan: terraform plan -var 'AccessKey=xxxxxxxxxxxxxxx' -var 'SecretKey=xxxxxxxxxxxxxxxxxxx'

Execution: terraform apply -var 'AccessKey=xxxxxxxxxxxxxxx' -var 'SecretKey=xxxxxxxxxxxxxxxxxxx'

Deployment to Docker container
------------------------------
Clone this repo to your docker machine



docker network create -d bridge mysql-nw
important! as both the containers should be in same nw and resolvable via name as the app config has mysql host running in different container but on the same network

docker pull sanjaymv/flaskapp:3.0 
pull the app from dockerhub or you can build using docker build -t <name>:1.0 .

docker run -d --network=mysql-nw --name flaskapp -p 5005:5000 sanjaymv/flaskapp:3.0 
run the app in the newly created network

 docker run -d --env-file package/mysql_config.env --network=mysql-nw --name mysqldb mysql:5.6
Creates the mysql container in the same network as the app runs with the configuration needed by the app to communicate with mysql

 docker exec -i mysqldb mysql -u sanju -psanju flaskapp < /path/to/py_flask.sql
Restore the dump

Open the required ports in security group in this case, 5005 and access the service on port 5005 from browser. 


Accessing the app
-----------------

http://flask-app-682349944.us-west-2.elb.amazonaws.com/<api end point> 

api end points: /post, /view, /search, /delete



