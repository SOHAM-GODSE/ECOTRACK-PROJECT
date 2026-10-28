import React, { useEffect, useState } from 'react'
import {
  Droplets,
  Plus,
  AlertTriangle,
  CheckCircle2,
  TrendingDown,
  Clock,
  Activity,
  Layers
} from 'lucide-react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts'
import { useAuthStore } from '../store/authStore'
import { waterApi } from '../api/endpoints'
import type { WaterMeter, WaterReading } from '../types'

export const WaterPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [meters, setMeters] = useState<WaterMeter[]>([])
  const [selectedMeter, setSelectedMeter] = useState<WaterMeter | null>(null)
  const [readings, setReadings] = useState<WaterReading[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [newReadingVal, setNewReadingVal] = useState('')
  const [readingNotes, setReadingNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const loadMeters = async () => {
    if (!currentOrg) return
    setLoading(true)
    try {
      const list = await waterApi.listMeters(currentOrg.id)
      setMeters(list)
      if (list.length > 0) {
        setSelectedMeter(list[0])
      }
    } catch (err) {
      console.error('Failed to load water meters:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadReadings = async (meterId: number) => {
    try {
      const data = await waterApi.getReadings(meterId, 30)
      setReadings(data)
    } catch (err) {
      console.error('Failed to load readings:', err)
    }
  }

  useEffect(() => {
    loadMeters()
  }, [currentOrg?.id])

  useEffect(() => {
    if (selectedMeter) {
      loadReadings(selectedMeter.id)
    }
  }, [selectedMeter?.id])

  const handleAddReading = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedMeter || !newReadingVal) return
    setSubmitting(true)
    try {
      await waterApi.addReading(selectedMeter.id, {
        reading_value: parseFloat(newReadingVal),
        notes: readingNotes,
      })
      setShowAddModal(false)
      setNewReadingVal('')
      setReadingNotes('')
      loadReadings(selectedMeter.id)
    } catch (err) {
      console.error('Failed to add reading:', err)
    } finally {
      setSubmitting(false)
    }
  }

  const chartData = [...readings].reverse().map((r) => ({
    date: r.recorded_at.slice(5, 10),
    consumption: r.consumption || 0,
    is_anomaly: r.is_anomaly,
  }))

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <Droplets className="w-8 h-8 text-blue-400" />
            Water Intelligence & Anomaly Triage
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Flow rate monitoring, nocturnal leak diagnosis, and consumption analytics.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="inline-flex items-center gap-2 bg-blue-500 hover:bg-blue-400 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs shadow-lg shadow-blue-500/20 transition-all self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Record New Reading</span>
        </button>
      </div>

      {/* Meter Selector Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {meters.map((meter) => {
          const isSelected = selectedMeter?.id === meter.id
          return (
            <div
              key={meter.id}
              onClick={() => setSelectedMeter(meter)}
              className={`p-5 rounded-2xl cursor-pointer transition-all border ${
                isSelected
                  ? 'bg-blue-500/10 border-blue-500/50 shadow-lg shadow-blue-500/10'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[11px] font-mono text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                  {meter.meter_id}
                </span>
                <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20 uppercase">
                  {meter.status}
                </span>
              </div>
              <h3 className="font-bold text-slate-100 text-base">{meter.name}</h3>
              <p className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-slate-500" />
                <span>{meter.location || 'General Feed'}</span>
              </p>
            </div>
          )
        })}
      </div>

      {/* Consumption Trend Bar Chart */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="font-bold text-white text-base">
              Consumption History — {selectedMeter?.name}
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Daily volume draw in Liters. Spikes highlighted automatically by statistical Z-score.
            </p>
          </div>
        </div>

        <div className="h-72 w-full">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  formatter={(val: any) => [`${Number(val).toLocaleString()} Liters`, 'Consumption']}
                />
                <Bar
                  dataKey="consumption"
                  fill="#3b82f6"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-slate-500 text-xs">
              No readings recorded for this meter.
            </div>
          )}
        </div>
      </div>

      {/* Detailed Reading Logs Table */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl">
        <h3 className="font-bold text-white text-base mb-4">Reading Telemetry Audit Log</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="pb-3">Timestamp</th>
                <th className="pb-3">Meter Reading</th>
                <th className="pb-3">Net Consumption</th>
                <th className="pb-3">Source</th>
                <th className="pb-3">Anomaly Status</th>
                <th className="pb-3">Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {readings.map((r) => (
                <tr key={r.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3 font-mono text-[11px] text-slate-400">
                    {r.recorded_at.replace('T', ' ').slice(0, 19)}
                  </td>
                  <td className="py-3 font-medium text-slate-100">
                    {r.reading_value.toLocaleString()} {r.unit}
                  </td>
                  <td className="py-3 font-semibold text-blue-400">
                    {r.consumption ? `${r.consumption.toLocaleString()} L` : '—'}
                  </td>
                  <td className="py-3 uppercase text-[10px] text-slate-400 font-semibold">
                    {r.source}
                  </td>
                  <td className="py-3">
                    {r.is_anomaly ? (
                      <span className="inline-flex items-center gap-1 text-[10px] font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                        <AlertTriangle className="w-3 h-3" />
                        Surge Spike
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        <CheckCircle2 className="w-3 h-3" />
                        Normal
                      </span>
                    )}
                  </td>
                  <td className="py-3 text-slate-400 italic">{r.notes || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Manual Entry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-6 w-full max-w-md shadow-2xl space-y-4">
            <h3 className="text-lg font-bold text-white">Record Water Reading</h3>
            <p className="text-xs text-slate-400">
              Meter: <span className="text-emerald-400 font-semibold">{selectedMeter?.name}</span> ({selectedMeter?.meter_id})
            </p>

            <form onSubmit={handleAddReading} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Cumulative Value ({selectedMeter?.unit})
                </label>
                <input
                  type="number"
                  step="0.1"
                  required
                  value={newReadingVal}
                  onChange={(e) => setNewReadingVal(e.target.value)}
                  placeholder="e.g. 54200"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Inspection Notes
                </label>
                <input
                  type="text"
                  value={readingNotes}
                  onChange={(e) => setReadingNotes(e.target.value)}
                  placeholder="e.g. Verified dial during maintenance audit"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2.5 rounded-xl text-xs font-bold bg-blue-500 hover:bg-blue-400 text-slate-950 shadow-lg shadow-blue-500/20"
                >
                  {submitting ? 'Submitting...' : 'Save Reading'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
