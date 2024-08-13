import boto3
from botocore.exceptions import ClientError
import argparse
import time

# Initialize Cognito IDP client
client = boto3.client('cognito-idp')

# Default list of attributes to test
default_attributes = [
    'email',
    'phone_number',
    'name',
    'given_name',
    'family_name',
    'preferred_username',
    'address',
    'birthdate',
    'gender',
    'locale',
    'middle_name',
    'nickname',
    'picture',
    'profile',
    'updated_at',
    'website',
    'zoneinfo',
]

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Enumerate Cognito user attributes')
    parser.add_argument('-client_id', required=True, help='Cognito User Pool client ID')
    parser.add_argument('-w', '--attributes', help='Path to the file containing list of attributes to test')
    return parser.parse_args()

# Function to read attributes from a text file
def read_attributes(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Function to generate a unique username with timestamp
def generate_username(attribute):
    timestamp = int(time.time())  # Current timestamp in seconds
    return f"testuser_{attribute}_{timestamp}"

# Function to test an attribute with a unique username
def test_attribute(client_id, attribute):
    username = generate_username(attribute)
    try:
        # Attempt to sign up using the attribute
        response = client.sign_up(
            ClientId=client_id,
            Username=username,
            Password='Password12!',  # Use a strong password that meets Cognito's requirements
            UserAttributes=[
                {'Name': attribute, 'Value': 'TestValue'},
                {'Name': 'email', 'Value': f'test_{attribute}@example.com'}  # Required email attribute
            ]
        )
        print(f"[+] {attribute}: Success (Username: {username})")
    except ClientError as e:
        error_message = str(e)
        if "NotAuthorizedException" in error_message:
            print(f"[-] {attribute}: Not authorized")
        elif "InvalidParameterException" in error_message:
            print(f"[-] {attribute}: Invalid parameter")
        elif "UsernameExistsException" in error_message:
            print(f"[-] {attribute}: User already exists")
        else:
            print(f"[-] {attribute}: {error_message}")

# Main function
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Determine which attributes to test: from file or default
    if args.attributes:
        attributes_to_test = read_attributes(args.attributes)
        print(f"Using attributes from file: {args.attributes}")
    else:
        attributes_to_test = default_attributes
        print("Using default attributes")

    # Enumerate possible attributes
    print(f"Testing attributes using client_id: {args.client_id}")
    for attribute in attributes_to_test:
        test_attribute(args.client_id, attribute)

