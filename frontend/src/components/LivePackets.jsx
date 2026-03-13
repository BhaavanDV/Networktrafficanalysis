import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export default function LivePackets() {
  const [packets, setPackets] = useState([]);
  const MAX_PACKETS = 50;

  useEffect(() => {
    const socket = io("http://localhost:8000"); // Correct port

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
    <div style={{ padding: "20px" }}>
      <h2>Live Packet Predictions</h2>
      <ul>
        {packets.map((p, idx) => (
          <li
            key={idx}
            style={{
              color: p.prediction !== 0 ? "red" : "green",
              fontWeight: p.prediction !== 0 ? "bold" : "normal",
            }}
          >
            {p.timestamp || "-"} | {p.src_ip || "-"} → {p.dst_ip || "-"} | Protocol: {p.protocol || "-"} | Prediction:{" "}
            {p.prediction === 0 ? "Normal" : "Abnormal"}
          </li>
        ))}
      </ul>
    </div>
  );
}