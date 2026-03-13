import Header from "../components/soc/Header";
import SOCSidebar from "../components/soc/SOCSidebar";
import TrafficChart from "../components/soc/TrafficChart";
import LiveTable from "../components/soc/LiveTable";
import AlertsView from "../components/soc/AlertsView";
import AttackPieChart from "../components/soc/AttackPieChart";
import AccuracyGauge from "../components/soc/AccuracyGauge";
import ModelsView from "../components/soc/ModelsView";
import TestPanel from "../components/soc/TestPanel";

function Index() {
  return (
    <div className="flex">

      <SOCSidebar />

      <div className="flex-1 p-4">

        <Header />

        <div className="grid grid-cols-2 gap-4 mt-4">
          <TrafficChart />
          <AttackPieChart />
        </div>

        <div className="mt-4">
          <LiveTable />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <AlertsView />
          <AccuracyGauge />
        </div>

        <div className="mt-4">
          <ModelsView />
        </div>

        <div className="mt-4">
          <TestPanel />
        </div>

      </div>
    </div>
  );
}

export default Index;
