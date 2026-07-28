import { Link, useLocation } from "react-router-dom";

function Navbar() {

    const location = useLocation();

    return (

        <nav className="navbar">

            <div className="logo">

                Invoice Validator

            </div>

            <div className="nav-links">

                <Link
                    className={
                        location.pathname === "/"
                        ? "active"
                        : ""
                    }
                    to="/"
                >
                    Dashboard
                </Link>

                <Link
                    className={
                        location.pathname === "/upload"
                        ? "active"
                        : ""
                    }
                    to="/upload"
                >
                    Upload
                </Link>

            </div>

        </nav>

    );

}

export default Navbar;