import { useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import CommonModal from "@/components/shared/Modal"
import { Category } from "@/types"

type CategoryTableProps = {
    categories: Category[]
    fetchData: () => void
}

const CategoryTable = ({ categories, fetchData }: CategoryTableProps) => {
    const [isOpen, setIsOpen] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState<Category | null>(null)
    const [editedName, setEditedName] = useState("")
    const [editedDescription, setEditedDescription] = useState("")

    const toggleModal = (category: Category) => {
        setSelectedCategory(category)
        setEditedName(category.name)
        setEditedDescription(category.description)
        setIsOpen(true)
    }

    const handleDelete = async (id: number) => {
        await axiosInstance.delete(`/categories/${id}`)
        await fetchData()
    }

    const handleSubmit = async () => {
        if (!selectedCategory) return

        await axiosInstance.put(`/categories/${selectedCategory.id}`, {
            name: editedName,
            description: editedDescription,
        })

        await fetchData()
        setIsOpen(false)
        setSelectedCategory(null)
    }

    return (
        <div className="space-y-2">
            {categories.map((cat) => (
                <div key={cat.id} className="flex justify-between items-center border p-2 rounded">
                    <span>{cat.name}</span>
                    <div className="space-x-2">
                        <Button onClick={() => toggleModal(cat)} size="sm" variant="outline">Edit</Button>
                        <Button onClick={() => handleDelete(cat.id)} size="sm" variant="destructive">Delete</Button>
                    </div>
                </div>
            ))}

            <CommonModal
                title="Edit Category"
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
                onSave={handleSubmit}
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
