# Domain Study

## 1. Domain Overview

The project belongs to the Civic Technology and Smart City domain,
with an Artificial Intelligence and Data Science component.

Public infrastructure includes facilities and assets that support
daily life in a community, such as roads, streetlights, traffic
signs, drainage systems, public spaces, and other municipal assets.

Effective maintenance of these facilities requires timely reporting,
proper categorization, prioritization, assignment, monitoring, and
resolution of infrastructure problems.

The proposed project focuses on creating a centralized digital
platform for reporting and managing public infrastructure issues.


## 2. Problem Context

Public infrastructure problems can occur frequently because of
weather conditions, regular usage, accidents, aging infrastructure,
or insufficient maintenance.

Examples include:

- Potholes on roads
- Damaged road surfaces
- Broken streetlights
- Damaged traffic signs

When citizens notice such problems, reporting may happen through
different channels or may not happen at all.

Even when a problem is reported, the reporting process may not provide
a convenient way for citizens to submit photographs, precise
locations, or additional information.

Authorities also need to organize reports, determine which issues
require urgent attention, assign responsible personnel, and track
whether the problem has been resolved.


## 3. Target Stakeholders

The main stakeholders of the proposed system are:

### Citizens

Citizens identify infrastructure problems and submit reports through
the application.

They provide:

- Issue category
- Description
- Photograph
- Location

They can also track the progress of their submitted reports.

### Administrators / Municipal Officers

Administrators are responsible for reviewing and managing reported
issues.

They can:

- Review reports
- Verify issues
- Assign priorities
- Assign departments or field staff
- Monitor progress
- View infrastructure statistics

### Field Staff

Field staff handle the physical inspection and maintenance work.

They can:

- View assigned issues
- Access issue information and location
- Update progress
- Add remarks
- Upload resolution evidence
- Mark issues as resolved


## 4. Major Infrastructure Issues Covered

The initial version of the system will focus on a limited set of
infrastructure issues to keep the project practical and achievable
within the capstone timeline.

### 1. Potholes

Potholes can create safety risks for vehicles, motorcycles, cyclists,
and pedestrians.

### 2. Road Damage

Damaged road surfaces may affect transportation and can worsen if
maintenance is delayed.

### 3. Broken Streetlights

Non-functional streetlights can reduce visibility and create safety
concerns, particularly during nighttime.

### 4. Damaged Traffic Signs

Damaged or missing traffic signs can affect road safety and
navigation.

Additional infrastructure categories may be considered in future
versions but are outside the initial project scope.


## 5. Existing Problem Workflow

A simplified traditional workflow can be represented as:

Citizen Notices Issue
        ↓
Reports Through Available Channel
        ↓
Complaint Reaches Authority
        ↓
Issue Reviewed
        ↓
Responsible Department Identified
        ↓
Maintenance Staff Assigned
        ↓
Issue Inspected
        ↓
Repair Work Performed
        ↓
Issue Resolved

The process can become inefficient when reporting, assignment,
communication, and tracking are handled through disconnected
channels.


## 6. Problems in the Existing Process

The proposed system addresses several common challenges:

### Fragmented Reporting

Infrastructure issues may be reported through different channels,
making centralized monitoring difficult.

### Lack of Evidence

A report without a photograph or sufficient description may make it
difficult for authorities to understand the issue before inspection.

### Inaccurate Location Information

If an exact location is not provided, field staff may spend
additional time identifying the reported problem.

### Difficulty in Prioritization

Multiple complaints may exist simultaneously, making it necessary
to determine which issues should receive attention first.

### Limited Status Visibility

Citizens may not have a clear way to know whether their complaint
has been reviewed, assigned, or resolved.

### Manual Monitoring

Authorities may need to manually organize and track a large number
of complaints.

### Lack of Historical Analytics

Without structured data, it can be difficult to identify areas with
repeated infrastructure problems or analyze resolution performance.


## 7. Proposed Digital Workflow

The proposed system introduces a centralized workflow:

Citizen
    ↓
Create Infrastructure Report
    ↓
Upload Photograph + Location
    ↓
System Stores Report
    ↓
Administrator Reviews Report
    ↓
Issue Verified
    ↓
Priority Assigned
    ↓
Department / Field Staff Assigned
    ↓
Field Staff Performs Maintenance
    ↓
Status Updated
    ↓
Resolution Evidence Uploaded
    ↓
Issue Closed
    ↓
Citizen Can View Final Status


## 8. Information and Data Used

The system will work with different types of data.

### User Data

- Name
- Email
- Password hash
- User role

### Issue Data

- Issue type
- Description
- Priority
- Status
- Creation date
- Update date

### Location Data

- Latitude
- Longitude
- Address

### Image Data

- Infrastructure photographs
- Resolution photographs

### Operational Data

- Assigned department
- Assigned field staff
- Status history
- Remarks
- Resolution information

This structured information can later support analytics and
machine learning.


## 9. Role of Maps and Location Services

Location is an important part of infrastructure issue management.

The system will use geographical coordinates to identify the
location of reported problems.

An interactive map can allow administrators to:

- View reported issues geographically.
- Identify areas with multiple complaints.
- Understand the distribution of infrastructure problems.
- Locate field work more efficiently.

The planned mapping technology is Leaflet with OpenStreetMap.


## 10. AI Opportunity

Artificial Intelligence will be introduced as a later enhancement
rather than being the foundation of the initial application.

The planned AI feature is an image-based infrastructure issue
detection and prioritization module.

### Proposed AI Workflow

Citizen Uploads Image
        ↓
Image Preprocessing
        ↓
Computer Vision Model
        ↓
Infrastructure Issue Detection
        ↓
Issue Classification
        ↓
Severity Estimation
        ↓
Priority Recommendation


### Possible AI Applications

The AI component may assist with:

- Pothole detection
- Road damage detection
- Infrastructure issue classification
- Image-based severity estimation
- Priority recommendation

The AI output will act as decision support for administrators.
Final decisions will remain under human control.


## 11. Data Science Opportunities

The structured issue data can also support future analytics.

Possible analytical features include:

- Number of reported issues
- Number of resolved issues
- Average resolution time
- Issue distribution by category
- Issue distribution by location
- High-priority issue trends
- Frequently affected areas
- Department performance statistics
- Monthly issue trends

These analytics can help authorities understand infrastructure
maintenance patterns.


## 12. Expected Benefits

### For Citizens

- Simple infrastructure issue reporting
- Ability to provide photographs and location
- Transparent status tracking
- Better visibility of resolution progress

### For Administrators

- Centralized issue management
- Better prioritization
- Easier assignment
- Map-based monitoring
- Infrastructure analytics

### For Field Staff

- Clear assignment information
- Accurate issue locations
- Better access to photographs and descriptions
- Digital progress updates
- Resolution evidence management


## 13. Expected Impact

The system aims to improve the overall infrastructure complaint
management process by providing a centralized platform connecting
citizens, administrators, and field staff.

The expected improvements include:

- Faster identification of reported issues
- Better organization of complaints
- Improved issue prioritization
- More transparent status tracking
- Better location-based monitoring
- Structured infrastructure data
- Data-driven maintenance insights
- AI-assisted issue detection and prioritization


## 14. Why This Domain Was Selected

Public infrastructure affects citizens directly and represents a
practical real-world problem suitable for a full-stack AI and Data
Science project.

The domain provides opportunities to combine:

- Full-stack web development
- REST APIs
- Relational databases
- Role-based authentication
- Geospatial data
- Data analytics
- Computer Vision
- Machine Learning
- Cloud deployment

The project can therefore demonstrate both software engineering
skills and AI/Data Science capabilities while maintaining a
realistic scope for a student capstone project.


## 15. Project Scope for the Capstone

The initial capstone implementation will focus on:

1. User authentication and role management.
2. Citizen infrastructure issue reporting.
3. Image upload.
4. Location capture.
5. Issue verification.
6. Priority management.
7. Department and field staff assignment.
8. Issue status tracking.
9. Resolution evidence.
10. Map-based monitoring.
11. Administrative dashboard.
12. Testing and deployment.

The AI-based image detection and prioritization feature will be
implemented during the later enhancement phase of the capstone.


## 16. Domain Conclusion

Public infrastructure issue management is a suitable domain for the
capstone because it combines a clearly identifiable real-world
problem with practical software and AI opportunities.

The proposed system provides a structured workflow for reporting,
verifying, prioritizing, assigning, resolving, and monitoring
infrastructure issues.

The addition of computer vision and data analytics can further
enhance the system while keeping human administrators involved in
the final decision-making process.