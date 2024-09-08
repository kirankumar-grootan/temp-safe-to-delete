output "instance_ids" {
  description = "List of EC2 instance IDs"
  value       = [for instance in aws_instance.app : instance.id]
}
