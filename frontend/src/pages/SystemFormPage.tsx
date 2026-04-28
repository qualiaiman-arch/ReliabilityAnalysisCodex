import { useState } from 'react'
import { createSystem } from '../api/client'
import type { SystemInput } from '../types'

type Props = { onCreated: (id: number) => void }

const defaultPayload: SystemInput = {
  name: 'Demo Mission Computer',
  description: 'Demonstration system for mission reliability analysis.',
  mission: 'Control and monitoring during 10-hour mission profile.',
  lifetime_hours: 5000,
  operating_environment: 'Ground mobile platform, moderate vibration.',
  assemblies: [
    {
      name: 'Compute Module',
      active_time: 10,
      passive_time: 2,
      rest_time: 12,
      redundancy_type: '1oo2_active',
      unintended_operation_probability: 0.0001,
      source: 'Engineering estimate',
      notes: '',
      components: [
        {
          name: 'CPU-A',
          critical: true,
          lambda_active: 2e-5,
          kp: 0.1,
          kr: 0.025,
          source: 'Internal handbook',
          notes: '',
        },
        {
          name: 'CPU-B',
          critical: true,
          lambda_active: 2e-5,
          kp: 0.1,
          kr: 0.025,
          source: 'Internal handbook',
          notes: '',
        },
      ],
    },
    {
      name: 'Power Bus',
      active_time: 10,
      passive_time: 0,
      rest_time: 14,
      redundancy_type: '1oo1',
      unintended_operation_probability: 0.0002,
      direct_lambda_active: 1.2e-5,
      source: 'Supplier datasheet',
      notes: 'Treated as direct assembly rate',
      components: [],
    },
  ],
}

export function SystemFormPage({ onCreated }: Props) {
  const [payloadText, setPayloadText] = useState(JSON.stringify(defaultPayload, null, 2))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const submit = async () => {
    try {
      setLoading(true)
      setError('')
      const parsed = JSON.parse(payloadText) as SystemInput
      const id = await createSystem(parsed)
      onCreated(id)
    } catch (e) {
      setError('Failed to create system. Please verify JSON payload.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Reliability Analysis MVP</h1>
      <p>Define system, assemblies, components, duty cycles, and redundancy.</p>
      <textarea
        style={{ width: '100%', height: 360, fontFamily: 'monospace' }}
        value={payloadText}
        onChange={(e) => setPayloadText(e.target.value)}
      />
      <div style={{ marginTop: 12 }}>
        <button onClick={submit} disabled={loading}>{loading ? 'Saving...' : 'Create System'}</button>
      </div>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
    </div>
  )
}
