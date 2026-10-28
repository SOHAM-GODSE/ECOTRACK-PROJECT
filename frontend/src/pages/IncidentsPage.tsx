import React, { useEffect, useState } from 'react'
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  ArrowRight,
  Filter,
  Layers,
  FileCheck2,
  Activity,
  ShieldAlert,
  ChevronRight
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { incidentApi } from '../api/endpoints'
import type { Incident } from '../types'

export const IncidentsPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null)
  const [loading, setLoading] = useState(true)
  const [severityFilter, setSeverityFilter] = useState<string>('')
  const [stateFilter, setStateFilter] = useState<string>('')
  const [transitioning, setTransitioning] = useState(false)
  const [actionNotes, setActionNotes] = useState('')

  const loadIncidents = async () => {
    if (!currentOrg) return
    setLoading(true)
    try {
      const list = await incidentApi.list(
        currentOrg.id,
        stateFilter || undefined,
        severityFilter || undefined
      )
      setIncidents(list)
    } catch (err) {
      console.error('Failed to load incidents:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadIncidents()
  }, [currentOrg?.id, severityFilter, stateFilter])

  const handleTransition = async (toState: string) => {
    if (!selectedIncident) return
    setTransitioning(true)
    try {
      const updated = await incidentApi.transition(selectedIncident.id, toState, actionNotes)
      setSelectedIncident(updated)
      setActionNotes('')
      loadIncidents()
    } catch (err) {
      console.error('Failed to transition incident state:', err)
    } finally {
      setTransitioning(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <AlertTriangle className="w-8 h-8 text-rose-400" />
          Autonomous Incident Triage & Resolution
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Root-cause diagnosis, evidence logging, and impact verification workflow.
        </p>
      </div>

      {/* Filters Strip */}
      <div className="flex flex-wrap items-center gap-3 bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-2 text-xs text-slate-400 mr-2">
          <Filter className="w-4 h-4 text-emerald-400" />
          <span className="font-semibold uppercase tracking-wider">Filters:</span>
        </div>

        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl px-3 py-1.5 focus:outline-none focus:border-emerald-500"
        >
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>

        <select
          value={stateFilter}
          onChange={(e) => setStateFilter(e.target.value)}
          className="bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl px-3 py-1.5 focus:outline-none focus:border-emerald-500"
        >
          <option value="">All States</option>
          <option value="new">New</option>
          <option value="investigating">Investigating</option>
          <option value="resolved">Resolved</option>
          <option value="impact_verified">Impact Verified</option>
        </select>
      </div>

      {/* Incident Cards List */}
      <div className="grid grid-cols-1 gap-4">
        {incidents.map((inc) => (
          <div
            key={inc.id}
            onClick={() => setSelectedIncident(inc)}
            className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/30 transition-all cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-6 group"
          >
            <div className="space-y-2 flex-1">
              <div className="flex items-center gap-2.5">
                <span
                  className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full ${
                    inc.severity === 'critical'
                      ? 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                      : inc.severity === 'high'
                      ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                      : 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                  }`}
                >
                  {inc.severity}
                </span>

                <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                  {inc.state.replace('_', ' ')}
                </span>

                <span className="text-xs text-slate-500 font-mono">
                  Ticket #{inc.id}
                </span>
              </div>

              <h3 className="text-base font-bold text-white group-hover:text-emerald-400 transition-colors">
                {inc.title}
              </h3>
              <p className="text-xs text-slate-400 line-clamp-2">{inc.description}</p>

              {inc.estimated_impact && (
                <div className="text-xs text-rose-400 font-medium pt-1">
                  Estimated Financial & Volumetric Impact: {inc.estimated_impact}
                </div>
              )}
            </div>

            <div className="flex items-center gap-4 shrink-0">
              <button
                type="button"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs font-semibold text-slate-200 group-hover:border-emerald-500/40 transition-colors"
              >
                <span>Triage Ticket</span>
                <ChevronRight className="w-4 h-4 text-emerald-400" />
              </button>
            </div>
          </div>
        ))}

        {incidents.length === 0 && !loading && (
          <div className="p-16 text-center text-slate-500 text-xs bg-slate-900/40 rounded-3xl border border-slate-800/60">
            No incident tickets match the selected filters.
          </div>
        )}
      </div>

      {/* Incident Detail Modal */}
      {selectedIncident && (
        <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-6 sm:p-8 w-full max-w-2xl shadow-2xl space-y-6 my-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-mono text-slate-400">#{selectedIncident.id}</span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30">
                    {selectedIncident.severity}
                  </span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                    {selectedIncident.state.replace('_', ' ')}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-white">{selectedIncident.title}</h3>
              </div>
              <button
                onClick={() => setSelectedIncident(null)}
                className="text-slate-400 hover:text-white text-lg font-bold p-1"
              >
                ✕
              </button>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 text-xs text-slate-300 space-y-2">
              <span className="text-slate-500 font-semibold uppercase tracking-wider block">Description</span>
              <p>{selectedIncident.description}</p>
            </div>

            {selectedIncident.ai_evidence && (
              <div className="p-4 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-xs space-y-2">
                <span className="text-blue-400 font-bold uppercase tracking-wider block flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5" />
                  AI Statistical Evidence
                </span>
                <pre className="font-mono text-[11px] text-slate-200 overflow-x-auto whitespace-pre-wrap">
                  {JSON.stringify(selectedIncident.ai_evidence, null, 2)}
                </pre>
              </div>
            )}

            {selectedIncident.ai_recommendations && (
              <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-xs space-y-1">
                <span className="text-emerald-400 font-bold uppercase tracking-wider block">
                  AI Action Recommendation
                </span>
                <p className="text-slate-200">{selectedIncident.ai_recommendations.action}</p>
              </div>
            )}

            {/* Workflow Action State Transition */}
            <div className="space-y-3 pt-3 border-t border-slate-800">
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Action Log / Resolution Notes
              </label>
              <textarea
                rows={2}
                value={actionNotes}
                onChange={(e) => setActionNotes(e.target.value)}
                placeholder="e.g. Plumber dispatched, valve replaced at 14:00"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
              />

              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <span className="text-[11px] text-slate-500">Transition Incident State:</span>
                <div className="flex items-center gap-2">
                  {selectedIncident.state !== 'investigating' && (
                    <button
                      onClick={() => handleTransition('investigating')}
                      disabled={transitioning}
                      className="px-3 py-1.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-xs font-semibold border border-amber-500/30"
                    >
                      Investigating
                    </button>
                  )}
                  {selectedIncident.state !== 'resolved' && (
                    <button
                      onClick={() => handleTransition('resolved')}
                      disabled={transitioning}
                      className="px-3 py-1.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 text-xs font-semibold border border-emerald-500/30"
                    >
                      Mark Resolved
                    </button>
                  )}
                  {selectedIncident.state === 'resolved' && (
                    <button
                      onClick={() => handleTransition('impact_verified')}
                      disabled={transitioning}
                      className="px-3 py-1.5 rounded-xl bg-teal-500/20 hover:bg-teal-500/30 text-teal-300 text-xs font-semibold border border-teal-500/30"
                    >
                      Verify Impact
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
