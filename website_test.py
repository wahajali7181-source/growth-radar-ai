from website_scanner.scanner import scan_website

result = scan_website("hubspot.com")

for key, value in result.items():
    print(f"{key}: {value}")