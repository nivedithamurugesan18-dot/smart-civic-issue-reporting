import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import LocationPicker from "../components/LocationPicker";
import api from "../services/api";

const initialForm = {
  title: "",
  description: "",
  category: "road",
  priority: "medium",
  severity: "medium",
  location: "",
  latitude: null,
  longitude: null,
};

export default function ReportIssue() {
  const navigate = useNavigate();

  const [form, setForm] = useState(initialForm);
  const [selectedImages, setSelectedImages] = useState([]);
  const [createdIssueId, setCreatedIssueId] = useState(null);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleImageChange = (e) => {
    setSelectedImages(Array.from(e.target.files || []));
  };

  const handleLocationSelect = ({ latitude, longitude }) => {
    setForm((currentForm) => ({
      ...currentForm,
      latitude,
      longitude,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setCreatedIssueId(null);
    setLoading(true);

    try {
      const issueResponse = await api.post(
        "/issues/",
        form
      );

      const createdIssue = issueResponse.data;
      const uploadResults = await Promise.allSettled(
        selectedImages.map((image) => {
          const imageData = new FormData();
          imageData.append("file", image);

          return api.post(
            `/issues/${createdIssue.id}/images`,
            imageData
          );
        })
      );

      const failedUploads = uploadResults.filter(
        (result) => result.status === "rejected"
      );

      if (failedUploads.length > 0) {
        setCreatedIssueId(createdIssue.id);
        setError(
          `Issue #${createdIssue.id} was created, but ` +
          `${failedUploads.length} photo(s) failed to upload.`
        );
        return;
      }

      navigate(`/issues/${createdIssue.id}`);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to report issue"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">

      <div className="form-card">

        <h1>Report Civic Issue</h1>

        <form onSubmit={handleSubmit}>

          <label>Title</label>
          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="Example: Street light damaged"
            required
          />

          <label>Description</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="Describe the problem"
            required
          />

          <label>Category</label>
          <select
            name="category"
            value={form.category}
            onChange={handleChange}
          >
            <option value="road">Road</option>
            <option value="street_light">
              Street Light
            </option>
            <option value="waste">Waste</option>
            <option value="water">Water</option>
            <option value="traffic">Traffic</option>
            <option value="other">Other</option>
          </select>

          <label>Priority</label>
          <select
            name="priority"
            value={form.priority}
            onChange={handleChange}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <label>Severity</label>
          <select
            name="severity"
            value={form.severity}
            onChange={handleChange}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <label>Location</label>
          <input
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="Example: Main Road, Trichy"
          />

          <label>Location on Map</label>
          <LocationPicker
            latitude={form.latitude}
            longitude={form.longitude}
            onLocationSelect={handleLocationSelect}
          />

          <label htmlFor="evidencePhotos">
            Evidence Photos
          </label>
          <input
            id="evidencePhotos"
            type="file"
            accept="image/jpeg,image/png,image/webp"
            multiple
            onChange={handleImageChange}
            disabled={loading}
          />

          {selectedImages.length > 0 && (
            <div className="selected-files">
              <strong>Selected photos</strong>
              <ul>
                {selectedImages.map((image) => (
                  <li key={`${image.name}-${image.lastModified}`}>
                    {image.name}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {error && (
            <div className="error">
              {error}
              {createdIssueId && (
                <p>
                  <Link to={`/issues/${createdIssueId}`}>
                    View the created issue
                  </Link>
                </p>
              )}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Submitting..."
              : "Submit Issue"}
          </button>

        </form>

      </div>

    </div>
  );
}
