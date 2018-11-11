variable "SecretKey" {}
variable "AccessKey" {}



variable "Region" {
    default = "us-west-2"
}

variable "ami_id" {
    default = "ami-0e32ec5bc225539f5"
  
}
 variable "pem_key"{
     default = "/home/sanjay/Ubuntu16.04_backup/sanjaym_home/Downloads/devops.pem"
 }
variable "compute" {
  default = "t2.micro"
}

variable "key" {
  default = "devops"
}

variable "num_instances" {
    default = 1
}

variable "sg" {
    default = "flask_sg"
  
}

variable "app_vpc" {
    default = "vpc-9bfac7e2"
  
}

variable "az" {

    default = ["us-west-2a"]
  
}







