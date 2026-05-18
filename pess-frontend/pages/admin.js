import { useEffect, useState } from "react";

export default function Admin() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("https://pess-backend.onrender.com/auth/users")
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  return (
    <div className="container py-5">
      <h2>Admin Dashboard</h2>
      <table className="table table-bordered mt-3">
        <thead>
          <tr><th>ID</th><th>Serial</th><th>Password</th></tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.serial}</td>
              <td>{u.password}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
