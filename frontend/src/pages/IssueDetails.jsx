import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import IssueLocationMap from "../components/IssueLocationMap";
import api from "../services/api";

export default function IssueDetails() {
  const { issueId } = useParams();

  const [issue, setIssue] = useState(null);
  const [updates, setUpdates] = useState([]);
  const [images, setImages] = useState([]);

  const [selectedStatus, setSelectedStatus] = useState("");
  const [updateMessage, setUpdateMessage] = useState("");

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const user = JSON.parse(
    localStorage.getItem("user") || "null"
  );

  const canManageIssue =
    user?.role === "admin" ||
    user?.role === "field_staff";

  const hasCoordinates =
    issue?.latitude !== null &&
    issue?.latitude !== undefined &&
    issue?.longitude !== null &&
    issue?.longitude !== undefined;

  const allowedStatuses = [
    "reported",
    "assigned",
    "in_progress",
    "resolved",
    "closed",
  ];

  const canDeleteImages =
    user?.role === "admin" ||
    (user?.role === "citizen" &&
      Number(issue?.reported_by) === Number(user?.id)) ||
    (user?.role === "field_staff" &&
      Number(issue?.assigned_to) === Number(user?.id));

  const getImageUrl = (imageUrl) =>
    new URL(imageUrl, api.defaults.baseURL).toString();

  const handleDeleteImage = async (imageId) => {
    if (!window.confirm("Delete this evidence photo?")) {
      return;
    }

    setActionError("");
    setSuccessMessage("");

    try {
      setActionLoading(true);
      await api.delete(
        `/issues/${issueId}/images/${imageId}`
      );
      setImages((currentImages) =>
        currentImages.filter((image) => image.id !== imageId)
      );
      setSuccessMessage("Evidence photo deleted successfully.");
    } catch (err) {
      setActionError(
        err.response?.data?.detail ||
          "Unable to delete evidence photo"
      );
    } finally {
      setActionLoading(false);
    }
  };

  const loadIssue = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const [issueResponse, updatesResponse, imagesResponse] =
        await Promise.all([
          api.get(`/issues/${issueId}`),
          api.get(`/issues/${issueId}/updates`),
          api.get(`/issues/${issueId}/images`),
        ]);

      setIssue(issueResponse.data);
      setUpdates(updatesResponse.data);
      setImages(imagesResponse.data);
      setSelectedStatus(issueResponse.data.status);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load issue"
      );
    } finally {
      setLoading(false);
    }
  }, [issueId]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadIssue();
    }, 0);

    return () => window.clearTimeout(timer);
  }, [loadIssue]);

  const handleStatusUpdate = async (e) => {
    e.preventDefault();

    setActionError("");
    setSuccessMessage("");

    if (!selectedStatus) {
      setActionError("Please select a status.");
      return;
    }

    if (selectedStatus === issue.status) {
      setActionError(
        "Please select a different status."
      );
      return;
    }

    try {
      setActionLoading(true);

      const response = await api.patch(
        `/issues/${issueId}/status`,
        {
          status: selectedStatus,
        }
      );

      setIssue(response.data);

      setSuccessMessage(
        "Issue status updated successfully."
      );

      await loadIssue();
    } catch (err) {
      setActionError(
        err.response?.data?.detail ||
          "Unable to update issue status"
      );
    } finally {
      setActionLoading(false);
    }
  };

  const handleAddUpdate = async (e) => {
    e.preventDefault();

    setActionError("");
    setSuccessMessage("");

    if (!updateMessage.trim()) {
      setActionError(
        "Please enter a progress update message."
      );
      return;
    }

    try {
      setActionLoading(true);

      await api.post(
        `/issues/${issueId}/updates`,
        {
          message: updateMessage.trim(),
          status: selectedStatus || issue.status,
        }
      );

      setUpdateMessage("");

      setSuccessMessage(
        "Progress update added successfully."
      );

      await loadIssue();
    } catch (err) {
      setActionError(
        err.response?.data?.detail ||
          "Unable to add progress update"
      );
    } finally {
      setActionLoading(false);
    }
  };

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

  if (loading) {
    return (
      <div className="page">
        <div className="hero">
          <h1>Issue Details</h1>
          <p>Loading issue information...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <div className="error">
          {error}
        </div>
      </div>
    );
  }

  if (!issue) {
    return (
      <div className="page">
        <div className="empty-state">
          <h2>Issue not found</h2>
          <p>
            The requested civic issue could not be
            found.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">

      {/* =====================================================
          ISSUE INFORMATION
      ====================================================== */}

      <div className="issue-detail-card">

        <div className="page-header">

          <div>
            <h1>{issue.title}</h1>

            <p>
              Issue #{issue.id}
            </p>
          </div>

          <span
            className={`status status-${issue.status}`}
          >
            {formatStatus(issue.status)}
          </span>

        </div>

        {/* DESCRIPTION */}

        <div className="detail-section">

          <h3>Description</h3>

          <p>
            {issue.description}
          </p>

        </div>

        {/* ISSUE DETAILS */}

        <div className="detail-grid">

          <div>
            <strong>Category</strong>
            <p>{issue.category}</p>
          </div>

          <div>
            <strong>Priority</strong>
            <p>{issue.priority}</p>
          </div>

          <div>
            <strong>Severity</strong>
            <p>{issue.severity}</p>
          </div>

          <div>
            <strong>Location</strong>
            <p>
              {issue.location ||
                "Map location not available for this issue."}
            </p>
          </div>

        </div>

        {/* ASSIGNED USER */}

        <div
          style={{
            marginTop: "20px",
            paddingTop: "20px",
            borderTop: "1px solid #e5e7eb",
          }}
        >
          <strong>Assigned To</strong>

          <p>
            {issue.assigned_to
              ? `Field Staff #${issue.assigned_to}`
              : "Not assigned"}
          </p>
        </div>

      </div>


      {hasCoordinates && (
        <div className="timeline-card location-map-card">
          <h2>Location</h2>
          <IssueLocationMap
            latitude={issue.latitude}
            longitude={issue.longitude}
          />
          <div className="selected-coordinates">
            <strong>Issue location</strong>
            <span>Latitude: {issue.latitude}</span>
            <span>Longitude: {issue.longitude}</span>
          </div>
        </div>
      )}


      {/* =====================================================
          EVIDENCE PHOTOS
      ====================================================== */}

      <div className="timeline-card evidence-card">
        <h2>Evidence Photos</h2>

        {images.length === 0 ? (
          <div className="empty-state">
            <h3>No evidence photos uploaded</h3>
          </div>
        ) : (
          <div className="evidence-gallery">
            {images.map((image) => (
              <div
                key={image.id}
                className="evidence-photo"
              >
                <a
                  href={getImageUrl(image.image_url)}
                  target="_blank"
                  rel="noreferrer"
                >
                  <img
                    src={getImageUrl(image.image_url)}
                    alt={image.file_name || "Issue evidence"}
                  />
                </a>

                {canDeleteImages ? (
                  <button
                    type="button"
                    className="danger-button"
                    onClick={() => handleDeleteImage(image.id)}
                    disabled={actionLoading}
                  >
                    Delete
                  </button>
                ) : null}
              </div>
            ))}
          </div>
        )}
      </div>


      {/* =====================================================
          MANAGEMENT SECTION
      ====================================================== */}

      {canManageIssue && (
        <div className="form-card">

          <div className="page-header">

            <div>
              <h2>Manage Issue</h2>

              <p>
                Update the current status and add
                progress information.
              </p>
            </div>

          </div>

          {actionError && (
            <div className="error">
              {actionError}
            </div>
          )}

          {successMessage && (
            <div
              style={{
                padding: "12px",
                margin: "10px 0",
                borderRadius: "7px",
                background: "#dcfce7",
                color: "#166534",
              }}
            >
              {successMessage}
            </div>
          )}

          {/* STATUS UPDATE */}

          <form
            onSubmit={handleStatusUpdate}
            style={{
              marginTop: "20px",
            }}
          >

            <label htmlFor="status">
              Change Status
            </label>

            <select
              id="status"
              value={selectedStatus}
              onChange={(e) =>
                setSelectedStatus(
                  e.target.value
                )
              }
              disabled={actionLoading}
            >

              {allowedStatuses.map(
                (status) => (
                  <option
                    key={status}
                    value={status}
                  >
                    {formatStatus(status)}
                  </option>
                )
              )}

            </select>

            <button
              type="submit"
              className="primary-button"
              disabled={
                actionLoading ||
                selectedStatus === issue.status
              }
              style={{
                marginTop: "15px",
              }}
            >
              {actionLoading
                ? "Updating..."
                : "Update Status"}
            </button>

          </form>


          {/* PROGRESS UPDATE */}

          <form
            onSubmit={handleAddUpdate}
            style={{
              marginTop: "30px",
            }}
          >

            <label htmlFor="updateMessage">
              Progress Update
            </label>

            <textarea
              id="updateMessage"
              value={updateMessage}
              onChange={(e) =>
                setUpdateMessage(
                  e.target.value
                )
              }
              placeholder="Describe the work completed or progress made..."
              rows="5"
              disabled={actionLoading}
            />

            <button
              type="submit"
              className="primary-button"
              disabled={
                actionLoading ||
                !updateMessage.trim()
              }
              style={{
                marginTop: "15px",
              }}
            >
              {actionLoading
                ? "Adding Update..."
                : "Add Progress Update"}
            </button>

          </form>

        </div>
      )}


      {/* =====================================================
          PROGRESS HISTORY
      ====================================================== */}

      <div className="timeline-card">

        <h2>Issue Progress</h2>

        {updates.length === 0 ? (
          <div className="empty-state">
            <h3>No progress updates yet</h3>

            <p>
              No status or progress updates have
              been recorded for this issue.
            </p>
          </div>
        ) : (
          <div className="timeline">

            {updates.map((update) => (
              <div
                key={update.id}
                className="timeline-item"
              >

                <span className="timeline-dot" />

                <div>

                  <h3>
                    {formatStatus(
                      update.status
                    )}
                  </h3>

                  <p>
                    {update.message}
                  </p>

                  <small>
                    {update.created_at
                      ? new Date(
                          update.created_at
                        ).toLocaleString()
                      : ""}
                  </small>

                </div>

              </div>
            ))}

          </div>
        )}

      </div>

    </div>
  );
}
