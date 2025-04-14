import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import SkillAccordion from "@/components/skill/SkillAccordion"
import { Category, Skill } from "@/types"
import { useAuth } from '@/lib/authContext'
import CommonModal from "../shared/Modal"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import SearchBar from "@/components/shared/SearchBar"

type SkillTableProps = {
    categories: Category[]
    fetchData: () => void
}

const SkillTable = ({ categories, fetchData }: SkillTableProps) => {
    const { user } = useAuth()
    const [localCategories, setLocalCategories] = useState<Category[]>(categories)
    const [isOpen, setIsOpen] = useState(false)
    const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null)
    const [editedName, setEditedName] = useState("")
    const [editedDescription, setEditedDescription] = useState("")
    const [editedCategoryId, setEditedCategoryId] = useState<number | null>(null)
    const [searchTerm, setSearchTerm] = useState("")

    useEffect(() => {
        setLocalCategories(categories)
    }, [categories])

    const handleSave = async () => {
        if (selectedSkill) {
            const res = await axiosInstance.put(`/skills/${selectedSkill.id}`, {
                name: editedName,
                description: editedDescription,
                category_id: editedCategoryId
            })
            await fetchData()
            setLocalCategories(prevCategories => {
                return prevCategories.map(category => {
                    if (category.id === res.data.category_id) {
                        return {
                            ...category,
                            skills: category.skills.map(skill => {
                                if (skill.id === selectedSkill.id) {
                                    return { ...skill, name: editedName, description: editedDescription }
                                }
                                return skill
                            })
                        }
                    }
                    return category
                })
            })
            setIsOpen(false)

            setSelectedSkill(null)
        }
    }

    const handleDelete = async (skillId: number) => {
        await axiosInstance.delete(`/skills/${skillId}`)
        await fetchData()
        setIsOpen(false)
        setSelectedSkill(null)
    }

    const filteredCategories = localCategories
        .map(cat => ({
            ...cat,
            skills: cat.skills.filter(skill =>
                skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                skill.description.toLowerCase().includes(searchTerm.toLowerCase())
            )
        }))
        .filter(cat => cat.skills.length > 0)

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            <h2 className="text-2xl font-bold">All Skills</h2>
            <SearchBar
                value={searchTerm}
                onChange={setSearchTerm}
                placeholder="Search skills..."
            />
            <SkillAccordion
                categories={filteredCategories}
                editable={user?.role === "admin" || user?.role === "superuser"}
                onEditClick={(skill) => {
                    setSelectedSkill(skill)
                    setEditedName(skill.name)
                    setEditedDescription(skill.description)
                    setEditedCategoryId(skill.category_id ?? null)
                    setIsOpen(true)
                }}
            />
            <CommonModal
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
                title="Edit Skill"
                onSave={handleSave}
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
                    <div className="flex justify-end">
                        <button
                            className="text-red-500 text-sm underline"
                            onClick={async () => {
                                if (selectedSkill) {
                                    const confirm = window.confirm(`Are you sure you want to delete "${selectedSkill.name}"?`)
                                    if (confirm) {
                                        await handleDelete(selectedSkill.id)
                                    }
                                }
                            }}
                        >
                            Delete Skill
                        </button>
                    </div>
                </div>
            </CommonModal>
        </div>
    )
}

export default SkillTable
