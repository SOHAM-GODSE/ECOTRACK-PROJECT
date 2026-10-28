import React from 'react'
import { Sun, Moon } from 'lucide-react'
import { useThemeStore } from '../../store/themeStore'

interface ThemeToggleProps {
  variant?: 'compact' | 'segmented' | 'sidebar'
  className?: string
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ variant = 'segmented', className = '' }) => {
  const { theme, setTheme, toggleTheme } = useThemeStore()
  const isDark = theme === 'dark'

  if (variant === 'sidebar') {
    return (
      <div className={`p-3 rounded-2xl bg-slate-100 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 transition-all ${className}`}>
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
            {isDark ? <Moon className="w-3.5 h-3.5 text-indigo-400" /> : <Sun className="w-3.5 h-3.5 text-amber-500" />}
            Theme Mode
          </span>
          <span className="text-[10px] font-semibold text-emerald-600 dark:text-emerald-400 capitalize">
            {isDark ? 'Night' : 'Day'}
          </span>
        </div>
        <div className="grid grid-cols-2 p-1 rounded-xl bg-slate-200/80 dark:bg-slate-950/70 border border-slate-300/60 dark:border-slate-800 text-xs font-semibold">
          <button
            type="button"
            onClick={() => setTheme('light')}
            className={`flex items-center justify-center gap-1.5 py-1.5 rounded-lg transition-all ${
              !isDark
                ? 'bg-white text-slate-900 shadow-sm shadow-slate-400/20 font-bold border border-slate-200'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sun className="w-3.5 h-3.5 text-amber-500" />
            <span>Day</span>
          </button>
          <button
            type="button"
            onClick={() => setTheme('dark')}
            className={`flex items-center justify-center gap-1.5 py-1.5 rounded-lg transition-all ${
              isDark
                ? 'bg-slate-800 text-white shadow-sm font-bold border border-emerald-500/30'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <Moon className="w-3.5 h-3.5 text-indigo-400" />
            <span>Night</span>
          </button>
        </div>
      </div>
    )
  }

  // Segmented Pill in Navbar
  return (
    <div
      className={`inline-flex items-center p-1 rounded-xl bg-slate-100 dark:bg-slate-800/90 border border-slate-300/80 dark:border-emerald-500/20 shadow-sm transition-all ${className}`}
      role="group"
      aria-label="Theme toggle"
    >
      <button
        type="button"
        onClick={() => setTheme('light')}
        title="Switch to Day Mode (Light Theme)"
        className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition-all ${
          !isDark
            ? 'bg-white text-slate-900 shadow-sm shadow-slate-300 border border-slate-200'
            : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        <Sun className={`w-3.5 h-3.5 ${!isDark ? 'text-amber-500' : 'text-slate-400'}`} />
        <span>Day</span>
      </button>

      <button
        type="button"
        onClick={() => setTheme('dark')}
        title="Switch to Night Mode (Dark Theme)"
        className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition-all ${
          isDark
            ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
            : 'text-slate-600 hover:text-slate-900'
        }`}
      >
        <Moon className={`w-3.5 h-3.5 ${isDark ? 'text-slate-950' : 'text-slate-500'}`} />
        <span>Night</span>
      </button>
    </div>
  )
}
