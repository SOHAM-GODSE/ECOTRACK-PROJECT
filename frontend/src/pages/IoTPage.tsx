import React, { useEffect, useState } from 'react'
import {
  Cpu,
  Wifi,
  WifiOff,
  Activity,
  Layers,
  Radio,
  Clock,
  ShieldCheck
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { iotApi } from '../api/endpoints'

export const IoTPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [devices, setDevices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!currentOrg) return
    setLoading(true)
    iotApi.listDevices(currentOrg.id)
      .then((data) => setDevices(data))
      .catch((err) => console.error('Failed to load IoT devices:', err))
      .finally(() => setLoading(false))
  }, [currentOrg?.id])

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Cpu className="w-8 h-8 text-purple-400" />
          IoT Sensor Mesh & Telemetry Pipeline
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Connected ultrasonic water flow meters, digital energy sub-panels, and MQTT gateways.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {devices.map((dev) => (
          <div
            key={dev.id}
            className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-slate-400 bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
                {dev.device_id}
              </span>
              <div className="flex items-center gap-2">
                <span className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  ONLINE
                </span>
                <span className="text-[10px] font-mono text-slate-500 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                  {dev.firmware_version || 'v1.0.0'}
                </span>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-bold text-white">{dev.name}</h3>
              <p className="text-xs text-slate-400 mt-0.5 capitalize">
                Sensor Type: <span className="text-slate-200 font-semibold">{dev.device_type?.replace('_', ' ')}</span>
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 text-xs space-y-2">
              <div className="flex justify-between text-slate-400">
                <span>Ingestion Frequency</span>
                <span className="text-slate-200 font-semibold">Every 15 minutes</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Protocol</span>
                <span className="text-slate-200 font-semibold">MQTT / TLS 1.3</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Telemetry Mode</span>
                <span className="text-emerald-400 font-semibold">
                  {dev.is_simulated ? 'Simulated Telemetry' : 'Physical Production Sensor'}
                </span>
              </div>
            </div>

            <div className="pt-2 text-[11px] text-slate-500 flex items-center justify-between">
              <span>Last Heartbeat: Active</span>
              <span className="text-emerald-400/80">Signal: 98% (Excellent)</span>
            </div>
          </div>
        ))}

        {devices.length === 0 && !loading && (
          <div className="p-16 text-center text-slate-500 text-xs bg-slate-900/40 rounded-3xl border border-slate-800/60 col-span-2">
            No IoT hardware nodes provisioned for this organization.
          </div>
        )}
      </div>
    </div>
  )
}
