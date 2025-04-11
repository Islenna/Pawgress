import './App.css'
import { AuthProvider } from './lib/authContext'
import { BrowserRouter } from 'react-router-dom'
import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import UserDashboard from './components/user/UserDashboard'
import Navbar from './components/layout/Navbar'
import AdminPanel from '@/pages/AdminPanel'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/me" element={<UserDashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
