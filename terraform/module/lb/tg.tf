resource "aws_lb_target_group" "app" {
  name = "app-tg"

  vpc_id = var.vpc_id

  load_balancing_algorithm_type = "round_robin"
  connection_termination = true
  preserve_client_ip = true
  target_type = "instance"

  port = 80
  protocol = "HTTP"
  protocol_version = "HTTP2"

  deregistration_delay = 15

  health_check {
    enabled = true
    healthy_threshold = 3
    unhealthy_threshold = 3
    path = "/"
    port = 80
    protocol = "HTTP"
    timeout = 5
    interval = 10
  }
}

resource "aws_lb_target_group_attachment" "app" {
  for_each = toset(var.instance_ids)

  target_group_arn = aws_lb_target_group.app.arn
  target_id        = each.value
  port             = 80
}
