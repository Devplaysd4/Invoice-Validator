function InvoiceTable({ invoices, onDelete }) {

    if (invoices.length === 0) {

        return <h3>No invoices found.</h3>;

    }

    return (

        <table className="invoice-table">

            <thead>

                <tr>

                    <th>ID</th>

                    <th>Invoice Number</th>

                    <th>Vendor</th>

                    <th>Date</th>

                    <th>Amount</th>

                    <th>Status</th>

                    <th>Validation Errors</th>

                    <th>Action</th>

                </tr>

            </thead>

            <tbody>

                {

                    invoices.map((invoice) => (

                        <tr key={invoice.id}>

                            <td>{invoice.id}</td>

                            <td>{invoice.invoice_number}</td>

                            <td>{invoice.vendor}</td>

                            <td>{invoice.invoice_date}</td>

                            <td>₹ {invoice.amount}</td>

                            <td>

                                <span
                                    style={{
                                        color:
                                            invoice.status === "VALID"
                                                ? "limegreen"
                                                : "red",
                                        fontWeight: "bold"
                                    }}
                                >
                                    {invoice.status}
                                </span>

                            </td>

                            <td>

                                {
                                    invoice.validation_errors
                                        ? invoice.validation_errors
                                        : "-"
                                }

                            </td>

                            <td>

                                <button
                                    onClick={() => onDelete(invoice.id)}
                                >
                                    Delete
                                </button>

                            </td>

                        </tr>

                    ))

                }

            </tbody>

        </table>

    );

}

export default InvoiceTable;