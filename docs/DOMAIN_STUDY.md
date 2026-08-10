# Domain Study

## 1. Domain

The project belongs to the following domains:

- Civic Technology
- Smart City
- Public Infrastructure Management
- Artificial Intelligence and Data Science

The system focuses on using a digital platform to improve the
reporting and management of public infrastructure issues.

---

## 2. Domain Overview

Public infrastructure includes facilities and structures that are
used by people in their daily lives.

Examples include:

- Roads
- Streetlights
- Traffic signs
- Public pathways
- Other commonly used civic infrastructure

Infrastructure can become damaged because of regular use, weather,
accidents, poor maintenance, or other reasons.

When these problems are not identified and handled properly, they can
affect public safety, transportation, and the quality of daily life.

Our project focuses on creating a centralized system for reporting
and managing these infrastructure issues.

---

## 3. Current Real-World Problem

Citizens may notice infrastructure problems but may not have a simple
centralized method to report them with complete information.

A report may not contain:

- A clear description
- A photograph
- Exact location
- Issue category
- Priority information

Authorities may also have difficulty managing many reports,
identifying responsible departments, assigning field staff, and
tracking whether reported problems have been resolved.

This can result in delayed maintenance and poor visibility of
unresolved infrastructure problems.

---

## 4. Target Users

The system has three main user roles.

### Citizen

Citizens can:

- Register and log in.
- Report infrastructure problems.
- Upload photographs.
- Provide issue locations.
- Track their submitted reports.
- View resolution information.

### Administrator / Municipal Officer

Administrators can:

- View submitted reports.
- Verify issues.
- Assign priority.
- Assign departments and field staff.
- Monitor issue progress.
- View statistics and map-based information.

### Field Staff

Field staff can:

- View assigned issues.
- View issue details and location.
- Update issue progress.
- Add maintenance remarks.
- Upload resolution evidence.
- Mark issues as resolved.

---

## 5. Main Infrastructure Issues

The initial system will focus on a manageable set of issue types:

1. Potholes
2. Road damage
3. Broken streetlights
4. Damaged traffic signs

The system can be extended to support additional infrastructure
categories in future versions.

---

## 6. Existing Approach

Infrastructure issues may be communicated through different channels
or informal reporting methods.

Depending on the situation, citizens may provide information through
methods such as:

- Informal communication
- Separate complaint systems
- Phone-based reporting
- Other disconnected channels

These approaches may not provide one centralized workflow for
reporting, verification, assignment, progress tracking, and
resolution.

---

## 7. Problems with Existing Approach

The main problems identified are:

### Lack of Centralization

Reports may be distributed across different channels instead of
being maintained in one system.

### Incomplete Information

A complaint may not contain sufficient evidence, location details,
or issue classification.

### Difficulty in Prioritization

Authorities may receive many reports and need a systematic way to
identify which issues should receive attention first.

### Assignment Difficulties

Reports need to be assigned to the appropriate department and field
staff.

### Limited Status Visibility

Citizens may not know whether their report has been reviewed,
assigned, or resolved.

### Limited Data Analysis

Without structured data, it is difficult to identify frequently
affected areas, common issue types, and resolution patterns.

---

## 8. Proposed Domain Workflow

The proposed system provides a centralized workflow:

Citizen Reports Issue
        ↓
Issue Stored in Database
        ↓
Administrator Reviews Issue
        ↓
Issue Verified
        ↓
Priority Assigned
        ↓
Department / Field Staff Assigned
        ↓
Maintenance Work
        ↓
Status Updated
        ↓
Resolution Evidence Added
        ↓
Issue Resolved
        ↓
Citizen Tracks Final Status

This creates a complete digital workflow from reporting to
resolution.

---

## 9. Data Used by the System

The system will work with structured and user-generated data.

### User Data

- User ID
- Name
- Email
- Role
- Account information

### Issue Data

- Issue ID
- Issue type
- Description
- Priority
- Status
- Date and time

### Location Data

- Latitude
- Longitude
- Address

### Image Data

- Infrastructure photographs
- Image references
- Upload information

### Assignment Data

- Department
- Field staff
- Assignment date
- Completion date

### Status Data

- Current status
- Previous status
- Status change time
- Remarks

This data will support both application functionality and future
analytics.

---

## 10. Data Science Opportunities

The collected issue data can be used for basic data analysis.

Possible analytics include:

- Most frequently reported issue types.
- Number of issues by area.
- Number of pending issues.
- Number of resolved issues.
- Average issue resolution time.
- Priority distribution.
- Department-wise workload.
- Areas with repeated infrastructure problems.

These analytics can help administrators understand infrastructure
maintenance patterns.

---

## 11. Artificial Intelligence Opportunity

A future enhancement of the project will use computer vision to
analyze uploaded infrastructure images.

The planned workflow is:

Image Upload
        ↓
Image Processing
        ↓
AI-Based Detection
        ↓
Issue Classification
        ↓
Severity Estimation
        ↓
Priority Recommendation

For example, the system may assist in identifying whether an uploaded
image contains a pothole or road damage.

The AI output will be used as decision support for administrators.

The final verification and decision will remain with the authorized
administrator.

---

## 12. Third-Party Integration Opportunity

The project provides scope for integration with external services.

### Mapping Integration

Leaflet and OpenStreetMap can be used to display reported issues
according to their geographical locations.

### Future Notification Integration

A notification service can be considered for sending important issue
status updates to users.

The exact external service will be selected during the implementation
phase based on the project requirements and available options.

---

## 13. Why This Domain is Suitable for the Project

This domain is suitable because it combines:

- Real-world civic problems.
- Web application development.
- Database management.
- Role-based access control.
- Geographic information.
- Data analytics.
- Artificial intelligence opportunities.

The project also allows development to begin with a practical MVP
and add advanced features during later enhancement phases.

---

## 14. Initial Project Scope

The initial implementation will focus on:

- Citizen registration and login.
- Infrastructure issue reporting.
- Image upload.
- Location capture.
- Issue verification.
- Priority assignment.
- Department and field staff assignment.
- Status tracking.
- Resolution updates.
- Administrative dashboard.
- Map-based issue visualization.

Advanced AI functionality will be treated as a later enhancement.

---

## 15. Domain Limitations

The initial project will not attempt to:

- Integrate directly with every government system.
- Automatically repair physical infrastructure.
- Monitor every type of infrastructure.
- Provide nationwide infrastructure monitoring.
- Make fully autonomous decisions using AI.

The project will demonstrate a practical prototype that can later be
extended into a larger civic infrastructure management platform.
