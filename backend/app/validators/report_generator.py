def generate_validation_report(invoices):

    total = len(invoices)

    valid = 0
    invalid = 0

    failed_invoices = []

    for invoice in invoices:

        if invoice["status"] == "VALID":
            valid += 1
            continue

        invalid += 1

        failed_invoices.append({

            "invoice_number": invoice.get("invoice_number"),

            "vendor": invoice.get("vendor"),

            "issues": invoice["validation_errors"]

        })

    success_rate = round(
        (valid / total) * 100,
        2
    ) if total else 0

    return {

        "summary":{

            "total_invoices": total,

            "valid_invoices": valid,

            "invalid_invoices": invalid,

            "success_rate": f"{success_rate}%"

        },

        "failed_invoices": failed_invoices

    }
    