output "instance_private_ip" {
  value = "${aws_instance.PyApp.*.private_ip}"
}
output "elb_endpoint" {
  value = "${aws_elb.elb.dns_name}"
}
