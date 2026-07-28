function StatsCards({ invoices }) {

    const total = invoices.length;

    const valid = invoices.filter(
        i => i.status === "VALID"
    ).length;

    const invalid = invoices.filter(
        i => i.status === "INVALID"
    ).length;

    const duplicates = total - new Set(
        invoices.map(i => i.invoice_number)
    ).size;

    const totalAmount = invoices.reduce(

        (sum, invoice) =>

            sum + Number(invoice.amount || 0),

        0

    );

    return (

        <div className="stats-grid">

            <div className="card">

                <h2>{total}</h2>

                <p>Total Invoices</p>

            </div>

            <div className="card green">

                <h2>{valid}</h2>

                <p>Valid</p>

            </div>

            <div className="card red">

                <h2>{invalid}</h2>

                <p>Invalid</p>

            </div>

            <div className="card yellow">

                <h2>{duplicates}</h2>

                <p>Duplicates</p>

            </div>

            <div className="card blue">

                <h2>

                    ₹ {totalAmount.toLocaleString()}

                </h2>

                <p>Total Amount</p>

            </div>

        </div>

    );

}

export default StatsCards;