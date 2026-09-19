import { Link } from "react-router-dom";

export default function Dashboard() {
  const user = JSON.parse(
    localStorage.getItem("user") || "null"
  );

  return (
    <div className="page">

      <div className="hero">
        <h1>
          Welcome, {user?.name || "Citizen"}
        </h1>

        <p>
          Report and track public infrastructure
          issues in your community.
        </p>
      </div>

      <div className="dashboard-grid">

        <Link
          to="/report"
          className="dashboard-card"
        >
          <h2>Report an Issue</h2>
          <p>
            Report roads, street lights,
            waste, water and other civic problems.
          </p>
        </Link>

        <Link
          to="/my-issues"
          className="dashboard-card"
        >
          <h2>My Issues</h2>
          <p>
            View the issues you have reported
            and track their status.
          </p>
        </Link>

      </div>

    </div>
  );
}