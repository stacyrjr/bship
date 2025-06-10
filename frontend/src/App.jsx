import React, { useState } from 'react';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = async () => {
    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',  // IMPORTANT: send cookies!
        body: JSON.stringify({ username, password }),
      });

      if (res.ok) {
        setIsLoggedIn(true);
        setMessage('Logged in!');
      } else {
        const err = await res.json();
        setMessage(`Login failed: ${err.detail || err.message}`);
      }
    } catch (err) {
      setMessage(`Login error: ${err.message}`);
    }
  };

  const handleLogout = async () => {
    await fetch('http://localhost:8000/logout', {
      method: 'POST',
      credentials: 'include',
    });
    setIsLoggedIn(false);
    setMessage('Logged out!');
  };

  const testAuthenticatedResource = async () => {
    try {
      const res = await fetch('http://localhost:8000/authenticated-resource', {
        method: 'GET',
        credentials: 'include',
      });

      if (res.ok) {
        setMessage('Accessed protected resource!');
      } else {
        setMessage('Failed to access protected resource.');
      }
    } catch (err) {
      setMessage(`Error: ${err.message}`);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Battleship Auth Test</h1>

      {!isLoggedIn ? (
        <>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          /><br />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          /><br />
          <button onClick={handleLogin}>Login</button>
        </>
      ) : (
        <>
          <button onClick={handleLogout}>Logout</button><br />
          <button onClick={testAuthenticatedResource}>Test Authenticated Resource</button>
        </>
      )}

      <p>{message}</p>
    </div>
  );
}

export default App;
