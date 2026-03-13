import React from "react";
import LiveTable from "./components/LiveTable";
import LivePackets from "./components/LivePackets";
import TrafficDashboard from "../src_backup/TrafficDashboard";
import LiveDashboard from "./components/LiveDashboard";
import LiveTable from "./components/LiveTable";
import "./styles/dashboard.css";

function App() {
  return (
    <div className="App">

      <h1>AI Network Traffic Analyzer</h1>

      <LiveDashboard />

      <div className="dashboard-grid">

        <div className="card">
          <TrafficDashboard />
        </div>

        <div className="card">
          <LivePackets />z
        </div>

        <div className="card full-width">
          <LiveTable />
        </div>

      </div>

    </div>
  );
}

export default App;