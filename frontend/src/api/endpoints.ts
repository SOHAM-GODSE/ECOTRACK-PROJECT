import client from './client'
import type {
  User,
  Organization,
  DashboardSummary,
  WaterMeter,
  WaterReading,
  ElectricityMeter,
  ElectricityReading,
  Incident,
  Recommendation,
  WasteClassification,
  Notification
} from '../types'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  full_name: string
  password: string
  phone?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const authApi = {
  login: async (payload: LoginPayload): Promise<AuthResponse> => {
    const res = await client.post('/auth/login', payload)
    return res.data
  },
  register: async (payload: RegisterPayload): Promise<AuthResponse> => {
    const res = await client.post('/auth/register', payload)
    return res.data
  },
  getMe: async (): Promise<User> => {
    const res = await client.get('/auth/me')
    return res.data
  },
}

export const orgApi = {
  listMy: async (): Promise<Organization[]> => {
    const res = await client.get('/organizations/my')
    return res.data
  },
  get: async (id: number): Promise<Organization> => {
    const res = await client.get(`/organizations/${id}`)
    return res.data
  },
  create: async (data: { name: string; slug: string; org_type: string; city?: string }): Promise<Organization> => {
    const res = await client.post('/organizations', data)
    return res.data
  },
}

export const dashboardApi = {
  getSummary: async (orgId: number): Promise<DashboardSummary> => {
    const res = await client.get('/dashboard/summary', { params: { org_id: orgId } })
    return res.data
  },
}

export const waterApi = {
  listMeters: async (orgId: number): Promise<WaterMeter[]> => {
    const res = await client.get('/water/meters', { params: { org_id: orgId } })
    return res.data
  },
  getReadings: async (meterId: number, limit = 90): Promise<WaterReading[]> => {
    const res = await client.get(`/water/meters/${meterId}/readings`, { params: { limit } })
    return res.data
  },
  addReading: async (meterId: number, data: { reading_value: number; recorded_at?: string; notes?: string }): Promise<WaterReading> => {
    const res = await client.post(`/water/meters/${meterId}/readings`, data)
    return res.data
  },
}

export const electricityApi = {
  listMeters: async (orgId: number): Promise<ElectricityMeter[]> => {
    const res = await client.get('/electricity/meters', { params: { org_id: orgId } })
    return res.data
  },
  getReadings: async (meterId: number, limit = 90): Promise<ElectricityReading[]> => {
    const res = await client.get(`/electricity/meters/${meterId}/readings`, { params: { limit } })
    return res.data
  },
  addReading: async (meterId: number, data: { reading_value: number; recorded_at?: string; notes?: string }): Promise<ElectricityReading> => {
    const res = await client.post(`/electricity/meters/${meterId}/readings`, data)
    return res.data
  },
}

export const wasteApi = {
  classify: async (file: File, orgId?: number): Promise<any> => {
    const formData = new FormData()
    formData.append('file', file)
    if (orgId) formData.append('org_id', String(orgId))
    const res = await client.post('/waste/classify', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res.data
  },
  getHistory: async (orgId?: number, limit = 50): Promise<any[]> => {
    const res = await client.get('/waste/history', { params: { org_id: orgId, limit } })
    return res.data
  },
  getStats: async (orgId?: number): Promise<any> => {
    const res = await client.get('/waste/stats', { params: { org_id: orgId } })
    return res.data
  },
  correctCategory: async (id: number, category: string): Promise<any> => {
    const res = await client.patch(`/waste/classifications/${id}/correct`, { category })
    return res.data
  },
}

export const incidentApi = {
  list: async (orgId: number, state?: string, severity?: string): Promise<Incident[]> => {
    const res = await client.get('/incidents', { params: { org_id: orgId, state, severity } })
    return res.data
  },
  get: async (id: number): Promise<Incident> => {
    const res = await client.get(`/incidents/${id}`)
    return res.data
  },
  transition: async (id: number, toState: string, notes?: string): Promise<Incident> => {
    const res = await client.post(`/incidents/${id}/transition`, { to_state: toState, notes })
    return res.data
  },
}

export const carbonApi = {
  getSummary: async (orgId: number): Promise<any> => {
    const res = await client.get('/carbon/summary', { params: { org_id: orgId } })
    return res.data
  },
  getFactors: async (): Promise<any[]> => {
    const res = await client.get('/carbon/factors')
    return res.data
  },
  getCalculations: async (orgId: number): Promise<any[]> => {
    const res = await client.get('/carbon/calculations', { params: { org_id: orgId } })
    return res.data
  },
}

export const recommendationApi = {
  list: async (orgId: number): Promise<Recommendation[]> => {
    const res = await client.get('/recommendations', { params: { org_id: orgId } })
    return res.data
  },
  updateStatus: async (id: number, status: string): Promise<Recommendation> => {
    const res = await client.patch(`/recommendations/${id}/status`, { status })
    return res.data
  },
}

export const challengesApi = {
  list: async (orgId: number): Promise<any[]> => {
    const res = await client.get('/challenges', { params: { org_id: orgId } })
    return res.data
  },
  join: async (id: number): Promise<any> => {
    const res = await client.post(`/challenges/${id}/join`)
    return res.data
  },
  submit: async (id: number, data: { title: string; description?: string }): Promise<any> => {
    const res = await client.post(`/challenges/${id}/submissions`, data)
    return res.data
  },
}

export const locationsApi = {
  list: async (params?: { city?: string; type?: string }): Promise<any[]> => {
    const res = await client.get('/locations', { params })
    return res.data
  },
}

export const iotApi = {
  listDevices: async (orgId: number): Promise<any[]> => {
    const res = await client.get('/iot/devices', { params: { org_id: orgId } })
    return res.data
  },
  getTelemetry: async (deviceId: number, limit = 50): Promise<any[]> => {
    const res = await client.get(`/iot/devices/${deviceId}/telemetry`, { params: { limit } })
    return res.data
  },
}

export const adminApi = {
  listUsers: async (): Promise<any[]> => {
    const res = await client.get('/admin/users')
    return res.data
  },
  listOrgs: async (): Promise<any[]> => {
    const res = await client.get('/admin/organizations')
    return res.data
  },
  getAuditLogs: async (limit = 50): Promise<any[]> => {
    const res = await client.get('/admin/audit-logs', { params: { limit } })
    return res.data
  },
  getHealth: async (): Promise<any> => {
    const res = await client.get('/admin/health')
    return res.data
  },
}
