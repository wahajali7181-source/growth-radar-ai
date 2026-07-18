from scanner.scanner import scanner

website = "https://puregym.com"

result = scanner.scan(
    website
)

print()

for key, value in result.items():

    print(key, ":", value)