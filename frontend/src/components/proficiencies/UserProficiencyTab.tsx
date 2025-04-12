import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { User, Category, Proficiency } from "@/types"
import { useAuth } from "@/lib/authContext"
import UserSelect from "@/components/proficiencies/UserSelect"
import UserProficiencyAccordion from "@/components/proficiencies/UserProficiencyAccordion"


const UserProficiencyTab = () => {
    const { user } = useAuth()
    const [users, setUsers] = useState<User[]>([])
    const [selectedUserId, setSelectedUserId] = useState("")
    const [proficiencies, setProficiencies] = useState<Proficiency[]>([])
    const [categories, setCategories] = useState<Category[]>([])

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
    }

    return (
        <div className="space-y-4">
            <UserSelect users={users} value={selectedUserId} onChange={setSelectedUserId} />
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