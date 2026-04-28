import axios from 'axios'
import type { SystemInput } from '../types'

const client = axios.create({ baseURL: 'http://localhost:8000/api' })

export async function createSystem(payload: SystemInput): Promise<number> {
  const res = await client.post('/systems', payload)
  return res.data.id
}

export async function calculate(systemId: number) {
  const res = await client.get(`/systems/${systemId}/calculate`)
  return res.data
}

export function exportExcel(systemId: number): string {
  return `http://localhost:8000/api/systems/${systemId}/export/excel`
}

export function exportPptx(systemId: number): string {
  return `http://localhost:8000/api/systems/${systemId}/export/pptx`
}
