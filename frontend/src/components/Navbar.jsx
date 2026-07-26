import { Link } from "react-router-dom";

function Navbar() {

    return (

        <nav className="navbar">

            <h2>Invoice Processor</h2>

            <div className="nav-links">

                <Link to="/">
                    Dashboard
                </Link>

                <Link to="/upload">
                    Upload
                </Link>

            </div>

        </nav>

    );

}

export default Navbar;