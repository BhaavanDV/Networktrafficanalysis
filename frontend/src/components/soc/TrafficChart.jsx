import { useSocket } from "@/context/SocketContext";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const TrafficChart = () => {
  const { stats } = useSocket();

  const data = stats.packetsPerSecond.map((val, i) => ({
    time: `${i}s`,
    pps: val,
  }));

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-foreground mb-3 tracking-wider">
        PACKETS PER SECOND
      </h3>
      <ResponsiveContainer width="100%" height={180}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(222,30%,18%)" />
          <XAxis dataKey="time" tick={{ fill: "hsl(215,20%,55%)", fontSize: 10 }} />
          <YAxis tick={{ fill: "hsl(215,20%,55%)", fontSize: 10 }} />
          <Tooltip
            contentStyle={{
              background: "hsl(222,40%,10%)",
              border: "1px solid hsl(222,30%,18%)",
              borderRadius: 8,
              fontSize: 12,
            }}
          />
          <Line
            type="monotone"
            dataKey="pps"
            stroke="hsl(183,100%,50%)"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrafficChart;
