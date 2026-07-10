from website_scanner.seo import scan_seo

result = scan_seo("hubspot.com")

for key, value in result.items():
    print(f"{key}: {value}")