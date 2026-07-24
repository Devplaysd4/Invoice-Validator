import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";

import Navbar from "./components/Navbar";

function App() {

    return (

        <>

            <Navbar />

            <Routes>

                <Route
                    path="/"
                    element={<Dashboard />}
                />

                <Route
                    path="/upload"
                    element={<Upload />}
                />

            </Routes>

        </>

    );

}

export default App;