import React, { useEffect, useState } from 'react'
import {
  Flame,
  ShieldCheck,
  Calculator,
  ExternalLink,
  BookOpen,
  PieChart as PieIcon,
  CheckCircle2
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { carbonApi } from '../api/endpoints'

export const CarbonPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [factors, setFactors] = useState<any[]>([])
  const [selectedActivity, setSelectedActivity] = useState<string>('grid_electricity_india')
  const [activityInput, setActivityInput] = useState<string>('1000')
  const [calculatedCo2, setCalculatedCo2] = useState<number | null>(null)

  useEffect(() => {
    carbonApi.getFactors()
      .then((data) => setFactors(data))
      .catch((err) => console.error('Failed to load emission factors:', err))
  }, [])

  const currentFactor = factors.find((f) => f.activity === selectedActivity) || {
    factor_value: 0.716,
    unit_numerator: 'kg_co2e',
    unit_denominator: 'kWh',
    name: 'India Grid Electricity Average',
    source: 'CEA CO2 Baseline Database 2022-23',
    source_url: 'https://cea.nic.in/',
  }

  const handleCompute = (e: React.FormEvent) => {
    e.preventDefault()
    const val = parseFloat(activityInput) || 0
    setCalculatedCo2(val * currentFactor.factor_value)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Flame className="w-8 h-8 text-teal-400" />
          Deterministic Carbon Accounting Engine
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Traceable greenhouse gas (GHG) calculations calibrated to the Central Electricity Authority (CEA) of India.
        </p>
      </div>

      {/* Standards & Transparency Box */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div className="space-y-2">
            <h3 className="font-bold text-white text-base">Mathematical Proof & Methodological Integrity</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              EcoTrack uses deterministic formula modeling: <code className="bg-slate-950 px-2 py-0.5 rounded text-emerald-400 font-mono">Emissions = Activity Data × Published Factor</code>.
              Unlike black-box estimates, every carbon credit and avoidance claim is accompanied by its source database citation and version timestamp.
            </p>
          </div>
        </div>
      </div>

      {/* Interactive Calculator */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl space-y-6">
          <div className="flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            <h3 className="font-bold text-white text-base">Interactive Footprint Simulator</h3>
          </div>

          <form onSubmit={handleCompute} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-2">
                Activity / Resource Category
              </label>
              <select
                value={selectedActivity}
                onChange={(e) => {
                  setSelectedActivity(e.target.value)
                  setCalculatedCo2(null)
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-emerald-500"
              >
                {factors.map((f) => (
                  <option key={f.activity} value={f.activity}>
                    {f.name} ({f.category})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-2">
                Input Activity Volume ({currentFactor.unit_denominator})
              </label>
              <input
                type="number"
                step="0.01"
                required
                value={activityInput}
                onChange={(e) => setActivityInput(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl shadow-lg shadow-emerald-500/20 text-sm transition-all"
            >
              Compute Emissions
            </button>
          </form>

          {calculatedCo2 !== null && (
            <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 space-y-2">
              <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">
                Emissions Output
              </span>
              <div className="text-3xl font-black text-white">
                {calculatedCo2.toLocaleString(undefined, { maximumFractionDigits: 2 })}{' '}
                <span className="text-sm font-semibold text-emerald-400">kg CO₂e</span>
              </div>
              <p className="text-xs text-slate-400 font-mono">
                Formula: {activityInput} {currentFactor.unit_denominator} × {currentFactor.factor_value} kg CO₂e/{currentFactor.unit_denominator}
              </p>
            </div>
          )}
        </div>

        {/* Accredited Database Registry */}
        <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl space-y-4">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-400" />
            <h3 className="font-bold text-white text-base">Active Emission Factor Registry</h3>
          </div>

          <div className="space-y-3">
            {factors.map((f) => (
              <div
                key={f.id}
                className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-200">{f.name}</span>
                  <span className="text-xs font-mono font-bold text-emerald-400">
                    {f.factor_value} {f.unit_numerator}/{f.unit_denominator}
                  </span>
                </div>
                <div className="flex items-center justify-between text-[11px] text-slate-400">
                  <span>Category: {f.category}</span>
                  <span className="text-slate-500 italic truncate max-w-[200px]">{f.source}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
