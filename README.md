# Cognito User Attribute Enumeration Tool

This Python script allows you to enumerate the possible user attributes that can be used during the sign-up process in an Amazon Cognito User Pool. It generates unique usernames by appending the current timestamp to ensure that each test is isolated and avoids conflicts with existing users.

## Features

- **Command-Line Interface**: Easily specify the Cognito User Pool client ID and a wordlist of attributes to test.
- **Default Attribute List**: If no wordlist is provided, the tool uses a predefined list of common Cognito attributes.
- **Unique Usernames**: Each test run generates a unique username by appending the current timestamp to the attribute being tested.
- **Error Handling**: The script handles various exceptions and provides clear feedback for each tested attribute.

## Prerequisites

- Python 3.x
- AWS CLI configured with appropriate credentials and permissions
- Boto3 library installed

## Installation

1. **Clone the repository** (if applicable):

   ```bash
   git clone https://github.com/your-repo/cognito-attribute-enumeration.git
   cd cognito-attribute-enumeration
   ```
