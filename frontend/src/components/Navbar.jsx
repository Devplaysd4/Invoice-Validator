import { Link } from "react-router-dom";

function Navbar() {

    return (

        <nav>

            <Link to="/">Dashboard</Link>

            {" | "}

            <Link to="/upload">Upload</Link>

        </nav>

    );

}

export default Navbar;