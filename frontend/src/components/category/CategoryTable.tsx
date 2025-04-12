import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import CommonModal from "@/components/shared/Modal"
import { Category } from "@/types"

const CategoryTable = () => {
    const [categories, setCategories] = useState<Category[]>([])
    const [isOpen, setIsOpen] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState<Category | null>(null)
    const [editedName, setEditedName] = useState("")
    const [editedDescription, setEditedDescription] = useState("")

    useEffect(() => {
        axiosInstance.get("/categories").then(res => setCategories(res.data))
    }, [])

    const toggleModal = (categoryId: number) => {
        const cat = categories.find(c => c.id === categoryId) || null
        setSelectedCategory(cat)
        setEditedName(cat?.name || "")
        setEditedDescription(cat?.description || "")
        setIsOpen(true)
    }

    const handleDelete = async (id: number) => {
        await axiosInstance.delete(`/categories/${id}`)
        setCategories(prev => prev.filter(c => c.id !== id))
    }

    const handleSubmit = async () => {
        if (!selectedCategory) return
        const updated = {
            ...selectedCategory,
            name: editedName,
            description: editedDescription,
        }

        const res = await axiosInstance.put(`/categories/${selectedCategory.id}`, updated)
        setCategories(prev =>
            prev.map(c => (c.id === selectedCategory.id ? res.data : c))
        )
        setIsOpen(false)
    }

    return (
        <div className="space-y-2">
            {categories.map((cat) => (
                <div key={cat.id} className="flex justify-between items-center border p-2 rounded">
                    <span>{cat.name}</span>
                    <div className="space-x-2">
                        <Button onClick={() => toggleModal(cat.id)} size="sm" variant="outline">Edit</Button>
                        <Button size="sm" variant="destructive" onClick={() => handleDelete(cat.id)}>Delete</Button>
                    </div>
                </div>
            ))}

            <CommonModal
                title="Edit Category"
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
                onSubmit={handleSubmit}
                submitLabel="Save Changes"
            >
                <div className="space-y-4">
                    <Input
                        value={editedName}
                        onChange={(e) => setEditedName(e.target.value)}
                        placeholder="Category Name"
                    />
                    <Textarea
                        value={editedDescription}
                        onChange={(e) => setEditedDescription(e.target.value)}
                        placeholder="Description"
                        className="min-h-[100px]"
                    />
                </div>
            </CommonModal>
        </div>
    )
}

export default CategoryTable
