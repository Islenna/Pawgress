import { useAuth } from "@/lib/authContext"
import Login from "@/components/user/Login"
import UserDashboard from "@/components/user/UserDashboard"

const Dashboard = () => {
    const { user } = useAuth()

    return user ? <UserDashboard /> : <Login />
}

export default Dashboard
