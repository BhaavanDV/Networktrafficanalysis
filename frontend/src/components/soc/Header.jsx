import { Shield, Wifi, WifiOff } from "lucide-react";
import { useSocket } from "@/context/SocketContext";

const Header = () => {
  const { connected, stats } = useSocket();

  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-border/50 bg-card/40 backdrop-blur-xl">
      <div className="flex items-center gap-3">
        <Shield className="h-6 w-6 text-primary neon-text-blue" />
        <h1 className="text-lg font-bold tracking-wider text-foreground">
          Network Traffic <span className="text-primary neon-text-blue">Analysis</span> Using ML
        </h1>
      </div>

      <div className="flex items-center gap-6 text-sm">
        <div className="flex items-center gap-4 font-mono text-xs text-muted-foreground">
          <span>Packets: <span className="text-foreground">{stats.totalPackets}</span></span>
          <span>Threats: <span className="text-neon-red">{stats.knownAttacks + stats.unknownAttacks}</span></span>
        </div>

        <div className="flex items-center gap-2">
          {connected ? (
            <>
              <Wifi className="h-4 w-4 text-neon-green" />
              <span className="text-neon-green text-xs font-medium flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-neon-green animate-pulse-neon" />
                CONNECTED
              </span>
            </>
          ) : (
            <>
              <WifiOff className="h-4 w-4 text-neon-orange" />
              <span className="text-neon-orange text-xs font-medium flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-neon-orange animate-pulse-neon" />
                DEMO MODE
              </span>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;