import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function FieldStaffDashboard() {
  const [issues, setIssues] = useState([]);
  const [statusFilter, setStatusFilter] = useState("all");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const user = JSON.parse(
    localStorage.getItem("user") || "null"
  );

  useEffect(() => {
    const loadAssignedIssues = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(
          "/issues/assigned"
        );

        setIssues(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load assigned issues"
        );
      } finally {
        setLoading(false);
      }
    };

    loadAssignedIssues();
  }, []);

  const filteredIssues = useMemo(() => {
    return issues.filter((issue) => {
      return (
        statusFilter === "all" ||
        issue.status === statusFilter
      );
    });
  }, [issues, statusFilter]);

  const totalIssues = issues.length;

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

  if (
    user?.role !== "field_staff"
  ) {
    return (
      <div className="page">
        <div className="error">
          You do not have permission to access
          the Field Staff Dashboard.
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="page">
        <div className="hero">
          <h1>Field Staff Dashboard</h1>

          <p>
            Loading your assigned civic issues...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <div className="hero">

        <h1>
          Field Staff Dashboard
        </h1>

        <p>
          View and manage civic issues assigned
          to you.
        </p>

      </div>


      {/* =====================================================
          SUMMARY CARDS
      ====================================================== */}

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>{totalIssues}</h2>
          <p>Total Assigned</p>
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


      {/* =====================================================
          ERROR
      ====================================================== */}

      {error && (
        <div className="error">
          {error}
        </div>
      )}


      {/* =====================================================
          FILTER
      ====================================================== */}

      <div className="form-card">

        <div className="page-header">

          <div>

            <h2>
              My Assigned Issues
            </h2>

            <p>
              Work on the infrastructure issues
              assigned to you.
            </p>

          </div>

        </div>

        <div className="detail-grid">

          <div>

            <label htmlFor="statusFilter">
              Filter by Status
            </label>

            <select
              id="statusFilter"
              value={statusFilter}
              onChange={(e) =>
                setStatusFilter(
                  e.target.value
                )
              }
            >

              <option value="all">
                All Issues
              </option>

              <option value="assigned">
                Assigned
              </option>

              <option value="in_progress">
                In Progress
              </option>

              <option value="resolved">
                Resolved
              </option>

              <option value="closed">
                Closed
              </option>

            </select>

          </div>

        </div>

      </div>


      {/* =====================================================
          ISSUE LIST
      ====================================================== */}

      <div className="issue-list">

        {filteredIssues.length === 0 ? (

          <div className="empty-state">

            <h2>
              No assigned issues
            </h2>

            <p>
              There are currently no issues
              matching the selected filter.
            </p>

          </div>

        ) : (

          filteredIssues.map((issue) => (

            <div
              key={issue.id}
              className="issue-card"
            >

              {/* ISSUE INFORMATION */}

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
                    gap: "10px",
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

                </div>

              </div>


              {/* STATUS + DETAILS */}

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-end",
                  gap: "12px",
                }}
              >

                <span
                  className={`status status-${issue.status}`}
                >
                  {formatStatus(
                    issue.status
                  )}
                </span>

                <Link
                  to={`/issues/${issue.id}`}
                  className="primary-button"
                >
                  Manage Issue
                </Link>

              </div>

            </div>

          ))

        )}

      </div>

    </div>
  );
}