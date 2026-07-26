import { useEffect, useState } from "react";

import {
    getInvoices,
    deleteInvoice
} from "../api/api";

import InvoiceTable from "../components/InvoiceTable";

function Dashboard() {

    const [invoices, setInvoices] = useState([]);

    async function loadInvoices() {

        const data = await getInvoices();

        setInvoices(data);

    }

    async function handleDelete(id) {

        await deleteInvoice(id);

        loadInvoices();

    }

    useEffect(() => {

        loadInvoices();

    }, []);

    const total = invoices.length;

    const valid = invoices.filter(
        invoice => invoice.status === "VALID"
    ).length;

    const invalid = total - valid;

    const totalAmount = invoices.reduce(
        (sum, invoice) => sum + Number(invoice.amount || 0),
        0
    );

    const successRate =
        total === 0
            ? 0
            : ((valid / total) * 100).toFixed(2);

    return (

        <div>

            <h1>Invoice Dashboard</h1>

            <div className="dashboard-cards">

                <div className="card">
                    <h3>Total Invoices</h3>
                    <h2>{total}</h2>
                </div>

                <div className="card">
                    <h3>Valid</h3>
                    <h2>{valid}</h2>
                </div>

                <div className="card">
                    <h3>Invalid</h3>
                    <h2>{invalid}</h2>
                </div>

                <div className="card">
                    <h3>Success Rate</h3>
                    <h2>{successRate}%</h2>
                </div>

                <div className="card">
                    <h3>Total Amount</h3>
                    <h2>₹ {totalAmount.toFixed(2)}</h2>
                </div>

            </div>

            <InvoiceTable
                invoices={invoices}
                onDelete={handleDelete}
            />

        </div>

    );

}

export default Dashboard;