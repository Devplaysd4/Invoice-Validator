import { useState,useEffect } from "react";

import {

    updateInvoice

} from "../api/api";

function EditInvoiceModal({

    invoice,

    onClose,

    refresh

}) {

    const [form,setForm]=useState({});

    useEffect(()=>{

        if(invoice){

            setForm(invoice);

        }

    },[invoice]);

    if(!invoice) return null;

    async function save(){

        await updateInvoice(

            invoice.id,

            form

        );

        refresh();

        onClose();

    }

    return(

        <div className="modal-overlay">

            <div className="modal">

                <h2>

                    Edit Invoice

                </h2>

                <label>

                    Invoice Number

                </label>

                <input

                    value={form.invoice_number||""}

                    onChange={(e)=>

                        setForm({

                            ...form,

                            invoice_number:e.target.value

                        })

                    }

                />

                <label>

                    Vendor

                </label>

                <input

                    value={form.vendor||""}

                    onChange={(e)=>

                        setForm({

                            ...form,

                            vendor:e.target.value

                        })

                    }

                />

                <label>

                    Date

                </label>

                <input

                    type="date"

                    value={form.invoice_date||""}

                    onChange={(e)=>

                        setForm({

                            ...form,

                            invoice_date:e.target.value

                        })

                    }

                />

                <label>

                    Amount

                </label>

                <input

                    type="number"

                    value={form.amount||0}

                    onChange={(e)=>

                        setForm({

                            ...form,

                            amount:e.target.value

                        })

                    }

                />

                <label>

                    Status

                </label>

                <select

                    value={form.status}

                    onChange={(e)=>

                        setForm({

                            ...form,

                            status:e.target.value

                        })

                    }

                >

                    <option>

                        VALID

                    </option>

                    <option>

                        INVALID

                    </option>

                </select>

                <div className="buttons">

                    <button

                        className="save-btn"

                        onClick={save}

                    >

                        Save

                    </button>

                    <button

                        onClick={onClose}

                    >

                        Cancel

                    </button>

                </div>

            </div>

        </div>

    );

}

export default EditInvoiceModal;