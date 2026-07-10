from social_checker.checker import check_socials

result = check_socials("hubspot.com")

for key, value in result.items():
    print(f"{key}: {value}")