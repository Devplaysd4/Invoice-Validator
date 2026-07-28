import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export async function uploadInvoice(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload-invoice/",
        formData
    );

    return response.data;
}

export async function getInvoices() {

    const response = await api.get(
        "/invoices/"
    );

    return response.data;
}

export async function getInvoice(id) {

    const response = await api.get(
        `/invoices/${id}`
    );

    return response.data;
}

export async function updateInvoice(id, invoice) {

    const response = await api.put(
        `/invoices/${id}`,
        invoice
    );

    return response.data;
}

export async function deleteInvoice(id) {

    await api.delete(
        `/invoices/${id}`
    );
}
export async function saveAnyway(invoice) {

    const payload = {

        invoice_number:
            invoice.invoice_number || "UNKNOWN",

        vendor:
            invoice.vendor || "Unknown Vendor",

        invoice_date:
            invoice.invoice_date || "2000-01-01",

        amount:
            invoice.amount ?? 0,

        status:
            invoice.status || "INVALID",

        validation_errors:
            JSON.stringify(
                invoice.validation_errors || []
            )

    };

    const response = await api.post(
        "/invoices/override",
        payload
    );

    return response.data;

}