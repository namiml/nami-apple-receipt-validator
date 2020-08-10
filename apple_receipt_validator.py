#!/usr/bin/python3

import sys
import getopt
import json
import urllib3

VERIFY_RECEIPT_SANDBOX = "https://sandbox.itunes.apple.com/verifyReceipt"
VERIFY_RECEIPT_PROD = "https://buy.itunes.apple.com/verifyReceipt"

def verify_receipt(encoded_receipt, shared_secret, use_sandbox):
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
        if status == 0:
            print(f"🎉 Receipt is valid (status {status})")
        else:
            print(f"👎 Unable to validate receipt (status {status})")
    else:
        print(f"💣 Error: {response.status}")


if __name__ == "__main__":
    help_message = "apple_receipt_validator.py  [receipt_file] <OPTIONAL: -s [appstore_shared_secret] --use_sandbox>"

    if len(sys.argv) < 2:
        print(help_message)
        sys.exit(2)

    with open(sys.argv[1], "r") as f:
        receipt_data = f.read().splitlines()[0]

    shared_secret = None
    use_sandbox = False

    try:
        opts, args = getopt.getopt(sys.argv[2:],"s:", ["secret=", "use_sandbox"])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--use_sandbox"):
            use_sandbox = True
        if opt in ("-s", "--secret"):
            shared_secret = arg

    verify_receipt(receipt_data, shared_secret, use_sandbox)
