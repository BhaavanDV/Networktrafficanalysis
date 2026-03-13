import { io } from "socket.io-client";

const socket = io("http://localhost:8000"); // backend address

socket.on("connect", () => {
  console.log("Connected to NIDS backend:", socket.id);
});

socket.on("packet_prediction", (data) => {
  console.log("Live prediction received:", data);
  // You can now update your UI with this data
});

export default socket;