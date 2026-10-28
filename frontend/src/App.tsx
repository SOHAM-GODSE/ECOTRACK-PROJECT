import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { LandingPage } from './pages/LandingPage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { Layout } from './components/layout/Layout'
import { HomePage } from './pages/HomePage'
import { DashboardPage } from './pages/DashboardPage'
import { WaterPage } from './pages/WaterPage'
import { ElectricityPage } from './pages/ElectricityPage'
import { WastePage } from './pages/WastePage'
import { IncidentsPage } from './pages/IncidentsPage'
import { CarbonPage } from './pages/CarbonPage'
import { RecommendationsPage } from './pages/RecommendationsPage'
import { ChallengesPage } from './pages/ChallengesPage'
import { LocationsPage } from './pages/LocationsPage'
import { IoTPage } from './pages/IoTPage'
import { ReportsPage } from './pages/ReportsPage'
import { AdminPage } from './pages/AdminPage'

export const App: React.FC = () => {
  return (
    <Routes>
      {/* Public Pages */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Authenticated Workspace App */}
      <Route element={<Layout />}>
        <Route path="/home" element={<HomePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/water" element={<WaterPage />} />
        <Route path="/electricity" element={<ElectricityPage />} />
        <Route path="/waste" element={<WastePage />} />
        <Route path="/incidents" element={<IncidentsPage />} />
        <Route path="/carbon" element={<CarbonPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/challenges" element={<ChallengesPage />} />
        <Route path="/locations" element={<LocationsPage />} />
        <Route path="/iot" element={<IoTPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
