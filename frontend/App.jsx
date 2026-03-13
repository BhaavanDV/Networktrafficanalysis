import { useEffect, useRef } from 'react'
import { TrafficProvider, useTraffic } from './context/TrafficContext'
import { useTrafficStream } from './hooks/useTrafficStream'
import Sidebar    from './components/layout/Sidebar'
import Header     from './components/layout/Header'
import AlertPopup from './components/alerts/AlertPopup'
import Dashboard  from './pages/Dashboard'

/* ─────────────────────────────────────────────────────────────────
   MOCK DATA INJECTOR
   Simulates the Flask backend when no real server is running.
   Remove this component (and its usage) in production.
───────────────────────────────────────────────────────────────── */
const ATTACK_POOL = [
  { attack_name:'SYN Flood',        attack_category:'Known',   detection_method:'Supervised'   },
  { attack_name:'UDP Flood',         attack_category:'Known',   detection_method:'Supervised'   },
  { attack_name:'DDoS HTTP',         attack_category:'Known',   detection_method:'Supervised'   },
  { attack_name:'Port Scan',         attack_category:'Known',   detection_method:'Supervised'   },
  { attack_name:'Brute Force SSH',   attack_category:'Known',   detection_method:'Supervised'   },
  { attack_name:'SQL Injection',     attack_category:'Known',   detection_method:'Supervised'   },
  { attack_name:'Zero-Day Exploit',  attack_category:'Unknown', detection_method:'Unsupervised' },
  { attack_name:'Encrypted C2',      attack_category:'Unknown', detection_method:'Unsupervised' },
  { attack_name:'Anomalous Pattern', attack_category:'Unknown', detection_method:'Unsupervised' },
  { attack_name:'Normal HTTP',       attack_category:'Normal',  detection_method:'Supervised'   },
  { attack_name:'Normal DNS',        attack_category:'Normal',  detection_method:'Supervised'   },
  { attack_name:'Normal HTTPS',      attack_category:'Normal',  detection_method:'Supervised'   },
]
const PROTOCOLS = ['TCP','UDP','ICMP','HTTP','HTTPS','DNS','FTP','SMTP']
const rndIp = () => `${r(10,220)}.${r(0,255)}.${r(0,255)}.${r(1,254)}`
const r     = (a,b) => Math.floor(Math.random()*(b-a+1))+a
const uid   = () => Math.random().toString(36).slice(2,10).toUpperCase()

function MockInjector() {
  const { setConnected, addPacket } = useTraffic()
  const iv = useRef(null)

  useEffect(() => {
    // Mark as connected after short delay (simulates socket connect)
    const t = setTimeout(() => setConnected(true), 500)

    iv.current = setInterval(() => {
      const base = ATTACK_POOL[r(0, ATTACK_POOL.length - 1)]
      addPacket({
        packet_id:       uid(),
        source_ip:       rndIp(),
        destination_ip:  rndIp(),
        protocol:        PROTOCOLS[r(0, PROTOCOLS.length - 1)],
        packet_size:     r(64, 1500),
        attack_name:     base.attack_name,
        attack_category: base.attack_category,
        detection_method:base.detection_method,
        confidence_score: parseFloat((Math.random() * 35 + 65).toFixed(1)),
        model_accuracy:   parseFloat((Math.random() * 4  + 91).toFixed(1)),
        timestamp:        new Date().toISOString(),
      })
    }, 700)

    return () => { clearTimeout(t); clearInterval(iv.current) }
  }, []) // eslint-disable-line

  return null
}

/* ─────────────────────────────────────────────────────────────────
   STREAM HOOK WRAPPER  (connects to real backend; ignored in demo)
───────────────────────────────────────────────────────────────── */
function StreamConnector({ onMode }) {
  const { mode } = useTrafficStream()
  useEffect(() => { onMode(mode) }, [mode]) // eslint-disable-line
  return null
}

/* ─────────────────────────────────────────────────────────────────
   ROOT APP
───────────────────────────────────────────────────────────────── */
function AppInner() {
  // In production remove MockInjector and uncomment StreamConnector
  // const [mode, setMode] = useState('connecting')

  return (
    <div className="soc-app flex h-screen overflow-hidden bg-bg-deep">
      {/* Scanline overlay */}
      <div className="scan-overlay" />

      {/* Grid background */}
      <div
        className="fixed inset-0 pointer-events-none z-0"
        style={{
          backgroundImage: 'linear-gradient(#1E2D4520 1px, transparent 1px), linear-gradient(90deg, #1E2D4520 1px, transparent 1px)',
          backgroundSize: '48px 48px',
          maskImage: 'radial-gradient(ellipse 120% 80% at 50% 0%, black 40%, transparent 100%)',
        }}
      />

      {/* MOCK: remove in production */}
      <MockInjector />

      {/* Production: connect to real Flask backend */}
      {/* <StreamConnector onMode={setMode} /> */}

      <Sidebar />

      <div className="flex flex-col flex-1 overflow-hidden relative z-10">
        <Header mode="socket" />
        <Dashboard />
      </div>

      {/* Alert overlay */}
      <AlertPopup />
    </div>
  )
}

export default function App() {
  return (
    <TrafficProvider>
      <AppInner />
    </TrafficProvider>
  )
}
