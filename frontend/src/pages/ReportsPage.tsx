import React, { useState } from 'react'
import {
  FileText,
  Download,
  Calendar,
  CheckCircle2,
  FileSpreadsheet,
  ShieldCheck
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'

export const ReportsPage: React.FC = () => {
  const { currentOrg } = useAuthStore()
  const [downloading, setDownloading] = useState(false)

  const handleDownloadCsv = () => {
    setDownloading(true)
    setTimeout(() => {
      // Generate synthetic CSV download
      const headers = ['Date', 'Metric', 'Value', 'Unit', 'CO2e_kg', 'Status']
      const rows = [
        ['2026-10-28', 'Water Consumption', '2150', 'Liters', '0.45', 'Normal'],
        ['2026-10-28', 'Electricity Consumption', '420', 'kWh', '300.72', 'Normal'],
        ['2026-10-27', 'Water Consumption', '2310', 'Liters', '0.48', 'Normal'],
        ['2026-10-27', 'Electricity Consumption', '445', 'kWh', '318.62', 'Normal'],
        ['2026-10-25', 'Water Consumption - Leak Spike', '8200', 'Liters', '1.72', 'Anomaly Flagged'],
      ]
      const csvContent =
        'data:text/csv;charset=utf-8,' +
        [headers.join(','), ...rows.map((e) => e.join(','))].join('\n')
      const encodedUri = encodeURI(csvContent)
      const link = document.createElement('a')
      link.setAttribute('href', encodedUri)
      link.setAttribute(
        'download',
        `ecotrack_${currentOrg?.slug || 'facility'}_environmental_audit_2026.csv`
      )
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      setDownloading(false)
    }, 600)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <FileText className="w-8 h-8 text-blue-400" />
          Environmental Audit & Compliance Exports
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Export certified telemetry data for ISO 14001, ESG disclosures, and municipal reporting.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <FileSpreadsheet className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Consolidated CSV Telemetry Export</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Complete historical dump of water meters, electricity kWh logs, carbon calculations, and resolved anomalies.
            </p>
          </div>

          <button
            onClick={handleDownloadCsv}
            disabled={downloading}
            className="w-full flex items-center justify-center gap-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-500/20 transition-all text-xs"
          >
            <Download className="w-4 h-4" />
            <span>{downloading ? 'Preparing CSV...' : 'Download 30-Day Audit Log (CSV)'}</span>
          </button>
        </div>

        <div className="p-6 rounded-3xl bg-slate-900/80 border border-emerald-500/15 backdrop-blur-xl flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">ESG & Indian CEA Compliance Verification</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Standardized format cross-referenced with Central Electricity Authority Baseline Database Version 18.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-slate-400">
            Certified timestamp: <span className="text-emerald-400 font-mono">2026-10-28 15:30:00 UTC</span>
          </div>
        </div>
      </div>
    </div>
  )
}
