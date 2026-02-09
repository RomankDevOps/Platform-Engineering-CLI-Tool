import os
import boto3

# 1. Ask Python where it thinks your "Home" is
home = os.path.expanduser('~')
print(f"Python thinks your home folder is: {home}")

# 2. Check if it sees the file
cred_path = os.path.join(home, '.aws', 'credentials')
print(f"Looking for credentials at:      {cred_path}")

if os.path.exists(cred_path):
    print("Found the file?                  YES")
    # Read the first few lines to check format (masking secrets)
    with open(cred_path, 'r') as f:
        print("\n--- File Content Preview ---")
        for line in f.readlines():
            if "key" in line:
                print(line.split('=')[0] + "= *****") # Hide the actual secret
            else:
                print(line.strip())
        print("----------------------------\n")
else:
    print("Found the file?                  NO (Check path above!)")

# 3. Try to connect
print("Attempting to connect to AWS...")
try:
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print(f"SUCCESS! Connected as: {identity['Arn']}")
except Exception as e:
    print(f"CONNECTION FAILED: {e}")