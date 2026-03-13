import { useSocket } from "@/context/SocketContext";
import { ScrollArea } from "../ui/scroll-area";

const LiveTable = () => {
  const { packets } = useSocket();

 const getRowClass = (category) => {
  switch (category) {
    case "Known": return "border-l-2 border-l-neon-red bg-[hsl(348,100%,50%,0.04)]";
    case "Unknown": return "border-l-2 border-l-neon-orange bg-[hsl(33,100%,50%,0.04)]";
    default: return "border-l-2 border-l-neon-green bg-[hsl(160,100%,50%,0.02)]";
  }
};

const getCategoryBadge = (category) => {
  switch (category) {
    case "Known": return "bg-neon-red/20 text-neon-red";
    case "Unknown": return "bg-neon-orange/20 text-neon-orange";
    default: return "bg-neon-green/20 text-neon-green";
  }
};

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-foreground mb-3 tracking-wider flex items-center gap-2">
        <span className="h-2 w-2 rounded-full bg-neon-green animate-pulse-neon" />
        LIVE PACKET MONITOR
      </h3>
      <ScrollArea className="h-[320px] scrollbar-cyber">
        <table className="w-full text-xs font-mono">
          <thead>
            <tr className="text-muted-foreground border-b border-border/50">
              <th className="text-left py-2 px-2">Time</th>
              <th className="text-left py-2 px-2">Source</th>
              <th className="text-left py-2 px-2">Destination</th>
              <th className="text-left py-2 px-2">Attack</th>
              <th className="text-left py-2 px-2">Category</th>
              <th className="text-left py-2 px-2">Conf.</th>
              <th className="text-left py-2 px-2">Model</th>
            </tr>
          </thead>
          <tbody>
            {packets.slice(0, 50).map((pkt) => (
              <tr key={pkt.id} className={`border-b border-border/20 hover:bg-secondary/30 transition-colors ${getRowClass(pkt.attack_category)}`}>
                <td className="py-1.5 px-2 text-muted-foreground">{pkt.timestamp.split(" ")[1] || pkt.timestamp}</td>
                <td className="py-1.5 px-2">{pkt.source_ip}</td>
                <td className="py-1.5 px-2">{pkt.destination_ip}</td>
                <td className="py-1.5 px-2 text-foreground">{pkt.attack_name}</td>
                <td className="py-1.5 px-2">
                  <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${getCategoryBadge(pkt.attack_category)}`}>
                    {pkt.attack_category}
                  </span>
                </td>
                <td className="py-1.5 px-2">{Math.round(pkt.confidence * 100)}%</td>
                <td className="py-1.5 px-2 text-muted-foreground">{pkt.model}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </ScrollArea>
    </div>
  );
};

export default LiveTable;
