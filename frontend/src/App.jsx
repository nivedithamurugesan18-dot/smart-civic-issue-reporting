import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ReportIssue from "./pages/ReportIssue";
import MyIssues from "./pages/MyIssues";
import IssueDetails from "./pages/IssueDetails";
import AuthorityDashboard from "./pages/AuthorityDashboard";
import FieldStaffDashboard from "./pages/FieldStaffDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import Notifications from "./pages/Notifications";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* ==================================================
            PUBLIC ROUTES
        ================================================== */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />


        {/* ==================================================
            PROTECTED ROUTES
        ================================================== */}

        <Route element={<ProtectedRoute />}>

          {/* ROOT */}

          <Route
            path="/"
            element={
              <>
                <Navbar />
                <Navigate
                  to="/dashboard"
                  replace
                />
              </>
            }
          />


          {/* CITIZEN DASHBOARD */}

          <Route
            path="/dashboard"
            element={
              <>
                <Navbar />
                <Dashboard />
              </>
            }
          />


          {/* REPORT ISSUE */}

          <Route
            path="/report"
            element={
              <>
                <Navbar />
                <ReportIssue />
              </>
            }
          />


          {/* MY ISSUES */}

          <Route
            path="/my-issues"
            element={
              <>
                <Navbar />
                <MyIssues />
              </>
            }
          />


          {/* ISSUE DETAILS */}

          <Route
            path="/issues/:issueId"
            element={
              <>
                <Navbar />
                <IssueDetails />
              </>
            }
          />


          {/* NOTIFICATIONS */}

          <Route
            path="/notifications"
            element={
              <>
                <Navbar />
                <Notifications />
              </>
            }
          />


          {/* AUTHORITY DASHBOARD */}

          <Route
            path="/authority"
            element={
              <>
                <Navbar />
                <AuthorityDashboard />
              </>
            }
          />


          {/* FIELD STAFF DASHBOARD */}

          <Route
            path="/field-staff"
            element={
              <>
                <Navbar />
                <FieldStaffDashboard />
              </>
            }
          />


          {/* ADMIN DASHBOARD */}

          <Route
            path="/admin"
            element={
              <>
                <Navbar />
                <AdminDashboard />
              </>
            }
          />

        </Route>


        {/* ==================================================
            UNKNOWN ROUTES
        ================================================== */}

        <Route
          path="*"
          element={
            <Navigate
              to="/dashboard"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
