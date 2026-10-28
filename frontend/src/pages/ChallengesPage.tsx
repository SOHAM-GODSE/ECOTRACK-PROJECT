import React, { useEffect, useState } from 'react'
import {
  Trophy,
  Users,
  Target,
  Sparkles,
  CheckCircle2,
  Calendar,
  Send
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { challengesApi } from '../api/endpoints'

export const ChallengesPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [challenges, setChallenges] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [submittingId, setSubmittingId] = useState<number | null>(null)
  const [submissionTitle, setSubmissionTitle] = useState('')
  const [submissionDesc, setSubmissionDesc] = useState('')

  const loadChallenges = async () => {
    if (!currentOrg) return
    setLoading(true)
    try {
      const list = await challengesApi.list(currentOrg.id)
      setChallenges(list)
    } catch (err) {
      console.error('Failed to load challenges:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadChallenges()
  }, [currentOrg?.id])

  const handleJoin = async (id: number) => {
    try {
      await challengesApi.join(id)
      loadChallenges()
    } catch (err) {
      console.error('Failed to join challenge:', err)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!submittingId || !submissionTitle) return
    try {
      await challengesApi.submit(submittingId, {
        title: submissionTitle,
        description: submissionDesc,
      })
      setSubmittingId(null)
      setSubmissionTitle('')
      setSubmissionDesc('')
      loadChallenges()
    } catch (err) {
      console.error('Failed to submit challenge action:', err)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Trophy className="w-8 h-8 text-amber-400" />
          Campus Green Challenges & Leaderboard
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Gamified sustainability campaigns that turn individual habits into collective measurable savings.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {challenges.map((c) => (
          <div
            key={c.id}
            className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/30 transition-all flex flex-col justify-between space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20 uppercase">
                  {c.category}
                </span>
                <span className="text-xs font-semibold text-emerald-400">
                  +{c.points_award || 150} EcoPoints
                </span>
              </div>

              <h3 className="text-lg font-bold text-white">{c.title}</h3>
              <p className="text-xs text-slate-300 leading-relaxed">{c.description}</p>

              <div className="flex items-center gap-4 text-xs text-slate-400 pt-2">
                <div className="flex items-center gap-1.5">
                  <Target className="w-3.5 h-3.5 text-blue-400" />
                  <span>
                    Goal: {c.target_value} {c.target_metric || 'units'}
                  </span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-purple-400" />
                  <span>Active until {c.end_date?.slice(0, 10)}</span>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between">
              <span className="text-xs text-slate-400 flex items-center gap-1">
                <Users className="w-3.5 h-3.5 text-emerald-400" />
                <span>{c.participants_count || 12} joined</span>
              </span>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleJoin(c.id)}
                  className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition-colors"
                >
                  Join
                </button>
                <button
                  onClick={() => setSubmittingId(c.id)}
                  className="px-4 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold transition-all shadow-md shadow-emerald-500/20"
                >
                  Log Action
                </button>
              </div>
            </div>
          </div>
        ))}

        {challenges.length === 0 && !loading && (
          <div className="p-16 text-center text-slate-500 text-xs bg-slate-900/40 rounded-3xl border border-slate-800/60 col-span-2">
            No active campaigns right now. Check back soon!
          </div>
        )}
      </div>

      {/* Submission Modal */}
      {submittingId && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-6 w-full max-w-md shadow-2xl space-y-4">
            <h3 className="text-lg font-bold text-white">Log Action for EcoPoints</h3>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Action Title
                </label>
                <input
                  type="text"
                  required
                  value={submissionTitle}
                  onChange={(e) => setSubmissionTitle(e.target.value)}
                  placeholder="e.g. Avoided single-use coffee cup with personal flask"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Details / Evidence
                </label>
                <textarea
                  rows={2}
                  value={submissionDesc}
                  onChange={(e) => setSubmissionDesc(e.target.value)}
                  placeholder="Location or notes..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setSubmittingId(null)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl text-xs font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 shadow-lg shadow-emerald-500/20"
                >
                  Submit & Earn Points
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
