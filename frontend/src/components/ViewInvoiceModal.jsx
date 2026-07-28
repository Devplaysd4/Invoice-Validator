function ViewInvoiceModal({

    invoice,

    onClose

}) {

    if (!invoice) return null;

    return (

        <div className="modal-overlay">

            <div className="modal">

                <h2>

                    Invoice Details

                </h2>

                <p>

                    <strong>ID</strong>

                    {invoice.id}

                </p>

                <p>

                    <strong>Invoice</strong>

                    {invoice.invoice_number}

                </p>

                <p>

                    <strong>Vendor</strong>

                    {invoice.vendor}

                </p>

                <p>

                    <strong>Date</strong>

                    {invoice.invoice_date}

                </p>

                <p>

                    <strong>Amount</strong>

                    ₹ {invoice.amount}

                </p>

                <p>

                    <strong>Status</strong>

                    {invoice.status}

                </p>

                <p>

                    <strong>Validation</strong>

                </p>

                <pre>

                    {

                        invoice.validation_errors

                    }

                </pre>

                <button

                    onClick={onClose}

                >

                    Close

                </button>

            </div>

        </div>

    );

}

export default ViewInvoiceModal;