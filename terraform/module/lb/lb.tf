resource "aws_lb" "app" {
  name               = "test-lb-tf"
  internal           = false
  load_balancer_type = "network"
  subnets            = var.subnets

  enable_deletion_protection = true
}

resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
