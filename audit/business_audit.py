import json

from scanner.scanner import scanner
from seo.seo_scanner import seo_scanner


class BusinessAudit:

    def audit(self, website):

        scanner_result = scanner.scan(website)

        seo_result = seo_scanner.scan(website)

        report = {

            "scanner": scanner_result,

            "seo": seo_result

        }

        return report

    def to_json(self, website):

        return json.dumps(

            self.audit(website),

            indent=4

        )


business_audit = BusinessAudit()