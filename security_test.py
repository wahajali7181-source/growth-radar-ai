from website_scanner.security import scan_security

result = scan_security("hubspot.com")

for key, value in result.items():
    print(f"{key}: {value}")