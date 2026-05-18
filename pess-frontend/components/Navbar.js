import { useEffect, useState } from "react";

export default function Navbar() {
  const [role, setRole] = useState(null);

  useEffect(() => {
    fetch("https://pess-backend.onrender.com/auth/session")
      .then(res => res.json())
      .then(data => setRole(data.role));
  }, []);

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <a className="navbar-brand" href="/">PESS</a>
        <div className="d-flex">
          {role === "admin" && (
            <a className="nav-link" href="/admin">Admin Dashboard</a>
          )}
          {role === "user" && (
            <a className="nav-link" href="/user">User Dashboard</a>
          )}
          {!role && (
            <>
              <a className="nav-link" href="/login">Login</a>
              <a className="nav-link" href="/register">Register</a>
            </>
          )}
          {role && (
            <a className="nav-link" href="https://pess-backend.onrender.com/auth/logout">Logout</a>
          )}
        </div>
      </div>
    </nav>
  );
}
