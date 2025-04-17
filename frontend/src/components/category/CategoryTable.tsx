import { useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import CommonModal from "@/components/shared/Modal"
import { Category } from "@/types"
import { toast } from "sonner"
import { useAuth } from "@/lib/authContext"
import { blockDemoAction } from "@/lib/permissions"

type CategoryTableProps = {
    categories: Category[]
    fetchData: () => void
}

const CategoryTable = ({ categories, fetchData }: CategoryTableProps) => {
    const { user } = useAuth()
    const [isOpen, setIsOpen] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState<Category | null>(null)
    const [editedName, setEditedName] = useState("")
    const [editedDescription, setEditedDescription] = useState("")
    const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false)
    const [deleteConfirmText, setDeleteConfirmText] = useState("")

    const confirmDelete = (category: Category) => {
        setSelectedCategory(category)
        setDeleteConfirmText("")
        setConfirmDeleteOpen(true)
    }

    const toggleModal = (category: Category) => {
        setSelectedCategory(category)
        setEditedName(category.name)
        setEditedDescription(category.description)
        setIsOpen(true)
    }

    const handleDelete = async () => {
        if (blockDemoAction(user)) return
        if (!selectedCategory) return
        if (deleteConfirmText !== selectedCategory.name) {
            toast.error("Category name does not match.")
            return
        }

        await axiosInstance.delete(`/categories/${selectedCategory.id}`)
        await fetchData()
        setConfirmDeleteOpen(false)
        setSelectedCategory(null)
    }


    const handleSubmit = async () => {
        if (blockDemoAction(user)) return
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
                        <Button onClick={() => confirmDelete(cat)} size="sm" variant="destructive">
                            Delete
                        </Button>

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
            <CommonModal
                title={`Delete Category: ${selectedCategory?.name}`}
                isOpen={confirmDeleteOpen}
                onClose={() => setConfirmDeleteOpen(false)}
                onSave={handleDelete}
                submitLabel="Confirm Deletion"
            >
                <p className="text-sm text-muted-foreground mb-4">
                    This will delete <strong>all skills</strong> associated with <strong>{selectedCategory?.name}</strong>. This action <strong>cannot</strong> be undone.
                </p>

                <p className="text-sm text-muted-foreground mb-2">
                    To confirm, type <strong>{selectedCategory?.name}</strong> below:
                </p>
                <Input
                    value={deleteConfirmText}
                    onChange={(e) => setDeleteConfirmText(e.target.value)}
                    placeholder="Category name"
                />
            </CommonModal>


        </div>
    )
}

export default CategoryTable
