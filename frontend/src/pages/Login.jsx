import { useState } from "react";

import { login } from "../api/api";

import { useNavigate } from "react-router-dom";

function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);

    async function handleLogin() {

        if (!username || !password) {

            alert("Enter username and password.");

            return;

        }

        setLoading(true);

        try {

            await login(username, password);

            navigate("/");

        }

        catch {

            alert("Invalid Username or Password");

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <div className="login-container">

            <div className="login-card">

                <h1>

                    Intelligent Invoice Processing

                </h1>

                <p>

                    Sign in to continue

                </p>

                <input

                    type="text"

                    placeholder="Username"

                    value={username}

                    onChange={(e) =>

                        setUsername(e.target.value)

                    }

                />

                <input

                    type="password"

                    placeholder="Password"

                    value={password}

                    onChange={(e) =>

                        setPassword(e.target.value)

                    }

                />

                <button

                    onClick={handleLogin}

                    disabled={loading}

                >

                    {

                        loading

                            ?

                            "Signing In..."

                            :

                            "Login"

                    }

                </button>

            </div>

        </div>

    );

}

export default Login;