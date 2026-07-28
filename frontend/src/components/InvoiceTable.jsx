function InvoiceTable({

    invoices,

    onDelete,

    onView,

    onEdit,


}) {

    return (

        <div className="table-container">

            <table>

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Invoice</th>

                        <th>Vendor</th>

                        <th>Date</th>

                        <th>Amount</th>

                        <th>Status</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        invoices.map(invoice => (

                            <tr key={invoice.id}>

                                <td>{invoice.id}</td>

                                <td>{invoice.invoice_number}</td>

                                <td>{invoice.vendor}</td>

                                <td>{invoice.invoice_date}</td>

                                <td>

                                    ₹ {Number(invoice.amount).toLocaleString()}

                                </td>

                                <td>

                                    <span

                                        className={

                                            invoice.status === "VALID"

                                            ? "status valid"

                                            : "status invalid"

                                        }

                                    >

                                        {invoice.status}

                                    </span>

                                </td>

                                <td>

    <button

        className="view-btn"

        onClick={() =>

            onView(invoice)

        }

    >

        View

    </button>

    

    <button

        className="edit-btn"

        onClick={() =>

            onEdit(invoice)

        }

    >

        Edit

    </button>

    <button

        className="delete-btn"

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

        </div>

    );

}

export default InvoiceTable;