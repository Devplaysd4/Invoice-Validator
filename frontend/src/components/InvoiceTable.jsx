function InvoiceTable({ invoices, onDelete }) {

    return (

        <table border="1">

            <thead>

                <tr>

                    <th>ID</th>

                    <th>Invoice</th>

                    <th>Vendor</th>

                    <th>Amount</th>

                    <th>Status</th>

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

                            <td>{invoice.amount}</td>

                            <td>{invoice.status}</td>

                            <td>

                                <button
                                    onClick={() =>
                                        onDelete(invoice.id)
                                    }
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