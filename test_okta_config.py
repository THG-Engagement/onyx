#!/usr/bin/env python3
"""
Test script to verify Okta OIDC configuration and implementation.
This script checks if the OpenID configuration URL is accessible and correctly formatted,
and also verifies that the OIDC implementation is properly set up in the codebase.
"""

import argparse
import json
import os
import sys
import urllib.request
from urllib.error import HTTPError, URLError

def test_openid_config(openid_config_url):
    """Test if the OpenID configuration URL is accessible and correctly formatted."""
    print(f"Testing OpenID configuration URL: {openid_config_url}")
    
    try:
        # Make a request to the OpenID configuration URL
        with urllib.request.urlopen(openid_config_url) as response:
            if response.status != 200:
                print(f"Error: Received status code {response.status}")
                return False
            
            # Parse the JSON response
            config = json.loads(response.read().decode())
            
            # Check for required fields
            required_fields = [
                "issuer", 
                "authorization_endpoint", 
                "token_endpoint", 
                "userinfo_endpoint",
                "jwks_uri"
            ]
            
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"Error: Missing required fields in OpenID configuration: {', '.join(missing_fields)}")
                return False
            
            print("OpenID configuration is valid!")
            print("\nConfiguration details:")
            print(f"  Issuer: {config['issuer']}")
            print(f"  Authorization endpoint: {config['authorization_endpoint']}")
            print(f"  Token endpoint: {config['token_endpoint']}")
            print(f"  UserInfo endpoint: {config['userinfo_endpoint']}")
            
            return True
            
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except URLError as e:
        print(f"URL Error: {e.reason}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return False

def verify_oidc_implementation():
    """Verify that the OIDC implementation is properly set up in the codebase."""
    print("\nVerifying OIDC implementation in the codebase...")
    
    # Check if the necessary files exist
    files_to_check = [
        "backend/onyx/auth/users.py",
        "backend/onyx/main.py",
        "backend/onyx/configs/constants.py"
    ]
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"Error: Required file {file_path} not found")
            return False
    
    # Check if AUTH_TYPE.OIDC is defined in constants.py
    try:
        with open("backend/onyx/configs/constants.py", "r") as f:
            constants_content = f.read()
            if "OIDC = " not in constants_content:
                print("Error: AUTH_TYPE.OIDC is not defined in constants.py")
                return False
    except Exception as e:
        print(f"Error reading constants.py: {str(e)}")
        return False
    
    # Check if OIDC is allowed in verify_auth_setting
    try:
        with open("backend/onyx/auth/users.py", "r") as f:
            users_content = f.read()
            if "AuthType.OIDC" not in users_content or "verify_auth_setting" not in users_content:
                print("Error: OIDC is not allowed in verify_auth_setting function")
                return False
    except Exception as e:
        print(f"Error reading users.py: {str(e)}")
        return False
    
    # Check if OIDC authentication is implemented in main.py
    try:
        with open("backend/onyx/main.py", "r") as f:
            main_content = f.read()
            if "AUTH_TYPE == AuthType.OIDC" not in main_content or "OpenID(" not in main_content:
                print("Error: OIDC authentication is not implemented in main.py")
                return False
    except Exception as e:
        print(f"Error reading main.py: {str(e)}")
        return False
    
    print("OIDC implementation verification successful!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Test Okta OIDC configuration and implementation")
    parser.add_argument("--url", help="OpenID configuration URL")
    parser.add_argument("--skip-implementation-check", action="store_true",
                        help="Skip checking the OIDC implementation in the codebase")
    args = parser.parse_args()
    
    if args.url:
        openid_config_url = args.url
    else:
        # Prompt for the URL if not provided as an argument
        okta_domain = input("Enter your Okta domain (e.g., dev-123456.okta.com): ")
        openid_config_url = f"https://{okta_domain}/.well-known/openid-configuration"
    
    config_success = test_openid_config(openid_config_url)
    
    implementation_success = True
    if not args.skip_implementation_check:
        implementation_success = verify_oidc_implementation()
    
    success = config_success and implementation_success
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()