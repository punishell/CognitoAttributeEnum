import boto3
from botocore.exceptions import ClientError
import argparse
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Initialize Cognito IDP client and rich console
client = boto3.client('cognito-idp')
console = Console()

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
        console.print(f"[+] {attribute}: Success (Username: {username})", style="bold green")
        return "Success"
    except ClientError as e:
        error_message = str(e)
        if "NotAuthorizedException" in error_message:
            console.print(f"[-] {attribute}: Not authorized", style="bold red")
            return "Not authorized"
        elif "InvalidParameterException" in error_message:
            console.print(f"[-] {attribute}: Invalid parameter", style="bold yellow")
            return "Invalid parameter"
        elif "UsernameExistsException" in error_message:
            console.print(f"[-] {attribute}: User already exists", style="bold magenta")
            return "User already exists"
        else:
            console.print(f"[-] {attribute}: {error_message}", style="bold red")
            return error_message

# Main function
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Determine which attributes to test: from file or default
    if args.attributes:
        attributes_to_test = read_attributes(args.attributes)
        console.print(f"[+] Using attributes from file: {args.attributes}", style="bold blue")
    else:
        attributes_to_test = default_attributes
        console.print("[+] Using default attributes", style="bold blue")

    # Prepare the result table
    table = Table(title="Cognito User Attribute Enumeration Results", box=box.DOUBLE)
    table.add_column("Attribute", style="cyan", no_wrap=True)
    table.add_column("Result", style="magenta")
    table.add_column("Details", style="green")

    # Enumerate possible attributes
    console.print(Panel.fit(f"Testing attributes using client_id: [bold yellow]{args.client_id}[/bold yellow]", box=box.DOUBLE))

    for attribute in attributes_to_test:
        result = test_attribute(args.client_id, attribute)
        table.add_row(attribute, result, f"Username: {generate_username(attribute)}")

    console.print(table)
