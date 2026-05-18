export default function Home() {
  return (
    <div className="text-center py-5">
      {/* Hero Section */}
      <div className="bg-light p-5 rounded shadow-sm">
        <h1 className="display-4 fw-bold">Welcome to PESS</h1>
        <p className="lead mt-3">
          Student & Admin Portal powered by Flask + Next.js
        </p>
        <div className="mt-4">
          <a href="/login" className="btn btn-primary btn-lg mx-2">Login</a>
          <a href="/register" className="btn btn-success btn-lg mx-2">Register</a>
        </div>
      </div>

      {/* Features Section */}
      <div className="row mt-5">
        <div className="col-md-4">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <h5 className="card-title">🔑 Secure Login</h5>
              <p className="card-text">
                Admins and users authenticate safely with SQLite backend.
              </p>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <h5 className="card-title">📋 Admin Dashboard</h5>
              <p className="card-text">
                Manage users, edit accounts, and monitor activity easily.
              </p>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <h5 className="card-title">👨‍🎓 User Portal</h5>
              <p className="card-text">
                Students access their dashboard and personalized content.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer CTA */}
      <div className="mt-5">
        <p className="text-muted">
          Powered by Flask (backend) + Next.js (frontend) • Deployed on Render + Vercel
        </p>
      </div>
    </div>
  );
}
