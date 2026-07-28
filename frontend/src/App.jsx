import {
    Routes,
    Route,
    Navigate,
    useLocation
} from "react-router-dom";
import { useEffect } from "react";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Login from "./pages/Login";

function App() {

    const token = localStorage.getItem("token");

    const location = useLocation();

    useEffect(() => {

    localStorage.removeItem("token");

}, []);

    return (

        <div className="app">

            {

                location.pathname !== "/login" &&

                <Navbar />

            }

            <main className="container">

                <Routes>

                    <Route

                        path="/login"

                        element={

                            token

                                ?

                                <Navigate
                                    to="/"
                                    replace
                                />

                                :

                                <Login />

                        }

                    />

                    <Route

                        path="/"

                        element={

                            token

                                ?

                                <Dashboard />

                                :

                                <Navigate
                                    to="/login"
                                    replace
                                />

                        }

                    />

                    <Route

                        path="/upload"

                        element={

                            token

                                ?

                                <Upload />

                                :

                                <Navigate
                                    to="/login"
                                    replace
                                />

                        }

                    />

                </Routes>

            </main>

        </div>

    );

}

export default App;