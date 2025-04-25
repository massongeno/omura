import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './App.css';
import Home from "./pages/home.jsx"

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/login', {
        username,
        password,
      });

      setMessage(response.data.message);

      // Auth token storage
      if (response.data.success) {
        localStorage.setItem('authToken', response.data.token);
        navigate('/home'); 
      }
    } catch (error) {
      setMessage('Login failed!');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="button" type="submit">
          Login
        </button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Check if the user is authenticated when the app loads or if the token changes
  useEffect(() => {
    const token = localStorage.getItem("authToken")
    if (token) {
      setIsAuthenticated(true)
    } else {
      setIsAuthenticated(false)
    }
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/home"
          element={isAuthenticated || localStorage.getItem("authToken") ? <Home /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  )
}

export default App;
