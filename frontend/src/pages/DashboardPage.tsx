import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Droplets,
  Zap,
  Flame,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  Lightbulb,
  CheckCircle,
  RefreshCw,
  Clock,
  Sparkles
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
import { dashboardApi, orgApi } from '../api/endpoints'
import type { DashboardSummary } from '../types'

export const DashboardPage: React.FC = () => {
  const { currentOrg, setCurrentOrg, setOrganizations } = useAuthStore()
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchSummary = async () => {
    setLoading(true)
    setError(null)
    try {
      let orgId = currentOrg?.id
      if (!orgId) {
        const orgs = await orgApi.listMy()
        setOrganizations(orgs)
        if (orgs.length > 0) {
          setCurrentOrg(orgs[0])
          orgId = orgs[0].id
        }
      }
      if (orgId) {
        const summary = await dashboardApi.getSummary(orgId)
        setData(summary)
      } else {
        setError('No active organization facility found.')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to retrieve dashboard metrics.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSummary()
  }, [currentOrg?.id])

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-emerald-400">
        <div className="w-8 h-8 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-slate-400 text-sm">Aggregating telemetry from {currentOrg?.name || 'facility'}...</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Page Title & Refresh */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Facility Executive Overview
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real-time telemetry and autonomous AI diagnosis for{' '}
            <span className="text-emerald-600 dark:text-emerald-400 font-semibold">{currentOrg?.name}</span>
          </p>
        </div>
        <button
          onClick={fetchSummary}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white hover:bg-slate-100 text-slate-800 border border-slate-200 dark:bg-slate-900 dark:border-emerald-500/20 dark:hover:border-emerald-500/40 text-xs font-semibold dark:text-slate-200 transition-colors self-start sm:self-auto shadow-sm"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-emerald-500 dark:text-emerald-400 ${loading ? 'animate-spin' : ''}`} />
          <span>Sync Telemetry</span>
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400 text-xs flex items-center justify-between">
          <span>{error}</span>
          <button onClick={fetchSummary} className="underline font-semibold ml-4">Retry</button>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Water Today */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl relative overflow-hidden group hover:border-emerald-500/30 transition-all shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Water Consumption</span>
            <div className="w-9 h-9 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-500 dark:text-blue-400 flex items-center justify-center">
              <Droplets className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
            {data ? (data.water_today_liters).toLocaleString() : '0'}{' '}
            <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">Liters</span>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400 font-medium">
            <ArrowDownRight className="w-3.5 h-3.5" />
            <span>-4.2% vs 30-day baseline</span>
          </div>
        </div>

        {/* Electricity Today */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl relative overflow-hidden group hover:border-emerald-500/30 transition-all shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Energy Demand</span>
            <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-500 dark:text-amber-400 flex items-center justify-center">
              <Zap className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
            {data ? (data.electricity_today_kwh).toLocaleString() : '0'}{' '}
            <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">kWh</span>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>Grid baseline load normal</span>
          </div>
        </div>

        {/* Carbon Today */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl relative overflow-hidden group hover:border-emerald-500/30 transition-all shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Carbon Footprint</span>
            <div className="w-9 h-9 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-500 dark:text-teal-400 flex items-center justify-center">
              <Flame className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
            {data ? (data.carbon_today_kg).toFixed(1) : '0'}{' '}
            <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">kg CO₂e</span>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>CEA factor 0.716 kg/kWh</span>
          </div>
        </div>

        {/* Active Incidents */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl relative overflow-hidden group hover:border-emerald-500/30 transition-all shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Active Anomalies</span>
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${
              (data?.active_incidents || 0) > 0
                ? 'bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400'
                : 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400'
            }`}>
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
            {data ? data.active_incidents : 0}{' '}
            <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">Open Tickets</span>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-rose-500 dark:text-rose-400 font-medium">
            <span>Requires team action</span>
          </div>
        </div>
      </div>

      {/* Dual Charts: 30-Day Water & Electricity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Water Chart */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
                <Droplets className="w-4 h-4 text-blue-500 dark:text-blue-400" />
                30-Day Daily Water Draw
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Aggregated consumption across active meters</p>
            </div>
            <Link to="/water" className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1">
              <span>Meters</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="h-64 w-full">
            {data && data.water_chart && data.water_chart.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data.water_chart} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="waterGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:stroke-slate-800" vertical={false} />
                  <XAxis
                    dataKey="date"
                    stroke="#94a3b8"
                    fontSize={11}
                    tickFormatter={(val) => val.slice(5)}
                  />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px', color: '#f8fafc' }}
                    labelFormatter={(label) => `Date: ${label}`}
                    formatter={(val: any) => [`${Number(val).toLocaleString()} Liters`, 'Consumption']}
                  />
                  <Area
                    type="monotone"
                    dataKey="consumption"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#waterGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-400 text-xs">
                No historical water readings recorded yet.
              </div>
            )}
          </div>
        </div>

        {/* Electricity Chart */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-500 dark:text-amber-400" />
                30-Day Daily Power Usage
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Aggregated consumption across sub-meters</p>
            </div>
            <Link to="/electricity" className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1">
              <span>Meters</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="h-64 w-full">
            {data && data.electricity_chart && data.electricity_chart.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data.electricity_chart} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="energyGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:stroke-slate-800" vertical={false} />
                  <XAxis
                    dataKey="date"
                    stroke="#94a3b8"
                    fontSize={11}
                    tickFormatter={(val) => val.slice(5)}
                  />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px', color: '#f8fafc' }}
                    labelFormatter={(label) => `Date: ${label}`}
                    formatter={(val: any) => [`${Number(val).toLocaleString()} kWh`, 'Electricity']}
                  />
                  <Area
                    type="monotone"
                    dataKey="consumption"
                    stroke="#f59e0b"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#energyGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-400 text-xs">
                No historical power readings recorded yet.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Incidents & Recommendations Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Incident Feed */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl shadow-sm">
          <div className="flex items-center justify-between mb-5">
            <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-500 dark:text-rose-400" />
              Active AI Incident Tickets
            </h3>
            <Link to="/incidents" className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline">
              View All
            </Link>
          </div>

          <div className="space-y-3">
            {data?.recent_incidents && data.recent_incidents.length > 0 ? (
              data.recent_incidents.map((inc) => (
                <div
                  key={inc.id}
                  className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/30 transition-all flex items-start justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                          inc.severity === 'critical'
                            ? 'bg-rose-500/15 text-rose-500 dark:text-rose-400 border border-rose-500/30'
                            : inc.severity === 'high'
                            ? 'bg-amber-500/15 text-amber-500 dark:text-amber-400 border border-amber-500/30'
                            : 'bg-blue-500/15 text-blue-500 dark:text-blue-400 border border-blue-500/30'
                        }`}
                      >
                        {inc.severity}
                      </span>
                      <span className="text-[10px] text-slate-500 font-medium capitalize">
                        Status: {inc.state}
                      </span>
                    </div>
                    <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">{inc.title}</h4>
                    <p className="text-xs text-slate-600 dark:text-slate-400 line-clamp-2">{inc.description}</p>
                    {inc.estimated_impact && (
                      <p className="text-[11px] font-medium text-emerald-600 dark:text-emerald-400/90 pt-1">
                        Est. Impact: {inc.estimated_impact}
                      </p>
                    )}
                  </div>
                  <Link
                    to="/incidents"
                    className="p-2 rounded-xl bg-slate-100 dark:bg-slate-900 text-slate-500 hover:text-emerald-600 dark:text-slate-400 dark:hover:text-emerald-400 transition-colors shrink-0"
                  >
                    <ArrowUpRight className="w-4 h-4" />
                  </Link>
                </div>
              ))
            ) : (
              <div className="p-8 text-center text-slate-400 text-xs flex flex-col items-center gap-2">
                <CheckCircle className="w-6 h-6 text-emerald-500/40" />
                <span>Zero open anomalies detected. All meters within expected baselines.</span>
              </div>
            )}
          </div>
        </div>

        {/* Recommendations */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-emerald-500/15 backdrop-blur-xl shadow-sm">
          <div className="flex items-center justify-between mb-5">
            <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              Prioritized Optimization Actions
            </h3>
            <Link to="/recommendations" className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline">
              View All
            </Link>
          </div>

          <div className="space-y-3">
            {data?.top_recommendations && data.top_recommendations.length > 0 ? (
              data.top_recommendations.map((rec) => (
                <div
                  key={rec.id}
                  className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/30 transition-all space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                      Score {rec.priority_score}/100
                    </span>
                    <span className="text-[11px] font-semibold text-slate-500 dark:text-slate-400">
                      {rec.category}
                    </span>
                  </div>
                  <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">{rec.title}</h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400 line-clamp-2">{rec.description}</p>
                  <div className="flex flex-wrap items-center gap-3 pt-1 text-[11px] text-slate-500 dark:text-slate-400">
                    {rec.estimated_savings_inr && (
                      <span className="text-emerald-600 dark:text-emerald-400 font-semibold">
                        Save ₹{rec.estimated_savings_inr.toLocaleString()}
                      </span>
                    )}
                    {rec.estimated_co2_reduction_kg && (
                      <span className="text-teal-600 dark:text-teal-400 font-semibold">
                        -{rec.estimated_co2_reduction_kg} kg CO₂
                      </span>
                    )}
                    <span className="text-slate-400 capitalize">Effort: {rec.implementation_effort}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-8 text-center text-slate-400 text-xs flex flex-col items-center gap-2">
                <Sparkles className="w-6 h-6 text-slate-400" />
                <span>Generating optimization suggestions from usage telemetry...</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
