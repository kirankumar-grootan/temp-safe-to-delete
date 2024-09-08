import boto3
import string
import random
import argparse
import json
import os
import re

from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

iam_client = boto3.client('iam')
ses_client = boto3.client('ses')

policy_arn = ""

def __generate_password():
  alphabet = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(random.choices(alphabet, k=12))
  return password

def create_iam_user(username) -> bool:
  try:
    iam_client.create_user(
      UserName=username
    )
    print(f'User {username} created successfully.')
  except Exception as e:
    print(f'Error creating user: {e}')
    return False

  return True

def create_login_profile(username, password) -> bool:
  try:
    iam_client.create_login_profile(
      UserName=username,
      Password=password,
      PasswordResetRequired=True
    )
    print(f'Login profile created for user {username}')
    # print(f'Generated password: {password}')
  except Exception as e:
    print(f'Error creating login profile: {e}')

    return False

  return True

def is_valid_email(email) -> string:
  reg_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
  return re.match(reg_pattern, email)

def create_policy(username) -> bool:
  policy_document = {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "VisualEditor0",
        "Effect": "Allow",
        "Action": [
          "iam:DeactivateMFADevice",
          "iam:GetMFADevice",
          "iam:DeleteVirtualMFADevice",
          "iam:EnableMFADevice",
          "iam:ResyncMFADevice",
          "iam:UntagMFADevice",
          "iam:TagMFADevice",
          "iam:CreateVirtualMFADevice",
          "iam:ListMFADevices",
          "iam:ListMFADeviceTags",
          "iam:ChangePassword"
        ],
        "Resource": [
          "arn:aws:iam::${aws:userid}:mfa/*",
          "arn:aws:iam::${aws:userid}:sms-mfa/*",
          "arn:aws:iam::${aws:userid}:user/${aws:username}"
        ]
      },
      {
        "Sid": "VisualEditor1",
        "Effect": "Allow",
        "Action": "iam:ListVirtualMFADevices",
        "Resource": "*"
      },
      # https://repost.aws/knowledge-center/mfa-iam-user-aws-cli
      {
        "Sid": "BlockMostAccessUnlessSignedInWithMFA",
        "Effect": "Deny",
        "NotAction": [
          "iam:CreateVirtualMFADevice",
          "iam:DeleteVirtualMFADevice",
          "iam:ListVirtualMFADevices",
          "iam:EnableMFADevice",
          "iam:ResyncMFADevice",
          "iam:ListAccountAliases",
          "iam:ListUsers",
          "iam:ListSSHPublicKeys",
          "iam:ListAccessKeys",
          "iam:ListServiceSpecificCredentials",
          "iam:ListMFADevices",
          "iam:GetAccountSummary",
          "sts:GetSessionToken"
        ],
        "Resource": "*",
        "Condition": {
          "Bool": {
            "aws:MultiFactorAuthPresent": "false",
            "aws:ViaAWSService": "false"
          }
        }
      }
    ]
  }

  try:
    response = iam_client.create_policy(
      PolicyName=username,
      PolicyDocument=json.dumps(policy_document)
    )

    policy_arn = response['Policy']['Arn']
    print(f'Policy created with ARN: {policy_arn}')
  except Exception as e:
    print(f'Error creating policy: {e}')
    return False

  try:
    iam_client.attach_user_policy(
      UserName=username,
      PolicyArn=policy_arn
    )

    print(f'Policy attached to user {username}')
  except Exception as e:
    iam_client.delete_policy(
      PolicyArn=policy_arn
    )
    print(f'Error attaching policy: {e}')
    return False

  return True

def send_email(recipient, account_id, policy_arn, username, password):
  sender="admin@test.com" # change me
  subject='AWS Account'
  body_text=f"""
  Hi,

  AWS login create

  Console: https://{account_id}.signin.aws.amazon.com/console
  Username: {username}
  Password: {password}

  Without enabling MFA you will not be able to perform any actions.

  Thanks,
  AWS Admin
  """

  try:
    response = ses_client.send_email(
      Source=sender,
      Destination={
        'ToAddresses': [recipient],
      },
      Message={
        'Subject': {
          'Data': subject,
        },
        'Body': {
          'Text': {
            'Data': body_text,
          }
        }
      }
    )
  except ClientError as e:
    print(f"Error sending email: {e}")
    iam_client.delete_user(
      UserName=username
    )
    iam_client.delete_policy(
      PolicyArn=policy_arn
    )
  else:
    print(f"Email sent! Message ID: {response}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Create IAM user')
  parser.add_argument('--username', type=str, help='The username for the new IAM user.')
  parser.add_argument('--email', type=str, help='The email for the new IAM user.', default="")

  account_id = "1234567890" # change me

  args = parser.parse_args()

  if args.email and not args.username:
    raise ValueError("invalid options")

  username = args.username or args.email
  email = args.email or args.username

  if not is_valid_email(email):
    raise ValueError(f"Invalid email format: {email}")

  print(f"Creating IAM user with username: {username} and email: {email}")

  password = __generate_password()

  if create_iam_user(username):
    if create_login_profile(username, password):
      if create_policy(username):
        # 1234567890 - Account ID used only on email console login string formation
        send_email(email, account_id, policy_arn, username, password)
