import useSession from "../hooks/useSession";

export default function Admin() {
  const role = useSession();

  if (role === null) return <p>Loading...</p>;
  if (role !== "admin") {
    if (typeof window !== "undefined") window.location.href = "/login";
    return null;
  }

  return (
    <div className="container py-5">
      <h2>Admin Dashboard</h2>
      {/* user table here */}
    </div>
  );
}
