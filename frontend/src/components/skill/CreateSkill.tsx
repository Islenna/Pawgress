import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import Form, { Field } from "../shared/Form"

const CreateSkill = () => {
    const [categoryOptions, setCategoryOptions] = useState<{ label: string; value: string }[]>([])

    useEffect(() => {
        axiosInstance.get("/categories").then(res => {
            const options = res.data.map((cat: any) => ({
                label: cat.name,
                value: String(cat.id),
            }))
            setCategoryOptions(options)
        })
    }, [])

    const handleSubmit = async (data: Record<string, string>) => {
        await axiosInstance.post("/skills", data)
        alert("Skill created!")
    }

    const fields: Field[] = [
        { name: "name", label: "Skill Name", type: "text" },
        { name: "description", label: "Description", type: "textarea" },
        {
            name: "category_id",
            label: "Category",
            type: "select",
            options: categoryOptions,
        },
    ]

    return <Form fields={fields} onSubmit={handleSubmit} />
}

export default CreateSkill
