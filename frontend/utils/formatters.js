/**
 * Format an ISO timestamp to HH:MM:SS
 */
export const fmtTime = (iso) => {
  try {
    return new Date(iso).toISOString().slice(11, 23)
  } catch {
    return iso
  }
}

/**
 * Format an ISO timestamp to full readable string
 */
export const fmtDateTime = (iso) => {
  try {
    return new Date(iso).toLocaleString('en-US', {
      month: 'short', day: '2-digit', hour: '2-digit',
      minute: '2-digit', second: '2-digit', hour12: false
    })
  } catch {
    return iso
  }
}

/**
 * Determine row / theme class from attack_category
 */
export const themeFromCategory = (cat) => {
  if (!cat) return 'green'
  const c = cat.toLowerCase()
  if (c === 'known')   return 'red'
  if (c === 'unknown') return 'orange'
  return 'green'
}

/**
 * Confidence bar class
 */
export const confClass = (score) => {
  if (score >= 90) return 'high'
  if (score >= 70) return 'mid'
  return 'low'
}

/**
 * Map attack name to distribution bucket
 */
export const mapToDist = (name = '', category = '') => {
  if (category === 'Normal')  return 'Normal'
  if (category === 'Unknown') return 'Unknown'
  const n = name.toLowerCase()
  if (n.includes('ddos') || n.includes('flood')) return 'DDoS'
  if (n.includes('scan'))   return 'Port Scan'
  if (n.includes('brute'))  return 'Brute Force'
  if (n.includes('sql'))    return 'SQL Injection'
  return 'Unknown'
}

/**
 * Short random ID helper
 */
export const shortId = () => Math.random().toString(36).slice(2, 9).toUpperCase()
