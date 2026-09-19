import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function AdminDashboard() {
  const [issues, setIssues] = useState([]);
  const [staffIds, setStaffIds] = useState({});

  const [loading, setLoading] = useState(true);
  const [assigning, setAssigning] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const user = JSON.parse(
    localStorage.getItem("user") || "null"
  );

  const loadIssues = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/issues/");

      setIssues(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load issues"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadIssues();
    }, 0);

    return () => window.clearTimeout(timer);
  }, []);

  const handleStaffIdChange = (issueId, value) => {
    setStaffIds((previous) => ({
      ...previous,
      [issueId]: value,
    }));
  };

  const handleAssign = async (issueId) => {
    const staffId = staffIds[issueId];

    setError("");
    setSuccess("");

    if (!staffId) {
      setError(
        "Please enter a Field Staff user ID."
      );
      return;
    }

    const numericStaffId = Number(staffId);

    if (!Number.isInteger(numericStaffId)) {
      setError(
        "Field Staff user ID must be a valid number."
      );
      return;
    }

    try {
      setAssigning(issueId);

      await api.patch(
        `/issues/${issueId}/assign`,
        {
          assigned_to: numericStaffId,
        }
      );

      setSuccess(
        `Issue #${issueId} was assigned successfully.`
      );

      setStaffIds((previous) => ({
        ...previous,
        [issueId]: "",
      }));

      await loadIssues();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to assign issue"
      );
    } finally {
      setAssigning(null);
    }
  };

  const totalIssues = issues.length;

  const reportedCount = issues.filter(
    (issue) => issue.status === "reported"
  ).length;

  const assignedCount = issues.filter(
    (issue) => issue.status === "assigned"
  ).length;

  const progressCount = issues.filter(
    (issue) => issue.status === "in_progress"
  ).length;

  const resolvedCount = issues.filter(
    (issue) => issue.status === "resolved"
  ).length;

  const formatStatus = (status) => {
    if (!status) {
      return "";
    }

    return status
      .replace("_", " ")
      .replace(/\b\w/g, (letter) =>
        letter.toUpperCase()
      );
  };

  if (user?.role !== "admin") {
    return (
      <div className="page">
        <div className="error">
          You do not have permission to access
          the Admin Dashboard.
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="page">
        <div className="hero">
          <h1>Admin Dashboard</h1>
          <p>
            Loading civic issue management data...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">

      {/* ==================================================
          HEADER
      ================================================== */}

      <div className="hero">

        <h1>
          Admin Dashboard
        </h1>

        <p>
          Manage reported civic issues and assign
          field staff for resolution.
        </p>

      </div>


      {/* ==================================================
          SUMMARY
      ================================================== */}

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>{totalIssues}</h2>
          <p>Total Issues</p>
        </div>

        <div className="dashboard-card">
          <h2>{reportedCount}</h2>
          <p>Reported</p>
        </div>

        <div className="dashboard-card">
          <h2>{assignedCount}</h2>
          <p>Assigned</p>
        </div>

        <div className="dashboard-card">
          <h2>{progressCount}</h2>
          <p>In Progress</p>
        </div>

        <div className="dashboard-card">
          <h2>{resolvedCount}</h2>
          <p>Resolved</p>
        </div>

      </div>


      {/* ==================================================
          ERROR
      ================================================== */}

      {error && (
        <div className="error">
          {error}
        </div>
      )}


      {/* ==================================================
          SUCCESS
      ================================================== */}

      {success && (
        <div
          style={{
            padding: "12px 16px",
            marginBottom: "20px",
            backgroundColor: "#d1fae5",
            color: "#065f46",
            borderRadius: "8px",
          }}
        >
          {success}
        </div>
      )}


      {/* ==================================================
          ISSUE MANAGEMENT
      ================================================== */}

      <div className="form-card">

        <div className="page-header">

          <div>

            <h2>
              Issue Management
            </h2>

            <p>
              Review reported issues and assign
              them to Field Staff.
            </p>

          </div>

        </div>

      </div>


      {/* ==================================================
          ISSUE LIST
      ================================================== */}

      <div className="issue-list">

        {issues.length === 0 ? (

          <div className="empty-state">

            <h2>
              No issues available
            </h2>

            <p>
              There are currently no civic issues
              in the system.
            </p>

          </div>

        ) : (

          issues.map((issue) => (

            <div
              key={issue.id}
              className="issue-card"
            >

              {/* ------------------------------------------
                  ISSUE INFORMATION
              ------------------------------------------- */}

              <div>

                <h2>
                  {issue.title}
                </h2>

                <p>
                  {issue.description}
                </p>

                <small>

                  Issue #{issue.id}

                  {" • "}

                  {issue.category}

                  {" • "}

                  {issue.location ||
                    "Location not provided"}

                </small>

                <div
                  style={{
                    marginTop: "12px",
                    display: "flex",
                    gap: "12px",
                    flexWrap: "wrap",
                  }}
                >

                  <strong>
                    Priority:{" "}
                    {issue.priority}
                  </strong>

                  <strong>
                    Severity:{" "}
                    {issue.severity}
                  </strong>

                  <strong>
                    Status:{" "}
                    {formatStatus(
                      issue.status
                    )}
                  </strong>

                </div>

              </div>


              {/* ------------------------------------------
                  ACTIONS
              ------------------------------------------- */}

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "12px",
                  minWidth: "220px",
                }}
              >

                <span
                  className={`status status-${issue.status}`}
                >
                  {formatStatus(
                    issue.status
                  )}
                </span>


                {/* ASSIGN FIELD STAFF */}

                <input
                  type="number"
                  min="1"
                  placeholder="Field Staff User ID"
                  value={
                    staffIds[issue.id] || ""
                  }
                  onChange={(e) =>
                    handleStaffIdChange(
                      issue.id,
                      e.target.value
                    )
                  }
                />


                <button
                  className="primary-button"
                  onClick={() =>
                    handleAssign(issue.id)
                  }
                  disabled={
                    assigning === issue.id
                  }
                >
                  {assigning === issue.id
                    ? "Assigning..."
                    : "Assign Field Staff"}
                </button>


                <Link
                  to={`/issues/${issue.id}`}
                  className="primary-button"
                >
                  View Details
                </Link>

              </div>

            </div>

          ))

        )}

      </div>

    </div>
  );
}