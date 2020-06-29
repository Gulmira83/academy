variable "mysql_user" {
  default = "academyuser"
}

variable "mysql_database" {
  default = "academydb"
}

variable "mysql_password" {
  default = "ZXKXYP1QN25BBkUbLjJ5V"
}

variable "mysql_root_password" {
  default = "ZXKXYP1QN25BBkUbLjJ5V"
}

variable "admin_user" {
  default = "academyadmin"
}

variable "admin_password" {
  default = "vKnqbgSh0qS7dpZy%S6"
}

variable "whitelisted_cidrs" {
  type = "map"
  default = {
    prod = "0.0.0.0/0"
    qa   = "10.16.0.27/8, 50.194.68.229/32, 50.194.68.230/32, 24.12.115.204/32"
    dev  = "10.16.0.27/8, 50.194.68.229/32, 50.194.68.230/32, 24.12.115.204/32"
    test = "0.0.0.0/0"
  }
}

variable "deployment_environment" {
  default = "dev"
}

variable "deployment_endpoint" {
  type = "map"

  default = {
    test  = "test.academy"
    dev  = "dev.academy"
    qa   = "qa.academy"
    prod = "academy"
    stage = "stage.academy"
  }
}

variable "google_domain_name" {
  default = "fuchicorp.com"
}

variable "mysql_host" {
  default = "Please-change-this-value-to-correct-data"
}

variable "academy_service_account" {
  default = "fuchicorp-api"
}

## organization github token
variable "github_token" {
  default = "Please-change-this-value-to-correct-data"
}

## organization's auth applciation id
variable "github_client_id" {
  type = "map"

  default = {
    test  = "Please-change-this-value-to-correct-data"
    dev  = "Please-change-this-value-to-correct-data"
    qa   = "Please-change-this-value-to-correct-data"
    prod = "Please-change-this-value-to-correct-data"
  }
}

## organization's auth applciation secret
variable "github_client_secret" {
  type = "map"

  default = {
    test  = "Please-change-this-value-to-correct-data"
    dev  = "Please-change-this-value-to-correct-data"
    qa   = "Please-change-this-value-to-correct-data"
    prod = "Please-change-this-value-to-correct-data"
  }
}

variable "application_secret" {
  default = "application_secret"
}

variable "deployment_image" {
  default = "docker.fuchicorp.com/academy-dev:0.3"
}

variable "lets_encrypt_email" {
  default = "fuchicorpsolutions@gmail.com"
}

variable "academy_secret" {
  default = "WELCOME2019"
}

variable "vimeo_client_id" {
}

variable "vimeo_access_token" {
}

variable "vimeo_client_secret" {  
}
