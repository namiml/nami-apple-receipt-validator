#!/usr/bin/python3

import sys
import getopt
import json
import urllib3

VERIFY_RECEIPT_SANDBOX = "https://sandbox.itunes.apple.com/verifyReceipt"
VERIFY_RECEIPT_PROD = "https://buy.itunes.apple.com/verifyReceipt"

VERIFY_RECEIPT_STATUS = {}
VERIFY_RECEIPT_STATUS[0] = "🎉 Receipt is valid"
VERIFY_RECEIPT_STATUS[21002] = "💣 The encoded receipt is malformed"
VERIFY_RECEIPT_STATUS[21004] = "🔐The shared secret does not match what's on file with Apple"
VERIFY_RECEIPT_STATUS[21007] = "🔬 The receipt is from Sandbox. Add --use_sandbox"
VERIFY_RECEIPT_STATUS[21008] = "🖥 The receipt is from Production. Remove --use_sandbox"

def verify_receipt(encoded_receipt, shared_secret, use_sandbox, show_response):
    if use_sandbox:
        url = VERIFY_RECEIPT_SANDBOX
    else:
        url = VERIFY_RECEIPT_PROD

    requestBody = {}
    requestBody["receipt-data"] = encoded_receipt

    if shared_secret:
        requestBody["password"] = shared_secret

    http = urllib3.PoolManager()
    response = http.request("POST",
                            url,
                            headers={"content-type": "application/json"},
                            body=json.dumps(requestBody).encode("utf-8")
                           )

    if response.status == 200:
        responseBody = json.loads(response.data)
        status = responseBody.get("status")

        if status in VERIFY_RECEIPT_STATUS:
            print(f"{VERIFY_RECEIPT_STATUS[status]} (status {status})")
            if status == 0 and show_response:
                print(responseBody)
        else:
            print(f"👎 Unable to validate receipt (status {status})")

    else:
        print(f"💣 Error: {response.status}")


if __name__ == "__main__":
    help_message = "apple_receipt_validator.py  [receipt_file] <OPTIONAL: -s [appstore_shared_secret] --use_sandbox --quiet>"

    if len(sys.argv) < 2:
        print(help_message)
        sys.exit(2)

    with open(sys.argv[1], "r") as f:
        receipt_data = f.read().splitlines()[0]

    shared_secret = None
    use_sandbox = False
    show_response = True

    try:
        opts, args = getopt.getopt(sys.argv[2:],"s:", ["secret=", "use_sandbox", "quiet"])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--use_sandbox"):
            use_sandbox = True
        if opt in ("-s", "--secret"):
            shared_secret = arg
        if opt in ("--quiet"):
            show_response = False

    verify_receipt(receipt_data, shared_secret, use_sandbox, show_response)
