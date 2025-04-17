import Form, { Field } from './../shared/Form'
import axiosInstance from "@/lib/axiosInstance"
import { toast } from 'sonner'
import { blockDemoAction } from '@/lib/permissions'
import { useAuth } from "@/lib/authContext"

type CreateCategoryProps = {
    onSuccess: () => void
}

const CreateCategory = ({ onSuccess }: CreateCategoryProps) => {
    const { user } = useAuth()
    const handleSubmit = async (data: Record<string, string>) => {
        if (blockDemoAction(user)) return
        await axiosInstance.post("/categories", data)
        toast.success("Category created!")
        onSuccess()
    }
    

    const fields: Field[] = [
        { name: "name", label: "Category Name", type: "text" },
        { name: "description", label: "Description", type: "textarea" },
    ]


    return <Form fields={fields} onSubmit={handleSubmit} />
}

export default CreateCategory
