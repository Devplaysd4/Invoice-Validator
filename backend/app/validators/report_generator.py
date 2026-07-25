def generate_validation_report(invoices):

    report = {
        "summary": {
            "total_invoices": len(invoices),
            "valid_invoices": 0,
            "invalid_invoices": 0,
            "success_rate": 0
        },
        "failed_invoices": [],
        "statistics": {
            "total_amount": 0,
            "average_amount": 0,
            "highest_amount": 0,
            "lowest_amount": None
        }
    }

    amounts = []

    for invoice in invoices:

        amount = invoice.get("amount")

        if isinstance(amount, (int, float)):
            amounts.append(amount)

        if invoice["status"] == "VALID":
            report["summary"]["valid_invoices"] += 1
        else:
            report["summary"]["invalid_invoices"] += 1

            report["failed_invoices"].append({

                "invoice_number": invoice["invoice_number"],

                "vendor": invoice["vendor"],

                "errors": invoice["validation_errors"]

            })

    if amounts:

        report["statistics"]["total_amount"] = round(sum(amounts),2)
        report["statistics"]["average_amount"] = round(sum(amounts)/len(amounts),2)
        report["statistics"]["highest_amount"] = max(amounts)
        report["statistics"]["lowest_amount"] = min(amounts)

    total = report["summary"]["total_invoices"]

    if total:

        report["summary"]["success_rate"] = round(
            report["summary"]["valid_invoices"]*100/total,
            2
        )

    return report