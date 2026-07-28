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

            <h1>

                Upload Invoice

            </h1>

            <div className="upload-box">

                <input
                    type="file"
                    onChange={(e) =>
                        setFile(
                            e.target.files[0]
                        )
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

                <h3>

                    Uploading...

                </h3>

            }

            {

                result &&

                <div className="upload-result">

                    <h2>

                        Upload Successful

                    </h2>

                    <p>

                        <b>File:</b>{" "}

                        {result.data.original_filename}

                    </p>

                    <p>

                        <b>Type:</b>{" "}

                        {result.data.file_type}

                    </p>

                    <p>

                        <b>Saved:</b>{" "}

                        {result.data.database.saved_records}

                    </p>

                    <p>

                        <b>Duplicates:</b>{" "}

                        {result.data.database.duplicates.length}

                    </p>

                    <p>

                        <b>Valid:</b>{" "}

                        {result.data.validation_report.summary.valid_invoices}

                    </p>

                    <p>

                        <b>Invalid:</b>{" "}

                        {result.data.validation_report.summary.invalid_invoices}

                    </p>

                    <button
                        onClick={() =>
                            setShowReport(!showReport)
                        }
                    >

                        {

                            showReport

                                ?

                                "Hide Validation Report"

                                :

                                "View Validation Report"

                        }

                    </button>

                    {

                        showReport &&

                        <pre>

                            {

                                JSON.stringify(

                                    result.data.validation_report,

                                    null,

                                    2

                                )

                            }

                        </pre>

                    }

                    <h3>

                        Invalid Invoices

                    </h3>

                    {

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

                                            marginTop: "10px",

                                            padding: "10px"

                                        }}

                                    >

                                        <p>

                                            <b>

                                                Invoice:

                                            </b>{" "}

                                            {

                                                invoice.invoice_number ||

                                                "Missing"

                                            }

                                        </p>

                                        <p>

                                            <b>

                                                Vendor:

                                            </b>{" "}

                                            {

                                                invoice.vendor ||

                                                "Missing"

                                            }

                                        </p>

                                        <pre>

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

            }

        </div>

    );

}

export default Upload;