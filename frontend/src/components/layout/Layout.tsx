import React, { useEffect, useState } from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { Navbar } from './Navbar'
import { useAuthStore } from '../../store/authStore'
import { orgApi } from '../../api/endpoints'

export const Layout: React.FC = () => {
  const { isAuthenticated, currentOrg, setCurrentOrg, setOrganizations } = useAuthStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated()) {
      setLoading(false)
      return
    }

    orgApi.listMy()
      .then((orgs) => {
        setOrganizations(orgs)
        if (orgs.length > 0 && !currentOrg) {
          setCurrentOrg(orgs[0])
        }
      })
      .catch((err) => {
        console.error('Failed to load user organizations:', err)
      })
      .finally(() => setLoading(false))
  }, [isAuthenticated, setCurrentOrg, setOrganizations])

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center text-emerald-500">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-600 dark:text-slate-300">Loading EcoTrack workspace...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-row text-slate-800 dark:text-slate-100 transition-colors duration-200">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />
        <main className="flex-1 p-6 md:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
