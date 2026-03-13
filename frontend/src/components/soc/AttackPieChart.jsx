import { useSocket } from "@/context/SocketContext";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const COLORS = [
  "hsl(348,100%,50%)",
  "hsl(33,100%,50%)",
  "hsl(160,100%,50%)",
];

const AttackPieChart = () => {
  const { stats } = useSocket();

  const data = [
    { name: "Known", value: stats.knownAttacks || 1 },
    { name: "Unknown", value: stats.unknownAttacks || 1 },
    { name: "Normal", value: stats.normalTraffic || 1 },
  ];

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-foreground mb-3 tracking-wider">
        ATTACK DISTRIBUTION
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={75}
            dataKey="value"
            stroke="none"
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: "hsl(222,40%,10%)",
              border: "1px solid hsl(222,30%,18%)",
              borderRadius: 8,
              fontSize: 12,
            }}
          />
          <Legend
            wrapperStyle={{ fontSize: 11, color: "hsl(215,20%,55%)" }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AttackPieChart;
