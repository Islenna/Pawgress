// src/components/skill/CreateSkill.tsx
import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import Form, { Field } from "../shared/Form"
import { toast } from "sonner"
import { blockDemoAction } from "@/lib/permissions"
import { useAuth } from "@/lib/authContext"

type CreateSkillProps = {
    onSuccess: () => void
}

const CreateSkill = ({ onSuccess }: CreateSkillProps) => {
    const [categoryOptions, setCategoryOptions] = useState<{ label: string; value: string }[]>([])
    const { user } = useAuth()

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
        if (blockDemoAction(user)) return
        await axiosInstance.post("/skills", data)
        toast.success("Skill created!")
        onSuccess() // 🧠 refetch data in parent
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
