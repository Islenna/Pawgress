import Form, { Field } from './../shared/Form'
import axiosInstance from "@/lib/axiosInstance"

const CreateCategory = () => {
    const handleSubmit = async (data: Record<string, string>) => {
        await axiosInstance.post("/categories", data)
        alert("Category created!")
    }

    const fields: Field[] = [
        { name: "name", label: "Category Name", type: "text" },
        { name: "description", label: "Description", type: "textarea" },
    ]


    return <Form fields={fields} onSubmit={handleSubmit} />
}

export default CreateCategory
