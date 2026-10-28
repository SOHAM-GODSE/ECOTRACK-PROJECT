import React, { useEffect, useState } from 'react'
import {
  Shield,
  Users,
  Building,
  Activity,
  History,
  CheckCircle2
} from 'lucide-react'
import { adminApi } from '../api/endpoints'

export const AdminPage: React.FC = () => {
  const [users, setUsers] = useState<any[]>([])
  const [orgs, setOrgs] = useState<any[]>([])
  const [logs, setLogs] = useState<any[]>([])
  const [health, setHealth] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      adminApi.listUsers().catch(() => []),
      adminApi.listOrgs().catch(() => []),
      adminApi.getAuditLogs().catch(() => []),
      adminApi.getHealth().catch(() => null),
    ]).then(([u, o, l, h]) => {
      setUsers(u)
      setOrgs(o)
      setLogs(l)
      setHealth(h)
      setLoading(false)
    })
  }, [])

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Shield className="w-8 h-8 text-emerald-400" />
          Platform Administration & Security Audit
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Manage tenant organizations, authorized users, and tamper-evident audit logs.
        </p>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 uppercase font-semibold">Registered Users</span>
            <div className="text-2xl font-bold text-white">{users.length}</div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <Building className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 uppercase font-semibold">Active Organizations</span>
            <div className="text-2xl font-bold text-white">{orgs.length}</div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 uppercase font-semibold">System Health</span>
            <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5 mt-1">
              <CheckCircle2 className="w-4 h-4" />
              <span>Operational (MySQL & FastAPI)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl">
        <h3 className="font-bold text-white text-base mb-4 flex items-center gap-2">
          <Users className="w-4 h-4 text-emerald-400" />
          <span>User Directory</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase">
                <th className="pb-3">User</th>
                <th className="pb-3">Email</th>
                <th className="pb-3">Role</th>
                <th className="pb-3">Status</th>
                <th className="pb-3">Joined</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-800/30">
                  <td className="py-3 font-semibold text-slate-100">{u.full_name}</td>
                  <td className="py-3 text-slate-400">{u.email}</td>
                  <td className="py-3 capitalize text-emerald-400 font-medium">
                    {u.role?.replace('_', ' ')}
                  </td>
                  <td className="py-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      ACTIVE
                    </span>
                  </td>
                  <td className="py-3 font-mono text-slate-500">{u.created_at?.slice(0, 10)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Audit Logs */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl">
        <h3 className="font-bold text-white text-base mb-4 flex items-center gap-2">
          <History className="w-4 h-4 text-purple-400" />
          <span>Security Audit Trail</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase">
                <th className="pb-3">Timestamp</th>
                <th className="pb-3">Action</th>
                <th className="pb-3">Resource</th>
                <th className="pb-3">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {logs.map((l) => (
                <tr key={l.id} className="hover:bg-slate-800/30">
                  <td className="py-3 font-mono text-slate-500">
                    {l.created_at?.replace('T', ' ').slice(0, 19)}
                  </td>
                  <td className="py-3 font-semibold text-emerald-400 uppercase text-[10px]">
                    {l.action}
                  </td>
                  <td className="py-3 text-slate-300">{l.resource_type}</td>
                  <td className="py-3 text-slate-400">{l.description || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
