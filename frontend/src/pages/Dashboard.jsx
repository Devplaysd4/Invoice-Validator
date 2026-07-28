import { useEffect, useState } from "react";

import {

    getInvoices,

    deleteInvoice

} from "../api/api";

import InvoiceTable from "../components/InvoiceTable";

import StatsCards from "../components/StatsCards";

import SearchBar from "../components/SearchBar";

import ViewInvoiceModal from "../components/ViewInvoiceModal";

import EditInvoiceModal from "../components/EditInvoiceModal";

function Dashboard(){

    const [invoices,setInvoices]=useState([]);

    const [filtered,setFiltered]=useState([]);

    const [search,setSearch]=useState("");

    const [status,setStatus]=useState("ALL");

    const [selectedInvoice,setSelectedInvoice]=useState(null);

    const [editingInvoice,setEditingInvoice]=useState(null);

    
    async function loadInvoices(){

        const data=await getInvoices();

        setInvoices(data);

    }

    useEffect(()=>{

        loadInvoices();

    },[]);

    useEffect(()=>{

        let temp=[...invoices];

        if(status!=="ALL"){

            temp=temp.filter(

                invoice=>invoice.status===status

            );

        }

        if(search){

            const s=search.toLowerCase();

            temp=temp.filter(invoice=>

                invoice.invoice_number?.toLowerCase().includes(s)

                ||

                invoice.vendor?.toLowerCase().includes(s)

            );

        }

        setFiltered(temp);

    },[search,status,invoices]);

    async function handleDelete(id){

        if(!window.confirm("Delete Invoice?")) return;

        await deleteInvoice(id);

        loadInvoices();

    }

    return(

        <div className="container">

            <h1>

                Invoice Processing Dashboard

            </h1>

            <StatsCards

                invoices={invoices}

            />

            <SearchBar

                search={search}

                setSearch={setSearch}

                status={status}

                setStatus={setStatus}

            />

            <InvoiceTable

                invoices={filtered}

                onDelete={handleDelete}

                onView={setSelectedInvoice}

                onEdit={setEditingInvoice}

                

            />

            <ViewInvoiceModal

                invoice={selectedInvoice}

                onClose={()=>setSelectedInvoice(null)}

            />

            <EditInvoiceModal

                invoice={editingInvoice}

                refresh={loadInvoices}

                onClose={()=>setEditingInvoice(null)}

            />

        </div>

    );

}

export default Dashboard;