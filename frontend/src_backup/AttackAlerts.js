function AttackAlerts({ traffic }) {

const attacks = traffic.filter(t => t.prediction === 1)

return (

<div>

<h2>⚠️ Attack Alerts</h2>

{attacks.map((a,i) => (

<p key={i} style={{color:"red"}}>

Attack from {a.src_ip} ({a.country})

</p>

))}

</div>

)

}

export default AttackAlerts