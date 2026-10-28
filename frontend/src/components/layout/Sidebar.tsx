import React from 'react'
import { NavLink } from 'react-router-dom'
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
  Leaf
} from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ThemeToggle } from '../common/ThemeToggle'

const navItems = [
  { to: '/home', label: 'Home Page', icon: Home },
  { to: '/dashboard', label: 'Main Dashboard', icon: LayoutDashboard },
  { to: '/water', label: 'Water Intelligence', icon: Droplets },
  { to: '/electricity', label: 'Energy & Power', icon: Zap },
  { to: '/waste', label: 'AI Waste Classifier', icon: Trash2 },
  { to: '/incidents', label: 'Incident Triage', icon: AlertTriangle },
  { to: '/carbon', label: 'Carbon Engine', icon: Flame },
  { to: '/recommendations', label: 'AI Recommendations', icon: Lightbulb },
  { to: '/challenges', label: 'Green Challenges', icon: Trophy },
  { to: '/locations', label: 'Recycling Hubs', icon: MapPin },
  { to: '/iot', label: 'IoT Sensor Mesh', icon: Cpu },
  { to: '/reports', label: 'Reports & Export', icon: FileText },
  { to: '/admin', label: 'Administration', icon: Shield, adminOnly: true },
]

export const Sidebar: React.FC = () => {
  const { user } = useAuthStore()
  const isAdmin = user?.role === 'org_admin' || user?.role === 'platform_admin'

  return (
    <aside className="w-64 bg-white/95 dark:bg-slate-900/90 border-r border-slate-200 dark:border-emerald-500/10 flex flex-col backdrop-blur-xl shrink-0 h-screen sticky top-0 transition-colors duration-200">
      <div className="h-16 flex items-center px-6 gap-3 border-b border-slate-200 dark:border-emerald-500/10">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <Leaf className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="font-bold text-slate-900 dark:text-white tracking-wide text-lg flex items-center gap-1.5">
            EcoTrack <span className="text-emerald-600 dark:text-emerald-400 text-xs px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 font-semibold uppercase tracking-wider">AI</span>
          </div>
          <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase font-medium tracking-wider">Environmental Intelligence</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
          Platform Features
        </div>
        {navItems
          .filter(item => !item.adminOnly || isAdmin)
          .map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-emerald-500/10 dark:bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 shadow-sm shadow-emerald-500/10 font-semibold'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span className="truncate">{item.label}</span>
              </NavLink>
            )
          })}
      </nav>

      {/* Visual Theme Mode Switcher */}
      <div className="px-3 pb-3">
        <ThemeToggle variant="sidebar" />
      </div>

      <div className="p-4 border-t border-slate-200 dark:border-emerald-500/10 bg-slate-50 dark:bg-slate-950/40">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-xs font-bold text-emerald-600 dark:text-emerald-400">
            {user?.full_name ? user.full_name[0] : 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">{user?.full_name || 'Active User'}</p>
            <p className="text-[10px] text-emerald-600 dark:text-emerald-400/80 truncate capitalize">{user?.role?.replace('_', ' ') || 'Member'}</p>
          </div>
        </div>
      </div>
    </aside>
  )
}
