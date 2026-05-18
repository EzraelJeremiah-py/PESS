import useSession from "../hooks/useSession";

export default function User() {
  const role = useSession();

  if (role === null) return <p>Loading...</p>;
  if (role !== "user") {
    if (typeof window !== "undefined") window.location.href = "/login";
    return null;
  }

  return (
    <div className="container py-5">
      <h2>User Dashboard</h2>
      <p>Welcome! Your serial is recognized.</p>
    </div>
  );
}
