import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function MyIssues() {
  const [issues, setIssues] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadIssues = async () => {
      try {
        const response = await api.get(
          "/issues/my"
        );

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

    loadIssues();
  }, []);

  if (loading) {
    return (
      <div className="page">
        <p>Loading issues...</p>
      </div>
    );
  }

  return (
    <div className="page">

      <div className="page-header">
        <h1>My Issues</h1>

        <Link
          to="/report"
          className="primary-button"
        >
          + Report Issue
        </Link>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {issues.length === 0 ? (
        <div className="empty-state">
          <h2>No issues reported</h2>
          <p>
            You haven't reported any civic issues yet.
          </p>
        </div>
      ) : (
        <div className="issue-list">

          {issues.map((issue) => (
            <Link
              key={issue.id}
              to={`/issues/${issue.id}`}
              className="issue-card"
            >
              <div>
                <h2>{issue.title}</h2>

                <p>
                  {issue.description}
                </p>

                <small>
                  {issue.category} •{" "}
                  {issue.location || "Location not provided"}
                </small>
              </div>

              <span
                className={`status status-${issue.status}`}
              >
                {issue.status}
              </span>

            </Link>
          ))}

        </div>
      )}

    </div>
  );
}