from audit.business_audit import business_audit

website = "https://puregym.com"

result = business_audit.audit(
    website
)

print(result)