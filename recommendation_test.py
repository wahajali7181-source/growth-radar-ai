from audit.business_audit import business_audit

from ai_engine.score_engine import score_engine

from ai_engine.recommendation_engine import recommendation_engine


website = "https://puregym.com"

audit = business_audit.audit(website)

score = score_engine.calculate(

    audit["scanner"],

    audit["seo"]

)

result = recommendation_engine.generate(

    audit["scanner"],

    audit["seo"],

    score

)

print()

print(result)