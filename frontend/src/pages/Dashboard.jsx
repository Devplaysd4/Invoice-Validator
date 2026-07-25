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

    return (

        <div>

            <h1>

                Dashboard

            </h1>

            <InvoiceTable

                invoices={invoices}

                onDelete={handleDelete}

            />

        </div>

    );

}

export default Dashboard;