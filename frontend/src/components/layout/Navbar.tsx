import React from 'react'
import { Bell, LogOut, Building } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ThemeToggle } from '../common/ThemeToggle'
import { useNavigate } from 'react-router-dom'

export const Navbar: React.FC = () => {
  const { user, currentOrg, organizations, setCurrentOrg, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="h-16 border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/90 backdrop-blur-xl px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30 transition-colors duration-200 shadow-sm">
      <div className="flex items-center gap-3 sm:gap-4">
        {organizations && organizations.length > 0 ? (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800/90 border border-slate-200 dark:border-emerald-500/20 text-xs">
            <Building className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <select
              value={currentOrg?.id || ''}
              onChange={(e) => {
                const found = organizations.find((o) => o.id === Number(e.target.value))
                if (found) setCurrentOrg(found)
              }}
              className="bg-transparent text-slate-900 dark:text-slate-100 font-semibold focus:outline-none cursor-pointer"
            >
              {organizations.map((org) => (
                <option key={org.id} value={org.id} className="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
                  {org.name}
                </option>
              ))}
            </select>
          </div>
        ) : (
          <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
            <Building className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span className="font-semibold text-slate-800 dark:text-slate-200">{currentOrg?.name || 'Default Campus'}</span>
          </div>
        )}

        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[11px] text-emerald-700 dark:text-emerald-400 font-bold">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          AI Monitoring Active
        </div>
      </div>

      <div className="flex items-center gap-3 sm:gap-4">
        {/* Unmissable Segmented Day / Night Mode Switch */}
        <ThemeToggle variant="segmented" />

        <div className="h-5 w-px bg-slate-200 dark:bg-slate-800 hidden sm:block"></div>

        <button
          title="Notifications"
          className="relative p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800/60 transition-colors"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-emerald-500"></span>
        </button>

        <div className="h-5 w-px bg-slate-200 dark:bg-slate-800"></div>

        <div className="flex items-center gap-2.5">
          <div className="text-right hidden md:block">
            <p className="text-xs font-bold text-slate-900 dark:text-slate-100">{user?.full_name}</p>
            <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">{user?.email}</p>
          </div>
          <button
            onClick={handleLogout}
            title="Sign Out"
            className="p-2 rounded-xl text-slate-400 hover:text-rose-500 hover:bg-rose-500/10 transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  )
}
