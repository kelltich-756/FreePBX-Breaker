![FreePBX-Breaker](FreePBX.png)
## General Overview
This repository contains the Proof of Concept (PoC) and the detailed methodology
required to exploit the CVE-2025-57819 vulnerability in FreePBX installations,
specifically designed for the Connected machine in HackTheBox.

This vulnerability allows an attacker to gain elevated access or execute
arbitrary commands on the underlying operating system (Asterisk/FreePBX) by
manipulating input parameters, resulting in a Remote Code Execution (RCE).

- **Affected System:** FreePBX
- **Vulnerability ID:** CVE-2025-57819
- **Impact:** Critical ($\text{Remote Code Execution} \rightarrow$ Total System Compromise).

## What is the Exploit? (Vulnerability Concept)
### What is CVE-2025-57819?
The vulnerability resides in the [Specify Module/Component, e.g., Dialplan Manager, AMI Listener, or API Gateway] within the FreePBX framework. The flaw is found in how the system sanitizes user input while processing specific functions (such as adding extensions, configuring trunks, or running custom scripts).

### Failure Mechanism (The "How")
- **Attack Vector:** The attacker directs their assault toward a specific parameter (e.g., `extension_name`, `ivr_command`, or an API parameter).
- **Payload Construction:** Instead of providing a valid value, the attacker injects special shell characters (such as `;`, `|`, `&&`, `$()`).
- **Execution Flow:** The vulnerable code executes the input string directly through a system shell (using functions like `system()` in C/C++ or `subprocess.run()` in Python). The shell parser interprets the injected characters, allowing the attacker to chain malicious commands after or instead of the original command.
- **Goal:** The attacker uses this chain to execute commands like `whoami`, `cat /etc/shadow`, or download backdoors.

## How to Use the Exploit? (Step-by-Step Guide)
This repository provides a Python script (`freepbx-breaker.py`) to automate the attack process.

### Prerequisites
- **Python 3:** Must be installed on your attacking machine.
- **Requests Library:** Must be installed (`pip install requests`).
- **Target Details:** You need the specific IP address and port of the FreePBX service you are attacking on the Connected machine.

## Installation

```bash
git clone https://github.com/kelltich-756/FreePBX-Breaker.git
cd FreePBX-Breaker
pip install requests
chmod +x flar3ad
```

### Execution Steps

**Step 1: Target Identification**
For the HackTheBox Connected machine, confirm the point of entry for the vulnerable point (Is it the web UI? Is it the AMI port? Is it a REST API?).

*   **Target IP:** `[IP_OF_CONNECTED_MACHINE]`
*   **Vulnerable Endpoint:** `[URL_OF_VULNERABLE_ENDPOINT]`

**Step 2: Payload Configuration**
You must adjust the variables within the `freepbx-breaker.py` file:

*   **`TARGET_URL`:** Set the complete URL of the attack point.
*   **`MALICIOUS_PAYLOAD`:** This is the key component.
    *   If the attack is RCE: Define the `"command"` field with the shell command you wish to execute (e.g., `"id"`, `"cat /etc/passwd"`).
    *   If it is another type of injection: Modify the structure of this dictionary to match the data model of the affected endpoint.

**Step 3: Execution**
Run the script from your terminal:
```bash
python3 exploit.py
```
## Authors

- [@Keltich](https://github.com/kelltich-756)
