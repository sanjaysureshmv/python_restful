provider "aws" {
  access_key = "${var.AccessKey}"
  secret_key = "${var.SecretKey}"
  region     = "${var.Region}"
}

resource "aws_instance" "PyApp" {
  ami             = "${var.ami_id}"
  instance_type   = "${var.compute}"
  key_name        = "${var.key}"
  count           = "${var.num_instances}"
  security_groups = ["${aws_security_group.my_sg.name}"]

  root_block_device {
    delete_on_termination = true
    volume_size           = 8
  }

  tags {
    Name = "Flask"
  }

  #user_data = "${file("python.sh")}"

  connection = {
    type        = "ssh"
    user        = "ubuntu"
    host        = "${self.public_ip}"
    private_key = "${file("~/Ubuntu16.04_backup/sanjaym_home/Downloads/devops.pem")}"# make as variable
  }

   provisioner "remote-exec" {
    inline = ["sudo apt-get -y install python-minimal"]

   }


  provisioner "local-exec" {
    command = "sleep=300; ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ec2.py -e hosts=tag_Name_${aws_instance.PyApp.tags.Name} -u ubuntu --private-key ../Ubuntu16.04_backup/sanjaym_home/Downloads/devops.pem  main.yaml"
  }
}


resource "aws_security_group" "my_sg" {
  name   = "${var.sg}"
  vpc_id = "${var.app_vpc}"

  ingress {
    from_port   = "5000"
    to_port     = "5000"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_elb" "elb" {
  name               = "flask-app"
  availability_zones = "${var.az}"

  listener {
    instance_port     = 5000
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    target              = "HTTP:5000/search"
    interval            = 10
  }

  instances                   = ["${aws_instance.PyApp.id}"]
  idle_timeout                = 300
  connection_draining         = true
  connection_draining_timeout = 300

  tags {
    Name = "flask-elb"
  }
}


