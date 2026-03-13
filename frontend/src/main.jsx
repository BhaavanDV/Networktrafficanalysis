import React from "react";
import ReactDOM from "react-dom/client";
import LiveDashboard from "./components/LiveDashboard";
import "./index.css";   // important for Tailwind styles

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <LiveDashboard />
  </React.StrictMode>
);