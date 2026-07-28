function ViewInvoiceModal({

    invoice,

    onClose

}) {

    if (!invoice) return null;

    let validation = invoice.validation_errors;

    try {

        while (typeof validation === "string") {

            validation = JSON.parse(validation);

        }

    }

    catch {

        validation = [];

    }

    return (

        <div className="modal-overlay">

            <div className="modal">

                <h2>

                    Invoice Details

                </h2>

                <hr />

                <p>

                    <strong>ID :</strong> {invoice.id}

                </p>

                <p>

                    <strong>Invoice Number :</strong> {invoice.invoice_number}

                </p>

                <p>

                    <strong>Vendor :</strong> {invoice.vendor || "N/A"}

                </p>

                <p>

                    <strong>Date :</strong> {invoice.invoice_date}

                </p>

                <p>

                    <strong>Amount :</strong>

                    {" "}₹ {Number(invoice.amount).toLocaleString()}

                </p>

                <p>

                    <strong>Status :</strong>

                    <span

                        style={{

                            color:

                                invoice.status === "VALID"

                                    ? "#22c55e"

                                    : "#ef4444",

                            fontWeight: "bold"

                        }}

                    >

                        {" "}{invoice.status}

                    </span>

                </p>

                <hr />

                <h3>

                    Validation Report

                </h3>

                {

                    !Array.isArray(validation) || validation.length === 0

                    ?

                    <div

                        style={{

                            background: "#dcfce7",

                            color: "#166534",

                            padding: "12px",

                            borderRadius: "8px",

                            marginBottom: "15px",

                            fontWeight: "bold"

                        }}

                    >

                        ✅ Invoice passed all validation checks.

                    </div>

                    :

                    validation.map((error, index) => (

                        <div

                            key={index}

                            style={{

                                marginBottom: "12px",

                                padding: "12px",

                                border: "1px solid #ccc",

                                borderRadius: "8px"

                            }}

                        >

                            {

                                typeof error === "string"

                                ?

                                <p>

                                    {error}

                                </p>

                                :

                                <>

                                    <p>

                                        <strong>Field :</strong> {error.field}

                                    </p>

                                    <p>

                                        <strong>Problem :</strong> {error.problem}

                                    </p>

                                    <p>

                                        <strong>Found :</strong> {String(error.value_found)}

                                    </p>

                                    <p>

                                        <strong>Expected :</strong> {error.expected}

                                    </p>

                                </>

                            }

                        </div>

                    ))

                }

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