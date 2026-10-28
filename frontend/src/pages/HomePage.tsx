import React from 'react'
import { Link } from 'react-router-dom'
import {
  Home,
  LayoutDashboard,
  Droplets,
  Zap,
  Trash2,
  AlertTriangle,
  Flame,
  Lightbulb,
  Trophy,
  MapPin,
  Cpu,
  FileText,
  Shield,
  ArrowRight,
  Activity,
  CheckCircle2,
  Sparkles,
  Leaf
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'

export const HomePage: React.FC = () => {
  const { user, currentOrg } = useAuthStore()

  const modules = [
    {
      title: 'Main Executive Dashboard',
      description: 'High-level KPI metrics, real-time demand curves, and critical incident alerts.',
      icon: LayoutDashboard,
      to: '/dashboard',
      color: 'from-emerald-600 to-teal-500',
      badge: 'Live Overview',
    },
    {
      title: 'Water Intelligence',
      description: 'Ultrasonic flow telemetry, nocturnal leak diagnosis, and baseline Z-score tracking.',
      icon: Droplets,
      to: '/water',
      color: 'from-blue-600 to-cyan-500',
      badge: 'Leak Detection',
    },
    {
      title: 'Energy & Power Analytics',
      description: 'Peak load demand profiling, sub-metering, and tariff cost analytics.',
      icon: Zap,
      to: '/electricity',
      color: 'from-amber-500 to-orange-500',
      badge: 'Peak Shaving',
    },
    {
      title: 'AI Waste Classifier',
      description: 'Computer vision neural classification for dry recyclables, organics, and e-waste.',
      icon: Trash2,
      to: '/waste',
      color: 'from-emerald-500 to-green-600',
      badge: 'Computer Vision',
    },
    {
      title: 'Incident Triage & Response',
      description: 'Autonomous root-cause analysis, ticket assignment, and impact verification workflow.',
      icon: AlertTriangle,
      to: '/incidents',
      color: 'from-rose-500 to-red-600',
      badge: 'Triage Agent',
    },
    {
      title: 'Deterministic Carbon Engine',
      description: 'Calibrated with official CEA (India) grid emission factors and IPCC guidelines.',
      icon: Flame,
      to: '/carbon',
      color: 'from-teal-500 to-emerald-600',
      badge: 'GHG Standards',
    },
    {
      title: 'Actionable Recommendations',
      description: 'AI-prioritized operational roadmaps ranked by payback period and carbon savings.',
      icon: Lightbulb,
      to: '/recommendations',
      color: 'from-yellow-500 to-amber-600',
      badge: 'ROI Optimization',
    },
    {
      title: 'Green Community Challenges',
      description: 'Gamified campus initiatives, EcoPoints awards, and behavioral habit tracking.',
      icon: Trophy,
      to: '/challenges',
      color: 'from-purple-500 to-indigo-600',
      badge: 'Gamification',
    },
    {
      title: 'Campus Recycling Hubs',
      description: 'Locate certified e-waste, composting stations, and paper baling centers.',
      icon: MapPin,
      to: '/locations',
      color: 'from-teal-600 to-cyan-600',
      badge: 'Facility Map',
    },
    {
      title: 'IoT Sensor Mesh',
      description: 'Monitor connected ultrasonic flow meters, smart power panels, and MQTT gateways.',
      icon: Cpu,
      to: '/iot',
      color: 'from-violet-600 to-purple-600',
      badge: 'Telemetry Mesh',
    },
    {
      title: 'Environmental Reports',
      description: 'Export verifiable CSV and PDF audit logs for ISO 14001 and ESG disclosures.',
      icon: FileText,
      to: '/reports',
      color: 'from-blue-500 to-indigo-500',
      badge: 'ESG Export',
    },
  ]

  return (
    <div className="space-y-10">
      {/* Welcome Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-emerald-50/80 via-teal-50/50 to-white dark:from-emerald-950/80 dark:via-slate-900/90 dark:to-teal-950/80 border border-emerald-500/20 p-8 sm:p-10 backdrop-blur-xl shadow-xl transition-all">
        <div className="absolute right-0 top-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>

        <div className="relative z-10 space-y-4 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-semibold uppercase tracking-wider">
            <Activity className="w-3.5 h-3.5 animate-pulse" />
            <span>EcoTrack AI Environmental Platform</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-slate-900 dark:text-white tracking-tight leading-tight">
            Welcome back,{' '}
            <span className="bg-gradient-to-r from-emerald-600 via-teal-500 to-cyan-600 dark:from-emerald-400 dark:via-teal-300 dark:to-cyan-300 bg-clip-text text-transparent">
              {user?.full_name || 'Sustainability Lead'}
            </span>
          </h1>

          <p className="text-slate-600 dark:text-slate-300 text-sm sm:text-base leading-relaxed">
            Active facility:{' '}
            <span className="text-emerald-600 dark:text-emerald-400 font-bold">{currentOrg?.name || 'EcoTech Smart Campus'}</span>
            . All autonomous monitoring agents are online, tracking utility telemetry, predicting resource anomalies, and quantifying carbon reduction.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-4">
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-xl shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5"
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Open Main Dashboard</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>

            <Link
              to="/waste"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 dark:bg-slate-900 dark:hover:bg-slate-800 dark:text-slate-200 dark:border-slate-700 font-semibold text-sm transition-colors shadow-sm"
            >
              <Trash2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
              <span>AI Waste Scanner</span>
            </Link>

            <Link
              to="/incidents"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 dark:bg-slate-900 dark:hover:bg-slate-800 dark:text-slate-200 dark:border-slate-700 font-semibold text-sm transition-colors shadow-sm"
            >
              <AlertTriangle className="w-4 h-4 text-rose-500 dark:text-rose-400" />
              <span>Review Incidents</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Live System Status Badges */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-500 dark:text-blue-400 flex items-center justify-center shrink-0">
            <Droplets className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Water Sub-system</span>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Online (2 Meters)
            </span>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-500 dark:text-amber-400 flex items-center justify-center shrink-0">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Power Grid</span>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Online (2 Panels)
            </span>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-500/10 text-teal-500 dark:text-teal-400 flex items-center justify-center shrink-0">
            <Flame className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Carbon Engine</span>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> CEA 0.716 Factor
            </span>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-500 dark:text-purple-400 flex items-center justify-center shrink-0">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">IoT Sensor Mesh</span>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> MQTT Connected
            </span>
          </div>
        </div>
      </div>

      {/* Feature Navigation Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              Platform Feature Directory
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Explore and launch any of the specialized environmental intelligence modules.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {modules.map((m) => {
            const Icon = m.icon
            return (
              <Link
                key={m.to}
                to={m.to}
                className="p-6 rounded-3xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/40 hover:bg-slate-50/80 dark:hover:bg-slate-900/95 shadow-sm hover:shadow-md transition-all group flex flex-col justify-between space-y-4 relative overflow-hidden"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className={`w-12 h-12 rounded-2xl bg-gradient-to-tr ${m.color} flex items-center justify-center text-white shadow-lg shadow-emerald-500/10 group-hover:scale-105 transition-transform`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 uppercase tracking-wider">
                      {m.badge}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                    {m.title}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                    {m.description}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs font-semibold text-slate-500 dark:text-slate-400 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                  <span>Launch Module</span>
                  <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
