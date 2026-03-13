import React from "react";
import Header from "./soc/Header";
import SOCSidebar from "./soc/SOCSidebar";
import TrafficChart from "./soc/TrafficChart";
import LiveTable from "./soc/LiveTable";
import AlertsView from "./soc/AlertsView";
import AlertPopup from "./soc/AlertPopup";
import AttackPieChart from "./soc/AttackPieChart";
import AccuracyGauge from "./soc/AccuracyGauge";
import ModelsView from "./soc/ModelsView";
import TestPanel from "./soc/TestPanel";

import { SocketProvider } from "../context/SocketContext";

function LiveDashboard() {
  return (
    <SocketProvider>
      <div className="flex h-screen bg-[#0f172a] text-white">

        <SOCSidebar />

        <div className="flex flex-col flex-1 overflow-hidden">

          <Header />

          <div className="flex-1 overflow-y-auto p-4 space-y-6">

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <TrafficChart />
              <AttackPieChart />
            </div>

            <LiveTable />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <AlertsView />
              <AccuracyGauge />
            </div>

            <ModelsView />

            <TestPanel />

          </div>
        </div>

        <AlertPopup />

      </div>
    </SocketProvider>
  );
}

export default LiveDashboard;