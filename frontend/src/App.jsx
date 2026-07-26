import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";

function App() {

    return (

        <div className="app">

            <Navbar />

            <main className="container">

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

            </main>

        </div>

    );

}

export default App;

// .app{
//     min-height:100vh;
//     background:#0f172a;
// }

// .container{
//     max-width:1300px;
//     margin:auto;
//     padding:30px;
// }