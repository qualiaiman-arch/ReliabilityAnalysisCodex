import ReactDOM from 'react-dom/client'
import { useState } from 'react'
import { SystemFormPage } from './pages/SystemFormPage'
import { ResultsPage } from './pages/ResultsPage'

function App() {
  const [systemId, setSystemId] = useState<number | null>(null)

  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16, fontFamily: 'Arial, sans-serif' }}>
      {systemId === null ? (
        <SystemFormPage onCreated={setSystemId} />
      ) : (
        <ResultsPage systemId={systemId} onReset={() => setSystemId(null)} />
      )}
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
