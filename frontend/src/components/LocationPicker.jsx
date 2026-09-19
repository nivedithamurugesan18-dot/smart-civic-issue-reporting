import { useEffect, useState } from "react";
import {
  MapContainer,
  Marker,
  TileLayer,
  useMap,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIconRetina from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

const DEFAULT_CENTER = [20.5937, 78.9629];
const DEFAULT_ZOOM = 5;

const marker = L.icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIconRetina,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

function MapClickHandler({ onLocationSelect }) {
  useMapEvents({
    click(event) {
      onLocationSelect({
        latitude: Number(event.latlng.lat.toFixed(6)),
        longitude: Number(event.latlng.lng.toFixed(6)),
      });
    },
  });

  return null;
}

function MapViewport({ position }) {
  const map = useMap();

  useEffect(() => {
    if (position) {
      map.setView(position, Math.max(map.getZoom(), 13));
    }
  }, [map, position]);

  return null;
}

export default function LocationPicker({
  latitude = null,
  longitude = null,
  onLocationSelect,
}) {
  const hasInitialLocation =
    latitude !== null &&
    latitude !== undefined &&
    longitude !== null &&
    longitude !== undefined;

  const initialPosition = hasInitialLocation
    ? [latitude, longitude]
    : null;

  const [selectedPosition, setSelectedPosition] = useState(
    initialPosition
  );

  const handleLocationSelect = (position) => {
    setSelectedPosition([
      position.latitude,
      position.longitude,
    ]);
    onLocationSelect(position);
  };

  return (
    <div className="location-picker">
      <MapContainer
        center={initialPosition || DEFAULT_CENTER}
        zoom={hasInitialLocation ? 13 : DEFAULT_ZOOM}
        scrollWheelZoom
        className="location-map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapClickHandler
          onLocationSelect={handleLocationSelect}
        />
        <MapViewport position={selectedPosition} />
        {selectedPosition && (
          <Marker
            position={selectedPosition}
            icon={marker}
          />
        )}
      </MapContainer>

      {selectedPosition ? (
        <div className="selected-coordinates">
          <strong>Selected coordinates</strong>
          <span>
            Latitude: {selectedPosition[0].toFixed(6)}
          </span>
          <span>
            Longitude: {selectedPosition[1].toFixed(6)}
          </span>
        </div>
      ) : (
        <p className="location-help">
          Click the map to select the issue location. This is optional.
        </p>
      )}
    </div>
  );
}
