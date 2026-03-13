import { Line } from "react-chartjs-2";

function TrafficChart({ traffic }) {

const data = {

labels: traffic.map(t => t.timestamp),

datasets: [
{
label: "Packet Size",
data: traffic.map(t => t.packet_size),
borderColor: "blue"
}
]

}

return <Line data={data} />

}

export default TrafficChart