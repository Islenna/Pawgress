import './App.css'
import { AuthProvider } from './lib/authContext'
import { BrowserRouter } from 'react-router-dom'
import { Routes, Route } from 'react-router-dom'
import UserDashboard from './components/user/UserDashboard'
import LoginRegister from './components/user/LoginRegister'
import Navbar from './components/layout/Navbar'
import AdminPanel from '@/pages/AdminPanel'
import SkillsPage from '@/components/user/SkillsPage'
import CEManagement from './components/CE/CEManagement'
import { Toaster } from '@/components/ui/sonner'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<LoginRegister />} />
          <Route path="/me" element={<UserDashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/skills" element={<SkillsPage />} />
          <Route path="/ce" element={<CEManagement />} />
        </Routes>
        <Toaster richColors position="top-right" />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
