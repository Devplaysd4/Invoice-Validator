import { useState } from "react";

import {
    uploadInvoice,
    saveAnyway
} from "../api/api";

function Upload() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [showReport, setShowReport] = useState(false);

    async function handleUpload() {

        if (!file) {
            alert("Choose file");
            return;
        }

        setLoading(true);

        try {

            const response = await uploadInvoice(file);

            console.log(response);

            setResult(response);

        }

        catch (err) {

            console.log(err);

            alert("Upload Failed");

        }

        finally {

            setLoading(false);

        }

    }

    async function handleSaveAnyway(invoice) {

        try {

            await saveAnyway(invoice);

            alert("Invoice saved successfully.");

        }

        catch (err) {

            console.log(err);

            alert("Save failed.");

        }

    }

    return (

        <div className="upload-page">

            <h1>Upload Invoice</h1>

            <div className="upload-box">

                <input

                    type="file"

                    onChange={(e) =>

                        setFile(e.target.files[0])

                    }

                />

                <button

                    onClick={handleUpload}

                >

                    Upload

                </button>

            </div>

            {

                loading &&

                <h3>Uploading...</h3>

            }

            {

                result &&

                <div className="upload-result">

                    <h2>Upload Successful</h2>

                    <p>

                        <b>File:</b> {result.data.original_filename}

                    </p>

                    <p>

                        <b>Type:</b> {result.data.file_type}

                    </p>

                    <p>

                        <b>Saved Records:</b> {result.data.database.saved_records}

                    </p>

                    <p>

                        <b>Duplicates:</b> {result.data.database.duplicates.length}

                    </p>

                    <hr />

                    <h2>Validation Summary</h2>

                    <p>

                        <b>Total Invoices:</b>{" "}

                        {result.data.validation_report.summary.total_invoices}

                    </p>

                    <p>

                        <b>Valid:</b>{" "}

                        {result.data.validation_report.summary.valid_invoices}

                    </p>

                    <p>

                        <b>Invalid:</b>{" "}

                        {result.data.validation_report.summary.invalid_invoices}

                    </p>

                    <p>

                        <b>Success Rate:</b>{" "}

                        {result.data.validation_report.summary.success_rate}

                    </p>

                    <button

                        onClick={() =>

                            setShowReport(!showReport)

                        }

                    >

                        {

                            showReport

                                ?

                                "Hide Full Validation Report"

                                :

                                "View Full Validation Report"

                        }

                    </button>

                    {

                        showReport &&

                        <div

                            style={{

                                marginTop: "20px",

                                maxHeight: "400px",

                                overflowY: "auto",

                                overflowX: "auto",

                                border: "1px solid #444",

                                borderRadius: "8px"

                            }}

                        >

                            <pre

                                style={{

                                    margin: 0,

                                    padding: "15px",

                                    background: "#111827",

                                    color: "#ffffff",

                                    whiteSpace: "pre-wrap"

                                }}

                            >

                                {

                                    JSON.stringify(

                                        result.data.validation_report,

                                        null,

                                        2

                                    )

                                }

                            </pre>

                        </div>

                    }

                    <hr />

                    <h2>Invalid Invoices</h2>

                    <div

                        style={{

                            maxHeight: "350px",

                            overflowY: "auto",

                            border: "1px solid #ddd",

                            borderRadius: "8px",

                            padding: "10px"

                        }}

                    >

                        {

                            result.data.parsed_rows

                                .filter(

                                    invoice =>

                                        invoice.status === "INVALID"

                                )

                                .length === 0

                            ?

                            <p>

                                🎉 No invalid invoices found.

                            </p>

                            :

                            result.data.parsed_rows

                                .filter(

                                    invoice =>

                                        invoice.status === "INVALID"

                                )

                                .map(

                                    (invoice, index) => (

                                        <div

                                            key={index}

                                            style={{

                                                border: "1px solid #ccc",

                                                borderRadius: "8px",

                                                padding: "15px",

                                                marginBottom: "15px"

                                            }}

                                        >

                                            <p>

                                                <b>Invoice:</b>{" "}

                                                {invoice.invoice_number || "Missing"}

                                            </p>

                                            <p>

                                                <b>Vendor:</b>{" "}

                                                {invoice.vendor || "Missing"}

                                            </p>

                                            <p>

                                                <b>Status:</b>{" "}

                                                {invoice.status}

                                            </p>

                                            <pre

                                                style={{

                                                    whiteSpace: "pre-wrap"

                                                }}

                                            >

                                                {

                                                    JSON.stringify(

                                                        invoice.validation_errors,

                                                        null,

                                                        2

                                                    )

                                                }

                                            </pre>

                                            <button

                                                onClick={() =>

                                                    handleSaveAnyway(invoice)

                                                }

                                            >

                                                Save Anyway

                                            </button>

                                        </div>

                                    )

                                )

                        }

                    </div>

                </div>

            }

        </div>

    );

}

export default Upload;