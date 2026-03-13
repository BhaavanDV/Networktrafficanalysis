import React, { createContext, useContext, useEffect, useState, useRef, useCallback } from "react";
import { io } from "socket.io-client";

const SocketContext = createContext(null);

export const useSocket = () => {
  const ctx = useContext(SocketContext);
  if (!ctx) throw new Error("useSocket must be used within SocketProvider");
  return ctx;
};

const BACKEND_URL = "http://localhost:5000";
const MAX_PACKETS = 200;
const MAX_PPS_HISTORY = 30;

let idCounter = 0;
const genId = () => `pkt-${Date.now()}-${++idCounter}`;

export const SocketProvider = ({ children }) => {
  const [connected, setConnected] = useState(false);
  const [packets, setPackets] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({
    totalPackets: 0,
    knownAttacks: 0,
    unknownAttacks: 0,
    normalTraffic: 0,
    packetsPerSecond: [],
  });
  const ppsCount = useRef(0);
  const socketRef = useRef(null);

  const processPacket = useCallback((data) => {
    const packet = { ...data, id: genId() };

    setPackets((prev) => [packet, ...prev].slice(0, MAX_PACKETS));

    if (packet.prediction !== 0) {
      const alert = { id: genId(), packet, createdAt: Date.now() };
      setAlerts((prev) => [alert, ...prev].slice(0, 10));
    }

    ppsCount.current++;

    setStats((prev) => ({
      totalPackets: prev.totalPackets + 1,
      knownAttacks: prev.knownAttacks + (packet.attack_category === "Known" ? 1 : 0),
      unknownAttacks: prev.unknownAttacks + (packet.attack_category === "Unknown" ? 1 : 0),
      normalTraffic: prev.normalTraffic + (packet.prediction === 0 ? 1 : 0),
      packetsPerSecond: prev.packetsPerSecond,
    }));
  }, []);

  const dismissAlert = useCallback((id) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id));
  }, []);

  const injectPacket = useCallback((packet) => {
    processPacket(packet);
  }, [processPacket]);

  // PPS tracker
  useEffect(() => {
    const interval = setInterval(() => {
      setStats((prev) => ({
        ...prev,
        packetsPerSecond: [...prev.packetsPerSecond, ppsCount.current].slice(-MAX_PPS_HISTORY),
      }));
      ppsCount.current = 0;
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Auto-dismiss alerts after 6s
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setAlerts((prev) => prev.filter((a) => now - a.createdAt < 6000));
    }, 500);
    return () => clearInterval(interval);
  }, []);

  // Socket connection
  useEffect(() => {
    const socket = io(BACKEND_URL, {
      transports: ["websocket", "polling"],
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 2000,
    });
    socketRef.current = socket;

    socket.on("connect", () => {
      console.log("✅ Connected with socket id:", socket.id);
      setConnected(true);
    });

    socket.on("disconnect", () => setConnected(false));

    socket.on("traffic_update", (data) => {
      processPacket(data);
    });

    return () => {
      console.log("🛑 Socket disconnected on unmount");
      socket.disconnect();
      socketRef.current = null;
    };
  }, [processPacket]);

  // Demo data generator when not connected
  useEffect(() => {
    if (connected) return;

    const attackNames = ["Normal", "DDoS", "SQL Injection", "XSS", "Port Scan", "Brute Force", "Man-in-the-Middle"];
    const models = ["RandomForest", "XGBoost", "NeuralNet", "SVM"];
    const ips = ["192.168.1.10", "10.0.0.5", "172.16.0.1", "192.168.0.100", "10.10.1.50"];
    const destIps = ["8.8.8.8", "1.1.1.1", "204.79.197.200", "142.250.80.46", "93.184.216.34"];

    const interval = setInterval(() => {
      const isAttack = Math.random() > 0.5;
      const isKnown = Math.random() > 0.4;
      const attackIdx = isAttack ? Math.floor(Math.random() * (attackNames.length - 1)) + 1 : 0;

      processPacket({
        timestamp: new Date().toISOString().replace("T", " ").slice(0, 19),
        source_ip: ips[Math.floor(Math.random() * ips.length)],
        destination_ip: destIps[Math.floor(Math.random() * destIps.length)],
        attack_name: attackNames[attackIdx],
        attack_category: isAttack ? (isKnown ? "Known" : "Unknown") : "Normal",
        prediction: isAttack ? 1 : 0,
        confidence: Number((0.7 + Math.random() * 0.3).toFixed(2)),
        model: models[Math.floor(Math.random() * models.length)],
        accuracy: Number((0.85 + Math.random() * 0.14).toFixed(2)),
      });
    }, 800);

    return () => clearInterval(interval);
  }, [connected, processPacket]);

  return (
    <SocketContext.Provider value={{ connected, packets, alerts, dismissAlert, injectPacket, stats }}>
      {children}
    </SocketContext.Provider>
  );
};