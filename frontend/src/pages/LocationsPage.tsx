import React, { useEffect, useState } from 'react'
import {
  MapPin,
  Clock,
  CheckCircle,
  Phone,
  Recycle,
  Filter,
  Layers
} from 'lucide-react'
import { locationsApi } from '../api/endpoints'

export const LocationsPage: React.FC = () => {
  const [locations, setLocations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [filterType, setFilterType] = useState<string>('')

  useEffect(() => {
    setLoading(true)
    locationsApi.list({ type: filterType || undefined })
      .then((data) => setLocations(data))
      .catch((err) => console.error('Failed to load recycling locations:', err))
      .finally(() => setLoading(false))
  }, [filterType])

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <MapPin className="w-8 h-8 text-teal-400" />
          Campus & Community Recycling Network
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Authorized e-waste collectors, composting hubs, and certified baling drop-offs.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center gap-3 bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
        <Filter className="w-4 h-4 text-emerald-400" />
        <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Facility Type:</span>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="bg-slate-950 border border-slate-800 text-xs text-slate-200 rounded-xl px-3 py-1.5 focus:outline-none focus:border-emerald-500"
        >
          <option value="">All Recycling Centers</option>
          <option value="e_waste">E-Waste & Batteries</option>
          <option value="compost">Compost & Organics</option>
          <option value="paper">Paper & Cardboard</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {locations.map((loc) => (
          <div
            key={loc.id}
            className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/30 transition-all flex flex-col justify-between space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-teal-400 bg-teal-500/10 px-3 py-1 rounded-full border border-teal-500/20 uppercase">
                  {loc.location_type?.replace('_', ' ')}
                </span>
                <span className="text-[11px] font-mono text-slate-500">
                  {loc.city || 'Campus'}
                </span>
              </div>

              <h3 className="text-lg font-bold text-white">{loc.name}</h3>
              <p className="text-xs text-slate-400">{loc.address}</p>

              {loc.accepts_categories && (
                <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs text-slate-300">
                  <span className="text-[10px] text-slate-500 font-semibold uppercase block mb-1">Accepted Items</span>
                  <div className="flex flex-wrap gap-1.5">
                    {((loc.accepts_categories as any)?.categories || []).map((cat: string) => (
                      <span key={cat} className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 capitalize">
                        {cat.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="pt-3 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                <span>{loc.operating_hours || 'Mon-Sat 09:00 - 18:00'}</span>
              </span>
              <span className="text-[11px] font-mono text-emerald-400/80">
                {loc.latitude?.toFixed(4)}, {loc.longitude?.toFixed(4)}
              </span>
            </div>
          </div>
        ))}

        {locations.length === 0 && !loading && (
          <div className="p-16 text-center text-slate-500 text-xs bg-slate-900/40 rounded-3xl border border-slate-800/60 col-span-3">
            No recycling locations registered for this filter.
          </div>
        )}
      </div>
    </div>
  )
}
