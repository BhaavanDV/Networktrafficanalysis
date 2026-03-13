import { useSocket } from "@/context/SocketContext";
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";

const AccuracyGauge = () => {
  const { packets } = useSocket();

  const latestAccuracy = packets.length > 0
    ? Math.round(packets[0].accuracy * 100)
    : 0;

  const avgAccuracy = packets.length > 0
    ? Math.round(
        (packets.slice(0, 20).reduce((s, p) => s + p.accuracy, 0) /
          Math.min(packets.length, 20)) *
          100
      )
    : 0;

  const data = [{ name: "Accuracy", value: avgAccuracy, fill: "hsl(183,100%,50%)" }];

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-foreground mb-3 tracking-wider">
        ML MODEL ACCURACY
      </h3>
      <div className="relative">
        <ResponsiveContainer width="100%" height={180}>
          <RadialBarChart
            cx="50%"
            cy="50%"
            innerRadius="60%"
            outerRadius="90%"
            startAngle={180}
            endAngle={0}
            data={data}
            barSize={12}
          >
            <RadialBar
              dataKey="value"
              cornerRadius={6}
              background={{ fill: "hsl(222,30%,14%)" }}
            />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center pt-4">
          <span className="text-3xl font-bold text-primary neon-text-blue font-mono">
            {avgAccuracy}%
          </span>
          <span className="text-[10px] text-muted-foreground mt-1">
            Latest: {latestAccuracy}% | Model: {packets[0]?.model || "N/A"}
          </span>
        </div>
      </div>
    </div>
  );
};

export default AccuracyGauge;
