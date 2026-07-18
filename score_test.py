from audit.business_audit import business_audit
from ai_engine.score_engine import score_engine

website = "https://puregym.com"

audit = business_audit.audit(website)

score = score_engine.calculate(

    audit["scanner"],

    audit["seo"]

)

print()

print("Business Score:", score)