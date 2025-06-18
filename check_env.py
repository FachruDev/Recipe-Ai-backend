#!/usr/bin/env python
"""
Helper script for checking environment variables in Heroku.
Run this with: heroku run python check_env.py --app your-app-name
"""

import os
import sys

def main():
    print(f"Python version: {sys.version}")
    print("\nEnvironment Variables:")
    
    # Check critical variables
    critical_vars = [
        "OPENROUTER_API_KEY", 
        "DATABASE_URL", 
        "CORS_ORIGINS"
    ]
    
    for var in critical_vars:
        value = os.environ.get(var)
        if var.lower().find("key") >= 0 and value:
            # Don't print full API keys
            print(f"✓ {var}: {'*' * (len(value) - 4)}{value[-4:]}")
        else:
            print(f"{'✓' if value else '✗'} {var}: {value if value else 'NOT SET'}")
    
    # Check all other environment variables
    print("\nAll Environment Variables (excluding sensitive ones):")
    for key, value in os.environ.items():
        if key not in critical_vars:
            # Don't print sensitive values
            if key.lower().find("key") >= 0 or key.lower().find("password") >= 0 or key.lower().find("secret") >= 0:
                print(f"  {key}: {'*' * (len(value) - 4)}{value[-4:] if value else ''}")
            else:
                print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 