import { useSocket } from "@/context/SocketContext";
import { AlertTriangle } from "lucide-react";

const AlertsView = () => {
  const { packets } = useSocket();
  const threats = packets.filter((p) => p.prediction !== 0).slice(0, 50);

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-foreground mb-3 tracking-wider flex items-center gap-2">
        <AlertTriangle className="h-4 w-4 text-neon-red" />
        THREAT LOG ({threats.length})
      </h3>
      <div className="space-y-2 max-h-[500px] overflow-y-auto scrollbar-cyber">
        {threats.length === 0 && (
          <p className="text-xs text-muted-foreground py-8 text-center">No threats detected yet</p>
        )}
        {threats.map((t) => (
          <div
            key={t.id}
            className={`p-3 rounded border text-xs font-mono ${
              t.attack_category === "Known"
                ? "border-neon-red/30 bg-[hsl(348,100%,50%,0.05)]"
                : "border-neon-orange/30 bg-[hsl(33,100%,50%,0.05)]"
            }`}
          >
            <div className="flex justify-between">
              <span className={t.attack_category === "Known" ? "text-neon-red" : "text-neon-orange"}>
                {t.attack_name}
              </span>
              <span className="text-muted-foreground">{t.timestamp}</span>
            </div>
            <p className="text-muted-foreground mt-1">
              {t.source_ip} → {t.destination_ip} | {t.model} ({Math.round(t.confidence * 100)}%)
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertsView;
