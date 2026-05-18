export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <a className="navbar-brand" href="/">PESS</a>
        <div>
          <a className="nav-link" href="/login">Login</a>
          <a className="nav-link" href="/register">Register</a>
        </div>
      </div>
    </nav>
  );
}
