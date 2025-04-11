import Form, { Field } from './../shared/Form'
import axiosInstance from "@/lib/axiosInstance"

const CreateSkill = () => {
    const handleSubmit = async (data: Record<string, string>) => {
        await axiosInstance.post("/skills", data)
        alert("Skill created!")
    }

    const fields: Field[] = [
        { name: "name", label: "Skill Name", type: "text" },
        { name: "description", label: "Description", type: "textarea" },
    ]


    return <Form fields={fields} onSubmit={handleSubmit} />
}

export default CreateSkill
