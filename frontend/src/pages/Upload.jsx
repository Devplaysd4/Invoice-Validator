import { useState } from "react";

import { uploadInvoice } from "../api/api";

function Upload() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    async function handleUpload() {

        if (!file) {
            alert("Choose a file first.");
            return;
        }

        setLoading(true);

        try {

            const response = await uploadInvoice(file);

            setResult(response);

        } catch (err) {

            console.error(err);

            alert("Upload Failed");

        } finally {

            setLoading(false);

        }
    }

    return (

        <div>

            <h1>Upload Invoice</h1>

            <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={handleUpload}>
                Upload
            </button>

            {loading && <p>Uploading...</p>}

            {result && (

                <>

                    <hr />

                    <h2>Upload Summary</h2>

                    <p><b>File:</b> {result.data.original_filename}</p>

                    <p><b>Type:</b> {result.data.file_type}</p>

                    <p><b>Invoices Parsed:</b> {result.data.parsed_rows.length}</p>

                    <p><b>Saved:</b> {result.data.database.saved_records}</p>

                    <p><b>Duplicates:</b> {result.data.database.duplicates.length}</p>

                    <hr />

                    <h2>Validation Report</h2>

                    <table border="1" cellPadding="8">

                        <tbody>

                            <tr>
                                <td>Total</td>
                                <td>{result.data.validation_report.summary.total_invoices}</td>
                            </tr>

                            <tr>
                                <td>Valid</td>
                                <td>{result.data.validation_report.summary.valid_invoices}</td>
                            </tr>

                            <tr>
                                <td>Invalid</td>
                                <td>{result.data.validation_report.summary.invalid_invoices}</td>
                            </tr>

                            <tr>
                                <td>Success Rate</td>
                                <td>{result.data.validation_report.summary.success_rate}%</td>
                            </tr>

                            <tr>
                                <td>Total Amount</td>
                                <td>₹ {result.data.validation_report.statistics.total_amount}</td>
                            </tr>

                            <tr>
                                <td>Average Amount</td>
                                <td>₹ {result.data.validation_report.statistics.average_amount}</td>
                            </tr>

                            <tr>
                                <td>Highest Amount</td>
                                <td>₹ {result.data.validation_report.statistics.highest_amount}</td>
                            </tr>

                            <tr>
                                <td>Lowest Amount</td>
                                <td>₹ {result.data.validation_report.statistics.lowest_amount}</td>
                            </tr>

                        </tbody>

                    </table>

                    <hr />

                    <h2>Parsed Invoices</h2>

                    <table border="1" cellPadding="8">

                        <thead>

                            <tr>

                                <th>Invoice No</th>

                                <th>Vendor</th>

                                <th>Date</th>

                                <th>Amount</th>

                                <th>Status</th>

                            </tr>

                        </thead>

                        <tbody>

                            {result.data.parsed_rows.map((invoice, index) => (

                                <tr key={index}>

                                    <td>{invoice.invoice_number}</td>

                                    <td>{invoice.vendor}</td>

                                    <td>{invoice.invoice_date}</td>

                                    <td>{invoice.amount}</td>

                                    <td>{invoice.status}</td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </>

            )}

        </div>

    );

}

export default Upload;