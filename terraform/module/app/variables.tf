variable "instances" {
  type = map(object({
    count         = number
    instance_type = string
    subnet_id     = list(string)
    key_name      = string
    volume_size   = number
  }))
}

variable "vpc_id" {
  type = string
}

variable "allow_ssh_cidr_blocks" {
  type = list(string)
}

variable "allow_http_cidr_blocks" {
  type = list(string)
}
