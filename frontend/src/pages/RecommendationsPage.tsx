import React, { useEffect, useState } from 'react'
import {
  Lightbulb,
  CheckCircle2,
  Clock,
  Sparkles,
  ArrowRight,
  TrendingDown,
  Layers,
  IndianRupee,
  Check,
  Pause
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { recommendationApi } from '../api/endpoints'
import type { Recommendation } from '../types'

export const RecommendationsPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [loading, setLoading] = useState(true)

  const loadRecs = async () => {
    if (!currentOrg) return
    setLoading(true)
    try {
      const list = await recommendationApi.list(currentOrg.id)
      setRecommendations(list)
    } catch (err) {
      console.error('Failed to load recommendations:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRecs()
  }, [currentOrg?.id])

  const handleStatusUpdate = async (id: number, status: string) => {
    try {
      await recommendationApi.updateStatus(id, status)
      loadRecs()
    } catch (err) {
      console.error('Failed to update recommendation status:', err)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Lightbulb className="w-8 h-8 text-emerald-400" />
          AI Recommendations & Optimization Roadmaps
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Scored by payback period, capital expenditure, and verified greenhouse gas reduction.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                  Priority Score: {rec.priority_score}/100
                </span>
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
                  {rec.category}
                </span>
                <span className={`text-[10px] font-bold uppercase px-2.5 py-1 rounded-full ${
                  rec.status === 'completed'
                    ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                    : rec.status === 'accepted'
                    ? 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                    : 'bg-slate-800 text-slate-400'
                }`}>
                  {rec.status}
                </span>
              </div>

              {/* Status Action Buttons */}
              <div className="flex items-center gap-2">
                {rec.status === 'pending' && (
                  <>
                    <button
                      onClick={() => handleStatusUpdate(rec.id, 'accepted')}
                      className="px-3.5 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5"
                    >
                      <Check className="w-3.5 h-3.5" />
                      <span>Accept</span>
                    </button>
                    <button
                      onClick={() => handleStatusUpdate(rec.id, 'deferred')}
                      className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-all flex items-center gap-1.5"
                    >
                      <Pause className="w-3.5 h-3.5" />
                      <span>Defer</span>
                    </button>
                  </>
                )}
                {rec.status === 'accepted' && (
                  <button
                    onClick={() => handleStatusUpdate(rec.id, 'completed')}
                    className="px-4 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Mark Completed & Verify</span>
                  </button>
                )}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-bold text-white">{rec.title}</h3>
              <p className="text-sm text-slate-300 mt-1 leading-relaxed">{rec.description}</p>
            </div>

            {/* Evidence & Verification Box */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              {rec.evidence_summary && (
                <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80">
                  <span className="text-slate-500 font-semibold uppercase tracking-wider block mb-1">Audit Evidence</span>
                  <p className="text-slate-300">{rec.evidence_summary}</p>
                </div>
              )}
              {rec.how_to_verify && (
                <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80">
                  <span className="text-slate-500 font-semibold uppercase tracking-wider block mb-1">Verification Method</span>
                  <p className="text-slate-300">{rec.how_to_verify}</p>
                </div>
              )}
            </div>

            {/* Savings & Effort Metrics */}
            <div className="flex flex-wrap items-center gap-5 pt-2 border-t border-slate-800/80 text-xs">
              {rec.estimated_savings_inr && (
                <div className="flex items-center gap-1 text-emerald-400 font-bold">
                  <span>Est. Annual Savings: ₹{rec.estimated_savings_inr.toLocaleString()}</span>
                </div>
              )}
              {rec.estimated_savings_kwh && (
                <div className="text-amber-400 font-semibold">
                  Energy: -{rec.estimated_savings_kwh.toLocaleString()} kWh/yr
                </div>
              )}
              {rec.estimated_savings_liters && (
                <div className="text-blue-400 font-semibold">
                  Water: -{rec.estimated_savings_liters.toLocaleString()} L/yr
                </div>
              )}
              {rec.estimated_co2_reduction_kg && (
                <div className="text-teal-400 font-semibold">
                  Carbon: -{rec.estimated_co2_reduction_kg.toLocaleString()} kg CO₂e
                </div>
              )}
              <div className="text-slate-400 ml-auto capitalize">
                Effort: <span className="text-slate-200 font-semibold">{rec.implementation_effort}</span> | Cost: <span className="text-slate-200 font-semibold">{rec.implementation_cost}</span>
              </div>
            </div>
          </div>
        ))}

        {recommendations.length === 0 && !loading && (
          <div className="p-16 text-center text-slate-500 text-xs bg-slate-900/40 rounded-3xl border border-slate-800/60">
            No optimization recommendations active right now.
          </div>
        )}
      </div>
    </div>
  )
}
