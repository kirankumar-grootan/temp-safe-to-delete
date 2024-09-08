terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.66.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"

  default_tags {
    tags = {
      App = "test"
      Environment = "dev"
    }
  }
}

module "instance" {
  source = "./module/app"

  vpc_id = "" # Change me
  allow_ssh_cidr_blocks = ["0.0.0.0/0"] # Change me if required
  allow_http_cidr_blocks = ["0.0.0.0/0"] # Change me to public subnet cidr range if required

  instances = {
    instance1 = {
      count         = 1
      instance_type = "t3a.micro"
      subnet_id     = ["subnet-abc123", "subnet-def456"]
      key_name      = "default"
      volume_size   = 8
    },
    instance2 = {
      count         = 2
      instance_type = "t3a.large"
      subnet_id     = ["subnet-abc123", "subnet-def456"]
      key_name      = "default"
      volume_size   = 8
    }
  }
}

module "lb" {
  source = "./module/lb"

  vpc_id = "" # Change me
  subnets = ["subnet-abc123", "subnet-def456"] # Change me
  instance_ids = module.instance.instance_ids
}
