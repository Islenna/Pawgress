import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import CommonModal from "@/components/shared/Modal"
import { Skill, Category } from "@/types"

const SkillTable = () => {
    const [skills, setSkills] = useState<Skill[]>([])
    const [categories, setCategories] = useState<Category[]>([])
    const [isOpen, setIsOpen] = useState(false)
    const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null)
    const [editedName, setEditedName] = useState("")
    const [editedDescription, setEditedDescription] = useState("")
    const [editedCategoryId, setEditedCategoryId] = useState<number | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            const [skillsRes, catsRes] = await Promise.all([
                axiosInstance.get("/skills"),
                axiosInstance.get("/categories"),
            ])
            setSkills(skillsRes.data)
            setCategories(catsRes.data)
        }

        fetchData()
    }, [])

    const toggleModal = (skillId: number) => {
        const skill = skills.find(s => s.id === skillId) || null
        setSelectedSkill(skill)
        setEditedName(skill?.name || "")
        setEditedDescription(skill?.description || "")
        setEditedCategoryId(skill?.category_id || null)
        setIsOpen(true)
    }

    const handleDelete = async (id: number) => {
        await axiosInstance.delete(`/skills/${id}`)
        setSkills(prev => prev.filter(s => s.id !== id))
    }

    const handleSubmit = async () => {
        if (!selectedSkill || editedCategoryId === null) return

        const updated = {
            ...selectedSkill,
            name: editedName,
            description: editedDescription,
            category_id: editedCategoryId,
        }

        const res = await axiosInstance.put(`/skills/${selectedSkill.id}`, updated)
        setSkills(prev => prev.map(s => (s.id === selectedSkill.id ? res.data : s)))
        setIsOpen(false)
    }

    return (
        <div className="space-y-2">
            {skills.map(skill => (
                <div key={skill.id} className="flex justify-between items-center border p-2 rounded">
                    <div>
                        <p className="font-medium">{skill.name}</p>
                        <p className="text-sm text-muted-foreground">
                            Category: {categories.find(c => c.id === skill.category_id)?.name || "Unknown"}
                        </p>
                    </div>
                    <div className="space-x-2">
                        <Button onClick={() => toggleModal(skill.id)} size="sm" variant="outline">Edit</Button>
                        <Button onClick={() => handleDelete(skill.id)} size="sm" variant="destructive">Delete</Button>
                    </div>
                </div>
            ))}

            <CommonModal
                title="Edit Skill"
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
                onSubmit={handleSubmit}
                submitLabel="Save Changes"
            >
                <div className="space-y-4">
                    <Input
                        value={editedName}
                        onChange={(e) => setEditedName(e.target.value)}
                        placeholder="Skill Name"
                    />
                    <Textarea
                        value={editedDescription}
                        onChange={(e) => setEditedDescription(e.target.value)}
                        placeholder="Description"
                        className="min-h-[100px]"
                    />
                    <select
                        className="w-full p-2 rounded border"
                        value={editedCategoryId ?? ""}
                        onChange={(e) => setEditedCategoryId(Number(e.target.value))}
                    >
                        <option value="" disabled>Select category</option>
                        {categories.map(c => (
                            <option key={c.id} value={c.id}>{c.name}</option>
                        ))}
                    </select>
                </div>
            </CommonModal>
        </div>
    )
}

export default SkillTable
