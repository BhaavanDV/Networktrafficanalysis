import { useState } from "react";
import { useSocket } from "@/context/SocketContext";
import { FlaskConical } from "lucide-react";

const TestPanel = () => {
  const { injectPacket } = useSocket();
  const [form, setForm] = useState({
    attack_name: "DDoS",
    confidence: "0.97",
    source_ip: "192.168.1.10",
    destination_ip: "8.8.8.8",
    model: "RandomForest",
    attack_category: "Known",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    injectPacket({
      timestamp: new Date().toISOString().replace("T", " ").slice(0, 19),
      source_ip: form.source_ip,
      destination_ip: form.destination_ip,
      attack_name: form.attack_name,
      attack_category: form.attack_category,
      prediction: form.attack_category === "Normal" ? 0 : 1,
      confidence: parseFloat(form.confidence),
      model: form.model,
      accuracy: 0.94,
    });
  };

  const update = (key, val) => setForm((p) => ({ ...p, [key]: val }));

  const inputClass =
    "w-full bg-secondary/60 border border-border/50 rounded px-3 py-2 text-xs font-mono text-foreground focus:outline-none focus:border-primary";

  return (
    <div className="glass-card p-6 max-w-lg">
      <h3 className="text-sm font-semibold text-foreground mb-4 tracking-wider flex items-center gap-2">
        <FlaskConical className="h-4 w-4 text-primary" />
        ALERT TEST PANEL
      </h3>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-[10px] text-muted-foreground mb-1 block">Attack Type</label>
          <input className={inputClass} value={form.attack_name} onChange={(e) => update("attack_name", e.target.value)} />
        </div>
        <div>
          <label className="text-[10px] text-muted-foreground mb-1 block">Category</label>
          <select className={inputClass} value={form.attack_category} onChange={(e) => update("attack_category", e.target.value)}>
            <option value="Known">Known</option>
            <option value="Unknown">Unknown</option>
            <option value="Normal">Normal</option>
          </select>
        </div>
        <div>
          <label className="text-[10px] text-muted-foreground mb-1 block">Source IP</label>
          <input className={inputClass} value={form.source_ip} onChange={(e) => update("source_ip", e.target.value)} />
        </div>
        <div>
          <label className="text-[10px] text-muted-foreground mb-1 block">Destination IP</label>
          <input className={inputClass} value={form.destination_ip} onChange={(e) => update("destination_ip", e.target.value)} />
        </div>
        <div>
          <label className="text-[10px] text-muted-foreground mb-1 block">Confidence</label>
          <input className={inputClass} value={form.confidence} onChange={(e) => update("confidence", e.target.value)} />
        </div>
        <div>
          <label className="text-[10px] text-muted-foreground mb-1 block">Model</label>
          <input className={inputClass} value={form.model} onChange={(e) => update("model", e.target.value)} />
        </div>
        <div className="col-span-2">
          <button
            type="submit"
            className="w-full py-2 rounded bg-primary text-primary-foreground font-semibold text-xs tracking-wider hover:opacity-90 transition-opacity"
          >
            GENERATE ALERT
          </button>
        </div>
      </form>
    </div>
  );
};

export default TestPanel;