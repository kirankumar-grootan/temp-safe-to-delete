resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allow_ssh_cidr_blocks
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.allow_http_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "all"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
