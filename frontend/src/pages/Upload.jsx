import { useState } from "react";

import { uploadInvoice } from "../api/api";

function Upload() {

    const [file, setFile] = useState(null);

    const [loading, setLoading] = useState(false);

    const [result, setResult] = useState(null);

    async function handleUpload() {

        if (!file) {

            alert("Choose a file.");

            return;

        }

        setLoading(true);

        try {

            const response = await uploadInvoice(file);

            setResult(response);

        }

        catch (err) {

            console.error(err);

            alert("Upload Failed");

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <div>

            <h1>Upload Invoice</h1>

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

            {

                loading &&

                <p>

                    Uploading...

                </p>

            }

            {

                result &&

                <pre>

                    {

                        JSON.stringify(

                            result,

                            null,

                            2

                        )

                    }

                </pre>

            }

        </div>

    );

}

export default Upload;