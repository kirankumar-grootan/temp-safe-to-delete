### Introduction

This Terraform project provisions AWS EC2 instances, a Network Load Balancer (NLB), and associated security groups. The configuration sets up an NLB and deploys EC2 instances across specified subnets with the defined count.

## Features

- **Scalable EC2 Instances**: Automatically provisions EC2 instances according to the specified configuration.
- **Load Balancing**: Sets up an NLB that dynamically registers EC2 instances with the target group as they are created.
- **Security Groups**: Configures security groups to ensure appropriate access and security for the instances and load balancer.

## Limitations

- **No HTTPS Support**: This setup does not include HTTPS handling for secure communication.
- **Limited Configuration Options**: The load balancer and EC2 instances have minimal customization options in this configuration.
- **Longer Startup Time**: The initial setup time may be longer due to package updates, Nginx installation, and service startup during instance boot. Using pre-built AMIs could help mitigate this.
- **Manual Scaling**: Scaling of instances must be managed manually; automatic scaling is not configured.

## Requirements

- **Terraform**: Ensure Terraform is installed on your system.
- **AWS Access**: Requires access to AWS EC2, SG and Load Balancer services.

### Future Improvements

- **Alternative Language**: Explore using Go with the Bubble Tea library for an interactive CLI interface, which could replace Python and reduce reliance on additional dependencies like `boto3`.
- **Error Handling**: Implement robust error handling to ensure no manual intervention is required, such as cleanups in the AWS Console, if errors occur.
- **Email Attachment Support**: Add functionality for sending email attachments.
- **Enhanced AWS Configuration**: Replace hardcoded values like account IDs and sender email addresses with configurable options that can be set via command-line arguments or configuration files.
- **Improved Logging**: Enhance logging capabilities for better tracking and debugging.
