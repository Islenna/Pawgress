import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { User } from "@/types"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/lib/authContext"


function AdminUsersPage() {
    const { user } = useAuth()
    if (!user || (user.role !== "admin" && user.role !== "superuser")) {
        return <p className="text-center mt-10 text-muted-foreground">You do not have permission to view this page.</p>
    }
    const [users, setUsers] = useState<User[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const res = await axiosInstance.get("/users")
                const sorted = res.data.sort((a: User, b: User) =>
                    a.last_name.localeCompare(b.last_name, undefined, { sensitivity: "base" })
                )

                setUsers(sorted)
            } catch (err) {
                setError("Failed to load users")
                toast.error("Failed to load users")
                console.error(err)
            } finally {
                setLoading(false)
            }
        }

        fetchUsers()
    }, [])


    if (loading) return <p className="text-center mt-10 text-muted-foreground">Loading users...</p>
    if (error) return <p className="text-center text-red-500">{error}</p>

    if (users.length === 0) return <p className="text-center mt-10 text-muted-foreground">No users found.</p>
    // Delete Functionality
    const handleDelete = async (userId: number) => {
        if (confirm("Are you sure you want to delete this user?")) {
            try {
                await axiosInstance.delete(`/users/${userId}`)
                setUsers(users.filter(user => user.id !== userId))
                toast.success("User deleted successfully")
            } catch (err) {
                toast.error("Failed to delete user")
                console.error(err)
            }
        }
    }
    // Edit Functionality (Placeholder for now)
    const handleEdit = (u: number) => {
        console.log(`Edit user with ID: ${u}`)
        toast.info("Edit functionality not implemented yet")
    }


    return (
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
            <h1 className="text-2xl font-bold text-center">User Management</h1>

            {users.map(u => (
                <Card key={u.id}>
                    <CardContent className="p-4 space-y-2">
                        <p><strong>Name:</strong> {u.first_name} {u.last_name}</p>
                        <p><strong>Email:</strong> {u.email}</p>
                        <p><strong>Role:</strong> {u.role}</p>
                        <p><strong>License #:</strong> {u.license_number || "—"}</p>
                        <p><strong>License Expiry:</strong> {u.license_expiry ? new Date(u.license_expiry).toLocaleDateString() : "—"}</p>
                        <Separator />
                        <div className="flex gap-2 mt-2">
                            <Button variant="outline" size="sm" onClick={() => handleEdit(u.id)}>Edit</Button>
                                <Button variant="destructive" size="sm" onClick={() => handleDelete(u.id)}>Delete</Button>
                        </div>

                    </CardContent>
                </Card>
            ))}
        </div>
    )
}

export default AdminUsersPage
