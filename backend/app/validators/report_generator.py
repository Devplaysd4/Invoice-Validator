from collections import Counter


def generate_validation_report(invoices):

    total = len(invoices)

    valid = [
        invoice
        for invoice in invoices
        if invoice["status"] == "VALID"
    ]

    invalid = [
        invoice
        for invoice in invoices
        if invoice["status"] == "INVALID"
    ]

    success_rate = round(
        (len(valid) / total) * 100,
        2
    ) if total else 0

    # ----------------------------------
    # Financial Statistics (VALID only)
    # ----------------------------------

    amounts = [
        float(invoice["amount"])
        for invoice in valid
        if invoice.get("amount") is not None
    ]

    if amounts:

        total_amount = round(sum(amounts), 2)

        average_amount = round(
            total_amount / len(amounts),
            2
        )

        highest_amount = max(amounts)

        lowest_amount = min(amounts)

    else:

        total_amount = 0
        average_amount = 0
        highest_amount = 0
        lowest_amount = 0

    # ----------------------------------
    # GST / Charges / Discount Summary
    # ----------------------------------

    gst_summary = {

        "total_cgst": round(
            sum(float(i.get("cgst", 0) or 0) for i in invoices),
            2
        ),

        "total_sgst": round(
            sum(float(i.get("sgst", 0) or 0) for i in invoices),
            2
        )

    }

    discount_summary = {

        "total_discount": round(
            sum(float(i.get("discount", 0) or 0) for i in invoices),
            2
        )

    }

    charges_summary = {

        "fixed_rent_total": round(
            sum(float(i.get("fixed_rent", 0) or 0) for i in invoices),
            2
        ),

        "call_usage_total": round(
            sum(float(i.get("call_usage", 0) or 0) for i in invoices),
            2
        ),

        "adjustments_total": round(
            sum(float(i.get("adjustments", 0) or 0) for i in invoices),
            2
        )

    }

    # ----------------------------------
    # Invoice Total Verification
    # ----------------------------------

    financial_validation = {

        "checked": 0,

        "passed": 0,

        "failed": 0,

        "failed_invoices": []

    }

    for invoice in invoices:

        if invoice.get("fixed_rent") is None:
            continue

        financial_validation["checked"] += 1

        expected = (

            float(invoice.get("fixed_rent", 0))
            + float(invoice.get("call_usage", 0))
            + float(invoice.get("adjustments", 0))
            + float(invoice.get("cgst", 0))
            + float(invoice.get("sgst", 0))
            + float(invoice.get("discount", 0))

        )

        actual = float(invoice.get("amount", 0))

        if abs(expected - actual) <= 1:

            financial_validation["passed"] += 1

        else:

            financial_validation["failed"] += 1

            financial_validation["failed_invoices"].append({

                "invoice_number": invoice.get("invoice_number"),

                "expected_total": round(expected, 2),

                "actual_total": actual,

                "difference": round(actual - expected, 2)

            })

    # ----------------------------------
    # Error Breakdown
    # ----------------------------------

    error_counter = Counter()

    failed_invoices = []

    for invoice in invalid:

        current_errors = []

        for error in invoice["validation_errors"]:

            if isinstance(error, dict):

                name = error["problem"]

            else:

                name = error

            error_counter[name] += 1

            current_errors.append(error)

        failed_invoices.append({

            "invoice_number": invoice["invoice_number"],

            "vendor": invoice["vendor"],

            "errors": current_errors

        })

    # ----------------------------------
    # Duplicate Count
    # ----------------------------------

    duplicate_count = 0

    seen = set()

    for invoice in invoices:

        number = invoice.get("invoice_number")

        if not number:
            continue

        if number in seen:

            duplicate_count += 1

        else:

            seen.add(number)

    # ----------------------------------
    # Recommendations
    # ----------------------------------

    recommendations = []

    if error_counter["Missing invoice number"]:

        recommendations.append(
            "Provide invoice numbers for all invoices."
        )

    if error_counter["Vendor is missing"]:

        recommendations.append(
            "Fill missing vendor names."
        )

    if error_counter["Invoice Date is missing"]:

        recommendations.append(
            "Provide invoice dates."
        )

    if error_counter["Invoice Date cannot be in the future"]:

        recommendations.append(
            "Correct future invoice dates."
        )

    if error_counter["Amount is missing"]:

        recommendations.append(
            "Fill missing invoice amounts."
        )

    if error_counter["Amount must be greater than zero"]:

        recommendations.append(
            "Invoice amount must be greater than zero."
        )

    if duplicate_count:

        recommendations.append(
            "Remove duplicate invoice numbers."
        )

    if financial_validation["failed"]:

        recommendations.append(
            "Some invoices have incorrect GST/charges/discount calculations."
        )

    # ----------------------------------
    # Final Report
    # ----------------------------------

    return {

        "summary": {

            "total_invoices": total,

            "valid_invoices": len(valid),

            "invalid_invoices": len(invalid),

            "success_rate": f"{success_rate}%"

        },

        "financial_summary": {

            "total_amount": total_amount,

            "average_amount": average_amount,

            "highest_amount": highest_amount,

            "lowest_amount": lowest_amount

        },

        "gst_summary": gst_summary,

        "discount_summary": discount_summary,

        "charges_summary": charges_summary,

        "financial_validation": financial_validation,

        "error_breakdown": dict(error_counter),

        "duplicates": {

            "duplicate_count": duplicate_count

        },

        "failed_invoices": failed_invoices,

        "recommendations": recommendations

    }