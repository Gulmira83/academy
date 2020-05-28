output "application_deployed" {
  value = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
}
output "whitelisted_ranges" {
  value = "${lookup(var.whitelisted_cidrs, "${var.deployment_environment}")}" 
}
