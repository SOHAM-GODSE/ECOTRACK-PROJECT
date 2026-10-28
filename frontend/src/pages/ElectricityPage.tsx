import React, { useEffect, useState } from 'react'
import {
  Zap,
  Plus,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  Layers,
  Flame,
  IndianRupee
} from 'lucide-react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts'
import { useAuthStore } from '../store/authStore'
import { electricityApi } from '../api/endpoints'
import type { ElectricityMeter, ElectricityReading } from '../types'

export const ElectricityPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [meters, setMeters] = useState<ElectricityMeter[]>([])
  const [selectedMeter, setSelectedMeter] = useState<ElectricityMeter | null>(null)
  const [readings, setReadings] = useState<ElectricityReading[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [newReadingVal, setNewReadingVal] = useState('')
  const [readingNotes, setReadingNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const loadMeters = async () => {
    if (!currentOrg) return
    setLoading(true)
    try {
      const list = await electricityApi.listMeters(currentOrg.id)
      setMeters(list)
      if (list.length > 0) {
        setSelectedMeter(list[0])
      }
    } catch (err) {
      console.error('Failed to load electricity meters:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadReadings = async (meterId: number) => {
    try {
      const data = await electricityApi.getReadings(meterId, 30)
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
      await electricityApi.addReading(selectedMeter.id, {
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
    kwh: r.consumption || 0,
    cost: (r.consumption || 0) * 7.0, // INR 7/kWh
  }))

  const totalConsumption30d = readings.reduce((acc, r) => acc + (r.consumption || 0), 0)
  const estimatedCost30d = totalConsumption30d * 7.0
  const estimatedCarbon30d = totalConsumption30d * 0.716

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <Zap className="w-8 h-8 text-amber-400" />
            Energy, Power & Peak Load Analytics
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Sub-metering, peak demand shaving, and tariff tracking.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs shadow-lg shadow-amber-500/20 transition-all self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Record Power Reading</span>
        </button>
      </div>

      {/* Summary KPI Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold uppercase">30-Day Total Energy</span>
          <div className="text-2xl font-black text-white mt-1">
            {totalConsumption30d.toLocaleString()} <span className="text-xs font-semibold text-slate-400">kWh</span>
          </div>
        </div>
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold uppercase">Estimated Power Cost</span>
          <div className="text-2xl font-black text-amber-400 mt-1">
            ₹{estimatedCost30d.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold uppercase">Attributed Emissions</span>
          <div className="text-2xl font-black text-teal-400 mt-1">
            {estimatedCarbon30d.toFixed(1)} <span className="text-xs font-semibold text-slate-400">kg CO₂e</span>
          </div>
        </div>
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
                  ? 'bg-amber-500/10 border-amber-500/50 shadow-lg shadow-amber-500/10'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[11px] font-mono text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                  {meter.meter_id}
                </span>
                <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20 uppercase">
                  {meter.meter_type || 'Main Grid'}
                </span>
              </div>
              <h3 className="font-bold text-slate-100 text-base">{meter.name}</h3>
              <p className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-slate-500" />
                <span>{meter.location || 'Substation Feed'}</span>
              </p>
            </div>
          )
        })}
      </div>

      {/* Consumption Trend Area Chart */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="font-bold text-white text-base">
              Daily Power Demand Curve — {selectedMeter?.name}
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Cumulative kWh progression tracked across 30 operational days.
            </p>
          </div>
        </div>

        <div className="h-72 w-full">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                <defs>
                  <linearGradient id="elecGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  formatter={(val: any) => [`${Number(val).toLocaleString()} kWh`, 'Consumption']}
                />
                <Area
                  type="monotone"
                  dataKey="kwh"
                  stroke="#f59e0b"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#elecGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-slate-500 text-xs">
              No readings recorded for this meter.
            </div>
          )}
        </div>
      </div>

      {/* Manual Entry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-6 w-full max-w-md shadow-2xl space-y-4">
            <h3 className="text-lg font-bold text-white">Record Electricity Reading</h3>
            <p className="text-xs text-slate-400">
              Meter: <span className="text-amber-400 font-semibold">{selectedMeter?.name}</span> ({selectedMeter?.meter_id})
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
                  placeholder="e.g. 28450"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-amber-400"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Audit Notes
                </label>
                <input
                  type="text"
                  value={readingNotes}
                  onChange={(e) => setReadingNotes(e.target.value)}
                  placeholder="e.g. Main grid meter verified by electrical staff"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-amber-400"
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
                  className="px-5 py-2.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/20"
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
