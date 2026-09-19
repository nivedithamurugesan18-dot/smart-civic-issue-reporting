import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function AuthorityDashboard() {
  const [issues, setIssues] = useState([]);
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const user = JSON.parse(
    localStorage.getItem("user") || "null"
  );

  useEffect(() => {
    const loadIssues = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/issues/");

        setIssues(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to load reported issues"
        );
      } finally {
        setLoading(false);
      }
    };

    loadIssues();
  }, []);

  const filteredIssues = useMemo(() => {
    return issues.filter((issue) => {
      const matchesStatus =
        statusFilter === "all" ||
        issue.status === statusFilter;

      const matchesPriority =
        priorityFilter === "all" ||
        issue.priority === priorityFilter;

      return matchesStatus && matchesPriority;
    });
  }, [issues, statusFilter, priorityFilter]);

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

  if (user?.role !== "admin" && user?.role !== "authority") {
    return (
      <div className="page">
        <div className="error">
          You do not have permission to access the
          authority dashboard.
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="page">
        <div className="hero">
          <h1>Authority Dashboard</h1>
          <p>Loading reported civic issues...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">

      {/* HEADER */}
      <div className="hero">
        <h1>Authority Dashboard</h1>

        <p>
          Monitor, review and manage reported public
          infrastructure issues.
        </p>
      </div>

      {/* SUMMARY CARDS */}
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

      {/* ERROR */}
      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {/* FILTERS */}
      <div className="form-card">

        <div className="page-header">
          <div>
            <h2>Reported Issues</h2>
            <p>
              Review infrastructure complaints submitted
              by citizens.
            </p>
          </div>
        </div>

        <div className="detail-grid">

          <div>
            <label>Status</label>

            <select
              value={statusFilter}
              onChange={(e) =>
                setStatusFilter(e.target.value)
              }
            >
              <option value="all">
                All Statuses
              </option>

              <option value="reported">
                Reported
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

          <div>
            <label>Priority</label>

            <select
              value={priorityFilter}
              onChange={(e) =>
                setPriorityFilter(e.target.value)
              }
            >
              <option value="all">
                All Priorities
              </option>

              <option value="low">
                Low
              </option>

              <option value="medium">
                Medium
              </option>

              <option value="high">
                High
              </option>

              <option value="critical">
                Critical
              </option>
            </select>
          </div>

        </div>

      </div>

      {/* ISSUE LIST */}
      <div className="issue-list">

        {filteredIssues.length === 0 ? (
          <div className="empty-state">
            <h2>No issues found</h2>

            <p>
              No reported issues match the selected
              filters.
            </p>
          </div>
        ) : (
          filteredIssues.map((issue) => (
            <div
              key={issue.id}
              className="issue-card"
            >

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
                    Priority: {issue.priority}
                  </strong>

                  <strong>
                    Severity: {issue.severity}
                  </strong>
                </div>

              </div>

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
                  {issue.status}
                </span>

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