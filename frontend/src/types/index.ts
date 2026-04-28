export type ComponentInput = {
  name: string
  critical: boolean
  lambda_active: number
  kp: number
  kr: number
  source: string
  notes: string
}

export type AssemblyInput = {
  name: string
  active_time: number
  passive_time: number
  rest_time: number
  redundancy_type: '1oo1' | '1oo2_active'
  unintended_operation_probability: number
  direct_lambda_active?: number
  source: string
  notes: string
  components: ComponentInput[]
}

export type SystemInput = {
  name: string
  description: string
  mission: string
  lifetime_hours: number
  operating_environment: string
  assemblies: AssemblyInput[]
}
