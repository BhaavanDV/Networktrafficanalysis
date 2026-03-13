import { useSocket } from "../../context/SocketContext";
import { Cpu } from "lucide-react";

const ModelsView = () => {
  const { packets } = useSocket();

  // Use plain JS Map, no TypeScript types
  const modelMap = new Map();
  packets.forEach((p) => {
    const entry = modelMap.get(p.model) || { count: 0, totalAcc: 0, totalConf: 0 };
    entry.count++;
    entry.totalAcc += p.accuracy;
    entry.totalConf += p.confidence;
    modelMap.set(p.model, entry);
  });

  const models = Array.from(modelMap.entries()).map(([name, d]) => ({
    name,
    count: d.count,
    avgAccuracy: Math.round((d.totalAcc / d.count) * 100),
    avgConfidence: Math.round((d.totalConf / d.count) * 100),
  }));

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-foreground mb-3 tracking-wider flex items-center gap-2">
        <Cpu className="h-4 w-4 text-primary" />
        ML MODEL PERFORMANCE
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {models.map((m) => (
          <div key={m.name} className="glass-card p-4 border border-border/30">
            <p className="text-foreground font-semibold text-sm">{m.name}</p>
            <div className="mt-2 space-y-1 text-xs font-mono text-muted-foreground">
              <p>Packets: <span className="text-foreground">{m.count}</span></p>
              <p>Avg Accuracy: <span className="text-neon-green">{m.avgAccuracy}%</span></p>
              <p>Avg Confidence: <span className="text-primary">{m.avgConfidence}%</span></p>
            </div>
          </div>
        ))}
        {models.length === 0 && (
          <p className="text-xs text-muted-foreground py-8 text-center col-span-2">Waiting for data…</p>
        )}
      </div>
    </div>
  );
};

export default ModelsView;