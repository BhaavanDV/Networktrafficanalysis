import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export default function TrafficDashboard() {
  const [packets, setPackets] = useState([]);
  const MAX_PACKETS = 50;

  useEffect(() => {
    const socket = io("http://localhost:5050"); // Correct port

    const handlePacket = (packet) => {
      setPackets((prev) => [packet, ...prev].slice(0, MAX_PACKETS));
    };

    socket.on("traffic_update", handlePacket);
    socket.on("connect_error", (err) => console.error("Socket.IO connect error:", err));

    return () => {
      socket.off("traffic_update", handlePacket);
      socket.disconnect();
    };
  }, []);

  return (
    <div>
      <h2>Live Network Traffic</h2>
      <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Time</th>
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>Protocol</th>
            <th>Size</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {packets.map((packet, index) => (
            <tr key={index} style={{ background: packet.prediction !== 0 ? "#ffe6e6" : "transparent" }}>
              <td>{packet.timestamp || "-"}</td>
              <td>{packet.src_ip || "-"}</td>
              <td>{packet.dst_ip || "-"}</td>
              <td>{packet.protocol || "-"}</td>
              <td>{packet.packet_size || "-"}</td>
              <td>{packet.prediction === 0 ? "Normal" : "Attack"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}