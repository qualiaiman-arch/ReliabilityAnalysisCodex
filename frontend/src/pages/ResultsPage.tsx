import { useEffect, useState } from 'react'
import { calculate, exportExcel, exportPptx } from '../api/client'

type Props = {
  systemId: number
  onReset: () => void
}

export function ResultsPage({ systemId, onReset }: Props) {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    calculate(systemId).then(setData)
  }, [systemId])

  if (!data) return <p>Calculating...</p>

  return (
    <div>
      <h2>Results: {data.system_name}</h2>
      <p><b>System R:</b> {data.system_r.toFixed(6)}</p>
      <p><b>System Q:</b> {data.system_q.toFixed(6)}</p>

      <h3>Assemblies</h3>
      <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr><th>Name</th><th>R</th><th>Q</th><th>Redundancy</th><th>P(unintended op)</th></tr>
        </thead>
        <tbody>
          {data.assemblies.map((a: any) => (
            <tr key={a.id}>
              <td>{a.name}</td>
              <td>{a.r.toFixed(6)}</td>
              <td>{a.q.toExponential(3)}</td>
              <td>{a.redundancy_type}</td>
              <td>{a.unintended_operation_probability}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Rule-based Recommendations</h3>
      <ul>
        {data.recommendations.map((r: string, i: number) => <li key={i}>{r}</li>)}
      </ul>

      <p>
        <a href={exportExcel(systemId)} target="_blank">Export Excel</a> |{' '}
        <a href={exportPptx(systemId)} target="_blank">Export PowerPoint</a>
      </p>
      <button onClick={onReset}>Analyze Another System</button>
    </div>
  )
}
