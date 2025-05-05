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
        <button className="button" type="button" onClick={() => navigate('/register')}>
          Register
        </button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/Register', {
        username,
        password,
      });

      setMessage(response.data.message);

      if (response.data.success) {
        navigate('/login'); 
      }
    } catch (error) {
      setMessage('Failed to register!');
    }
  };

  return (
    <div>
      <h1> Create a new account</h1>
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
          Register
        </button>
        <button className="button" type="button" onClick={() => navigate('/login')}>
          Back to Login Screen
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
        <Route path="/Register" element={<Register />} />
        <Route
          path="/home"
          element={isAuthenticated || localStorage.getItem("authToken") ? <Home /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  )
}

export default App;
