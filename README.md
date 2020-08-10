# nami-apple-receip-validator

A simple Python 3 CLI for validating an App Store Receipt via Apple's verifyReceipt service.


### Production

```
./apple_receipt_validator.py  /path/to/base64_encoded_receipt
```

### Sandbox


```
./apple_receipt_validator.py  /path/to/base64_encoded_receipt --use_sandbox
```

### Specify an App Store Shared Secret

This is necessary to receive responses for receipts containing auto-renewnable subscriptions


```
./apple_receipt_validator.py  /path/to/base64_encoded_receipt -s your_app_shared_secret
```
