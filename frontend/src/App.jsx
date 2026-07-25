import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";

import Upload from "./pages/Upload";

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
