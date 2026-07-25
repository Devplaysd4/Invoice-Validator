import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export async function uploadInvoice(file) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload-invoice",
        formData
    );

    return response.data;
}

export async function getInvoices() {

    const response = await api.get(
        "/invoices"
    );

    return response.data;
}

export async function deleteInvoice(id) {

    await api.delete(
        `/invoices/${id}`
    );

}