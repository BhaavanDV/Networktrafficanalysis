import { useEffect, useState } from "react";

function TrafficDashboard() {

  const [packets, setPackets] = useState([]);

  useEffect(() => {

    const fetchTraffic = async () => {
      try {
        const res = await fetch("http://localhost:5050/traffic");
        const data = await res.json();
        setPackets(data);
      } catch (err) {
        console.error("Error fetching traffic:", err);
      }
    };

    fetchTraffic();

    const interval = setInterval(fetchTraffic, 1000);

    return () => clearInterval(interval);

  }, []);

  return (
    <div>

      <h2>Live Network Traffic</h2>

      <table border="1">
        <thead>
          <tr>
            <th>Time</th>
            <th>Source IP</th>
            <th>Destination</th>
            <th>Country</th>
            <th>Protocol</th>
            <th>Port</th>
            <th>Size</th>
            <th>Status</th>
            <th>Port Scan</th>
            <th>DDoS</th>
          </tr>
        </thead>

        <tbody>
          {packets.map((packet, index) => (
            <tr key={index}>
              <td>{packet.timestamp}</td>
              <td>{packet.src_ip}</td>
              <td>{packet.dst_ip}</td>
              <td>{packet.country}</td>
              <td>{packet.protocol}</td>
              <td>{packet.port}</td>
              <td>{packet.packet_size}</td>

              <td>
                {packet.prediction === 0 ? "Normal" : "Attack"}
              </td>

              <td>
                {packet.port_scan ? "Yes" : "No"}
              </td>

              <td>
                {packet.ddos ? "Yes" : "No"}
              </td>

            </tr>
          ))}
        </tbody>

      </table>

    </div>
  );
}

export default TrafficDashboard;