import React from 'react'
import { Link } from 'react-router-dom'
import {
  Leaf,
  Droplets,
  Zap,
  Trash2,
  ShieldCheck,
  TrendingDown,
  ArrowRight,
  Activity,
  Cpu,
  BarChart3,
  CheckCircle2
} from 'lucide-react'

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-emerald-500 selection:text-white">
      {/* Top Navbar */}
      <header className="border-b border-emerald-500/10 backdrop-blur-xl bg-slate-950/70 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/25">
              <Leaf className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                EcoTrack <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-semibold uppercase">AI</span>
              </span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="text-sm font-medium text-slate-300 hover:text-emerald-400 transition-colors px-4 py-2"
            >
              Sign In
            </Link>
            <Link
              to="/login"
              className="text-sm font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 px-5 py-2.5 rounded-xl shadow-lg shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5"
            >
              Open Live Demo
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-24 pb-20 px-6 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(16,185,129,0.18),rgba(255,255,255,0))]"></div>
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-xs font-semibold mb-8 uppercase tracking-widest">
            <Activity className="w-3.5 h-3.5 animate-pulse" />
            AI-Driven Environmental Intelligence Platform
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white leading-[1.1] mb-8">
            Detect Waste. Predict Problems.{' '}
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
              Measure Real Impact.
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto mb-10 leading-relaxed">
            Autonomous multi-utility intelligence for campuses, housing societies, and enterprises. 
            Real-time IoT anomaly detection, computer vision waste recognition, and verifiable greenhouse gas reductions.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/login"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-8 py-4 rounded-xl shadow-xl shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5 text-base"
            >
              <span>Explore Campus Dashboard</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/register"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-700/60 font-semibold px-8 py-4 rounded-xl transition-colors text-base"
            >
              Register Facility
            </Link>
          </div>

          <div className="mt-12 flex flex-wrap items-center justify-center gap-8 text-xs text-slate-400 font-medium">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>CEA (India) Emission Standard Built-in</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Sub-second Anomaly Triage</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>MobileNet AI Waste Classification</span>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-20 px-6 max-w-7xl mx-auto border-t border-emerald-500/10">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Five Cohesive Intelligence Engines</h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            From physical IoT flow meters to high-level ESG compliance reporting, EcoTrack AI unifies every environmental touchpoint.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="p-8 rounded-2xl bg-slate-900/60 border border-emerald-500/15 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mb-6">
              <Droplets className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Water Intelligence</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Detect underground bursts, nocturnal leaks, and valve failures using automated Z-score baseline modeling before water bills escalate.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-slate-900/60 border border-emerald-500/15 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center mb-6">
              <Zap className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Energy & Power Peak Load</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Real-time kWh tracking across transformers and sub-panels. Automatically flags HVAC weekend runaways and phantom loads.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-slate-900/60 border border-emerald-500/15 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mb-6">
              <Trash2 className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Computer Vision Waste Classifier</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Instant photographic sorting for wet organic, dry recyclables, e-waste, and hazardous materials with localized disposal instructions.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-slate-900/60 border border-emerald-500/15 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center mb-6">
              <TrendingDown className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Deterministic Carbon Engine</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Accredited CEA Indian power grid baseline emission factor calculations (0.716 kg CO₂e/kWh) with transparent mathematical proof.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-slate-900/60 border border-emerald-500/15 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center mb-6">
              <Cpu className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Autonomous Incident Agent</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Translates raw statistical anomalies into structured actionable tickets with verified financial and volumetric loss estimates.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-slate-900/60 border border-emerald-500/15 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center mb-6">
              <BarChart3 className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Community & Green Challenges</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Gamified behavioral challenges, recycling center locator maps, and auditable verification for LEED and ISO 14001 compliance.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-emerald-500/10 py-10 px-6 text-center text-xs text-slate-500 bg-slate-950">
        <p>© 2026 EcoTrack AI Environmental Intelligence. Open-source, transparent, deterministic sustainability.</p>
      </footer>
    </div>
  )
}
