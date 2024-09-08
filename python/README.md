### Introduction

This Python script facilitates the creation of IAM users, including password reset and MFA management permissions. It also handles the generation of initial passwords and sends instructions for MFA registration and password reset via email.

### Features

- **Random Password Generation**: Automatically generates a random password for new users.
- **Email Notification**: Sends an email using Amazon SES with an attachment containing instructions for MFA registration and password reset.
- **User Creation Rollback**: Deletes the IAM user if the email sending process fails.

### Requirements

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Dependencies**: Install `boto3` and `botocore` libraries using `pip`:
  ```bash
  pip install boto3 botocore
  ```
- **Attachment**: The attachment containing the MFA and password reset instructions must be in the same directory as the Python script.

### Instructions

**Preparation**:
1. Configure boto client `https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html`
2. Change the value in `iam.py` file with all the place holders `change me`

**Run the Script**: Execute the script with the user’s email as an argument:
```bash
# email will be same as username. fails if email is not valid.
python iam.py --username user@example.com

python iam.py --username user --email user@example.com
```

### Future Improvements

- **Alternative Language**: Consider using Go with the Bubble Tea library for an interactive CLI interface, eliminating the need for Python and additional manual dependencies like `boto3`.
- **Error Handling**: Need to perform good error handling in a way no need to perform any manual task like cleanups in AWS Console if anything gone wrong
- **Email Attachment**: Support for email attachment
- **More Configurable AWS Options**: Remove hardcoded accountid, sender email etc to have a default and make it configurable via args
- **Better Logging**: Have better logging
