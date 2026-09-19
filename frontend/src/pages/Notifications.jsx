import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadNotifications = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/notifications/");
      setNotifications(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load notifications"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadNotifications();
    }, 0);

    return () => window.clearTimeout(timer);
  }, []);

  const markAsRead = async (notificationId) => {
    try {
      const response = await api.patch(
        `/notifications/${notificationId}/read`
      );

      setNotifications((currentNotifications) =>
        currentNotifications.map((notification) =>
          notification.id === notificationId
            ? response.data
            : notification
        )
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to mark notification as read"
      );
    }
  };

  if (loading) {
    return (
      <div className="page">
        <div className="hero">
          <h1>Notifications</h1>
          <p>Loading notifications...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Notifications</h1>
          <p>Updates about your civic issue activity.</p>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {notifications.length === 0 ? (
        <div className="empty-state">
          <h2>No notifications yet</h2>
          <p>New issue updates will appear here.</p>
        </div>
      ) : (
        <div className="notification-list">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`notification-card ${
                notification.is_read
                  ? ""
                  : "notification-unread"
              }`}
            >
              <div>
                <div className="notification-heading">
                  <h2>{notification.title}</h2>
                  {!notification.is_read && (
                    <span className="notification-badge">
                      Unread
                    </span>
                  )}
                </div>

                <p>{notification.message}</p>

                <small>
                  {notification.created_at
                    ? new Date(
                        notification.created_at
                      ).toLocaleString()
                    : ""}
                  {notification.notification_type &&
                    ` • ${notification.notification_type}`}
                </small>

                {notification.issue_id && (
                  <p>
                    <Link
                      to={`/issues/${notification.issue_id}`}
                    >
                      View issue #{notification.issue_id}
                    </Link>
                  </p>
                )}
              </div>

              {!notification.is_read && (
                <button
                  type="button"
                  onClick={() =>
                    markAsRead(notification.id)
                  }
                >
                  Mark as read
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
