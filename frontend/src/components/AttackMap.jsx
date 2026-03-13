import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";
import { Line } from "react-chartjs-2";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// Mock geo for IPs (replace with real geolocation if needed)
const IP_LOCATIONS = {
  "192.168.0.1": [12.9716, 77.5946], // Bangalore
  "10.0.0.2": [28.6139, 77.209],    // Delhi
  "172.16.0.3": [19.076, 72.8777],   // Mumbai
  "8.8.8.8": [37.3861, -122.0839],   // Google HQ
};

export default function AttackMap() {
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState({ labels: [], datasets: [{ label: "Packet Size", data: [] }] });

  useEffect(() => {
    const socket = io("http://127.0.0.1:8000"); // Must match backend port

    socket.on("traffic_update", (pkt) => {
      // If attack, add to alerts (keep last 20)
      if (pkt.prediction !== 0) {
        setAlerts((prev) => [pkt, ...prev].slice(0, 20));
      }

      // Update chart data (keep last 20 points)
      setChartData((prev) => {
        const newLabels = [...prev.labels, pkt.timestamp].slice(-20);
        const newData = [...prev.datasets[0].data, pkt.packet_size].slice(-20);
        return { labels: newLabels, datasets: [{ ...prev.datasets[0], data: newData }] };
      });
    });

    return () => socket.disconnect();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      {/* ALERT */}
      {alerts.length > 0 && (
        <div style={{ background: "red", color: "white", padding: "10px", marginBottom: "20px" }}>
          ⚠ Attack Detected from {alerts[0].src_ip}
        </div>
      )}

      {/* GRAPH */}
      <h2>Traffic Graph</h2>
      <Line data={chartData} />

      {/* MAP */}
      <h2>Attack Map</h2>
      <MapContainer center={[20, 0]} zoom={2} style={{ height: "400px" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {alerts.map((a, i) => (
          <Marker key={i} position={IP_LOCATIONS[a.src_ip] || [20, 0]}>
            <Popup>Attack from {a.src_ip}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}