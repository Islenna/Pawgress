import { useEffect, useState } from "react"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import axiosInstance from "@/lib/axiosInstance"
import { User, Category, Proficiency } from "@/types"
import { useAuth } from "@/lib/authContext"
import UserProficiencyAccordion from "@/components/proficiencies/UserProficiencyAccordion"
import { toast } from "sonner"

const UserProficiencyTab = () => {
    const { user } = useAuth()
    const [users, setUsers] = useState<User[]>([])
    const [selectedUserId, setSelectedUserId] = useState<string>("")
    const [proficiencies, setProficiencies] = useState<Proficiency[]>([])
    const [categories, setCategories] = useState<Category[]>([])
    const [search, setSearch] = useState<string>("")

    useEffect(() => {
        axiosInstance.get("/users").then(res => setUsers(res.data))
        axiosInstance.get("/categories").then(res => setCategories(res.data))
    }, [])

    useEffect(() => {
        if (selectedUserId) {
            axiosInstance.get(`/proficiencies?user_id=${selectedUserId}`)
                .then(res => setProficiencies(res.data))
        }
    }, [selectedUserId])

    const profMap = new Map(proficiencies.map(p => [p.skill_id, p.proficiency]))

    const handleUpdate = async (skillId: number, newValue: number) => {
        await axiosInstance.post("/proficiencies", {
            user_id: Number(selectedUserId),
            skill_id: skillId,
            proficiency: newValue,
            signed_off_by: user?.id,
            signed_off_at: new Date().toISOString()
        })
        const updated = await axiosInstance.get(`/proficiencies?user_id=${selectedUserId}`)
        setProficiencies(updated.data)
        toast.success("Proficiency updated successfully!")
    }

    const selectedUser = users.find(u => u.id === Number(selectedUserId))

    const filteredUsers = users.filter(u =>
        `${u.first_name} ${u.last_name}`.toLowerCase().includes(search.toLowerCase())
    )

    return (
        <div className="space-y-4">
            <div className="relative w-full max-w-lg">
                <Input
                    type="text"
                    placeholder="Search users..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="mb-1 w-full"
                />
                {search && (
                    <div className="absolute z-10 bg-muted text-sm rounded-md w-full max-h-60 overflow-y-auto border shadow-md">
                        {filteredUsers.length > 0 ? (
                            filteredUsers.map(u => (
                                <div
                                    key={u.id}
                                    className="px-4 py-2 hover:bg-accent cursor-pointer"
                                    onClick={() => {
                                        setSelectedUserId(u.id.toString())
                                        setSearch("")
                                    }}
                                >
                                    {u.first_name} {u.last_name}
                                </div>
                            ))
                        ) : (
                            <div className="px-4 py-2 text-muted-foreground">No users found.</div>
                        )}
                    </div>
                )}
            </div>

            {/* ✅ Only visible to superusers */}
            {user?.role === "superuser" && selectedUser && (
                <div className="bg-muted p-3 rounded-md border mb-2">
                    <p className="text-sm font-medium mb-1">
                        Edit role for <span className="font-semibold">{selectedUser.first_name} {selectedUser.last_name}</span>
                    </p>
                    <div className="flex items-center gap-4">
                        <Label htmlFor="role" className="text-sm">Role:</Label>
                        <select
                            className="border rounded px-2 py-1 bg-background text-foreground"
                            value={selectedUser.role}
                            disabled={selectedUser.role === "superuser"}
                            onChange={async (e) => {
                                const newRole = e.target.value
                                try {
                                    await axiosInstance.put(`/users/${selectedUserId}`, {
                                        ...selectedUser,
                                        role: newRole,
                                    })
                                    toast.success(`Role updated to ${newRole}`)
                                    const updated = await axiosInstance.get("/users")
                                    setUsers(updated.data)
                                } catch (err) {
                                    toast.error("Failed to update role.")
                                    console.error(err)
                                }
                            }}
                        >
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>
                </div>
            )}

            {selectedUserId && (
                <UserProficiencyAccordion
                    categories={categories}
                    userProficiencies={Object.fromEntries(profMap)}
                    onProficiencyChange={handleUpdate}
                    editable={true}
                />
            )}
        </div>
    )
}

export default UserProficiencyTab
