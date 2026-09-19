import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Navbar() {
  const navigate = useNavigate();

  const user = JSON.parse(
    localStorage.getItem("user") || "null"
  );
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const loadUnreadCount = async () => {
      try {
        const response = await api.get(
          "/notifications/unread-count"
        );
        setUnreadCount(response.data.count || 0);
      } catch {
        setUnreadCount(0);
      }
    };

    loadUnreadCount();
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    navigate("/login");
  };

  const isAdmin = user?.role === "admin";
  const isAuthority = user?.role === "authority";
  const isFieldStaff = user?.role === "field_staff";
  const isCitizen = user?.role === "citizen";

  return (
    <nav className="navbar">

      {/* ==================================================
          BRAND
      ================================================== */}

      <div className="navbar-brand">
        Smart Civic
      </div>


      {/* ==================================================
          NAVIGATION
      ================================================== */}

      <div className="navbar-links">

        {/* COMMON DASHBOARD */}

        <Link to="/dashboard">
          Dashboard
        </Link>

        <Link to="/notifications">
          Notifications
          {unreadCount > 0 && ` (${unreadCount})`}
        </Link>


        {/* ==================================================
            ADMIN
        ================================================== */}

        {isAdmin && (
          <Link to="/admin">
            Admin Dashboard
          </Link>
        )}


        {/* ==================================================
            AUTHORITY
        ================================================== */}

        {isAuthority && (
          <Link to="/authority">
            Authority Dashboard
          </Link>
        )}


        {/* ==================================================
            FIELD STAFF
        ================================================== */}

        {isFieldStaff && (
          <Link to="/field-staff">
            Field Staff Dashboard
          </Link>
        )}


        {/* ==================================================
            CITIZEN
        ================================================== */}

        {isCitizen && (
          <>
            <Link to="/report">
              Report Issue
            </Link>

            <Link to="/my-issues">
              My Issues
            </Link>
          </>
        )}


        {/* ==================================================
            LOGOUT
        ================================================== */}

        <button onClick={logout}>
          Logout
        </button>

      </div>

    </nav>
  );
}
