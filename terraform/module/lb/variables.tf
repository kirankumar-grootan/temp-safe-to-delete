variable "vpc_id" {
  type = string
}

variable "subnets" {
  type = list(string)
}

variable "instance_ids" {
  type = list(string)
}