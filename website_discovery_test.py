from lead_engine.website_discovery import website_discovery

print("=" * 80)
print("Program Started")
print("=" * 80)

website = website_discovery.discover(
    "PureGym",
    "London"
)

print()
print("Website Found:")
print(website)
print()

print("=" * 80)
print("Program Finished")
print("=" * 80)