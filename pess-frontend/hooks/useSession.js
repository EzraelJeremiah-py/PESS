import { useEffect, useState } from "react";

export default function useSession() {
  const [role, setRole] = useState(null);

  useEffect(() => {
    fetch("https://pess-backend.onrender.com/auth/session")
      .then(res => res.json())
      .then(data => setRole(data.role));
  }, []);

  return role;
}
