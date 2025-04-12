import { useAuth } from "@/lib/authContext"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom"

const UserDashboard = () => {
    const { user, logout } = useAuth()

    if (!user) {
        return <p className="text-center mt-10 text-muted-foreground">Loading user info...</p>
    }

    return (
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
            <h1 className="text-3xl font-bold">Welcome back, {user.username} 👋</h1>

            <Card>
                <CardContent className="space-y-2 p-4">
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Role:</strong> {user.role}</p>
                    <p><strong>License #:</strong> {user.license_number || "Not set"}</p>
                    <p><strong>License Expiry:</strong>
                        {user.license_expiry ? new Date(user.license_expiry).toLocaleDateString() : "Not set"}
                    </p>
                    <div className="flex justify-end gap-2">
                        <Button asChild>
                            <Link to="/skills">View Skills</Link>
                        </Button>
                        <Button variant="destructive" onClick={logout}>
                            Log out
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <div className="flex justify-end">
                <Button variant="destructive" onClick={logout}>
                    Log out
                </Button>
            </div>
        </div>
    )
}

export default UserDashboard
