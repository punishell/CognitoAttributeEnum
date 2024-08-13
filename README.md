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

1. **Clone the repository** 

   ```bash
   git clone https://github.com/punishell/CognitoAttributeEnum.git
   cd cognito-attribute-enumeration
   ```

## Usage

```
$ python cognito-attribute-enu.py -client_id 16f1g98bfuj9i0g3f8be36kkrl 
Using default attributes
Testing attributes using client_id: 16f1g98bfuj9i0g3f8be36kkrl
[+] email: Success (Username: testuser_email_1723574859)
[-] phone_number: Not authorized
[+] name: Success (Username: testuser_name_1723574860)
[-] given_name: Not authorized
[-] family_name: Not authorized
[-] preferred_username: Not authorized
[-] address: Not authorized
[-] birthdate: Not authorized
[-] gender: Not authorized
[-] locale: Not authorized
[-] middle_name: Not authorized
[-] nickname: Not authorized
[-] picture: Not authorized
[-] profile: Not authorized
[-] updated_at: Not authorized
[-] website: Not authorized
[-] zoneinfo: Not authorized
```
