import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, X } from "lucide-react";
import { useSocket } from "@/context/SocketContext";

const AlertPopup = () => {
  const { alerts, dismissAlert } = useSocket();

  return (
    <div className="fixed top-20 right-0 z-50 flex flex-col items-end gap-3 p-4 pointer-events-none">
      <AnimatePresence>
        {alerts.map((alert) => {
          const { attack_name, attack_category, model, source_ip, destination_ip, timestamp, confidence, accuracy } = alert.packet;
          const isKnown = attack_category === "Known";

          const borderClass = isKnown
            ? "border-neon-red neon-glow-red"
            : "border-neon-orange neon-glow-orange";
          const textClass = isKnown
            ? "text-neon-red neon-text-red"
            : "text-neon-orange";
          const bgClass = isKnown
            ? "bg-[hsl(348,100%,50%,0.08)]"
            : "bg-[hsl(33,100%,50%,0.08)]";

          // Calculate accuracy display
          let displayAccuracy = 0;
          if (typeof accuracy === "number") {
            displayAccuracy = Math.round(accuracy);
          } else if (typeof confidence === "number") {
            displayAccuracy = Math.round(confidence * 100);
          }

          // Determine color for accuracy bar
          const accuracyColor = displayAccuracy > 75
            ? "bg-neon-green"
            : displayAccuracy > 50
            ? "bg-neon-yellow"
            : "bg-neon-red";

          return (
            <motion.div
              key={alert.id}
              initial={{ x: 400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 400, opacity: 0 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className={`pointer-events-auto glass-card border ${borderClass} ${bgClass} p-4 rounded-lg w-80 shadow-lg`}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <AlertTriangle className={`h-5 w-5 ${textClass} animate-pulse-neon`} />
                  <span className={`font-bold text-sm tracking-wider ${textClass}`}>
                    ⚠ ATTACK DETECTED
                  </span>
                </div>
                <button
                  onClick={() => dismissAlert(alert.id)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              {/* Details */}
              <div className="space-y-1 font-mono text-xs text-muted-foreground">
                <p>Attack Type: <span className="text-foreground">{attack_name}</span></p>
                <p>Category: <span className={textClass}>{attack_category} Attack</span></p>
                <p>Model: <span className="text-foreground">{model}</span></p>
                <p>Source: <span className="text-foreground">{source_ip}</span></p>
                <p>Dest: <span className="text-foreground">{destination_ip}</span></p>
                <p>Time: <span className="text-foreground">{timestamp}</span></p>

                {/* Accuracy bar */}
                <div className="mt-2">
                  <p className="text-xs font-semibold mb-1 text-foreground">Accuracy: {displayAccuracy}%</p>
                  <div className="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className={`h-2 ${accuracyColor} rounded-full`}
                      style={{ width: `${displayAccuracy}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
};

export default AlertPopup;