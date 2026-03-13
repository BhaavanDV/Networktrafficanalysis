import { LayoutDashboard, Bell, BarChart3, Cpu, Settings, FlaskConical } from "lucide-react";
import { useState } from "react";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "alerts", label: "Alerts", icon: Bell },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
  { id: "models", label: "Models", icon: Cpu },
  { id: "test", label: "Test Panel", icon: FlaskConical },
  { id: "settings", label: "Settings", icon: Settings },
];

const SOCSidebar = ({ activeView, onViewChange }) => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`${collapsed ? "w-16" : "w-52"} transition-all duration-300 border-r border-border/50 bg-sidebar flex flex-col`}
    >
      <div className="flex-1 py-4">
        {navItems.map((item) => {
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                isActive
                  ? "text-primary bg-secondary/60 border-r-2 border-primary"
                  : "text-muted-foreground hover:text-foreground hover:bg-secondary/30"
              } ${collapsed ? "justify-center" : ""}`}
            >
              <item.icon className="h-4 w-4 flex-shrink-0" />
              {!collapsed && <span className="font-medium">{item.label}</span>}
            </button>
          );
        })}
      </div>

      <button
        onClick={() => setCollapsed(!collapsed)}
        className="p-4 text-muted-foreground hover:text-foreground text-xs border-t border-border/50"
      >
        {collapsed ? "»" : "« Collapse"}
      </button>
    </aside>
  );
};

export default SOCSidebar;