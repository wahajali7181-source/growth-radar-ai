from lead_engine.detectors.technology_detector import detect_technology

result = detect_technology(
    "https://wordpress.org"
)

print(result)