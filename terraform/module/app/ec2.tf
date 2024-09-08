data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

locals {
  # Generates a flattened list of maps, each representing an instance-subnet combination.
  # Each map includes details for a specific instance and its associated subnet from the 'instances' variable.
  instance_subnet_combinations = flatten([
    for instance_key, instance in var.instances : [
      for subnet_index, subnet_id in instance.subnet_id : [
        for i in range(instance.count) : {
          instance_key  = instance_key
          instance_type = instance.instance_type
          subnet_id     = subnet_id
          key_name      = instance.key_name
          volume_size   = instance.volume_size
          subnet_index  = subnet_index
          count_index   = i
        }
      ]
    ]
  ])
}

resource "aws_instance" "app" {
  # Iterating over the local.instance_subnet_combinations list.
  # 'idx' represents the index of each combination, and 'val' contains the object with instance and subnet details.
  # The for_each expression creates a map where 'idx' is the unique key, and 'val' is the instance-subnet combination.
  for_each = { for idx, val in local.instance_subnet_combinations : idx => val }

  ami           = data.aws_ami.ubuntu.id
  instance_type = each.value.instance_type
  subnet_id     = each.value.subnet_id
  key_name      = each.value.key_name

  root_block_device {
    encrypted   = true
    volume_type = "gp3"
    volume_size = each.value.volume_size
  }

  user_data = file("${path.module}/app.sh")

  tags = {
    Name = "app-${each.value.instance_key}-${each.value.count_index}"
  }
}
