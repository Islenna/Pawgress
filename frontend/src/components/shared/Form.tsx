// components/Form.tsx
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

export type Field = {
    name: string
    label: string
    type: "text" | "textarea" | "select"
    options?: { label: string, value: string }[] // for select
}

interface FormProps {
    fields: Field[]
    onSubmit: (data: Record<string, string>) => void
    defaultValues?: Record<string, string>
}

const Form = ({ fields, onSubmit, defaultValues = {} }: FormProps) => {
    const [formData, setFormData] = useState<Record<string, string>>(defaultValues)

    const handleChange = (name: string, value: string) => {
        setFormData({ ...formData, [name]: value })
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit(formData)
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {fields.map((field) => (
                <div key={field.name}>
                    <Label htmlFor={field.name}>{field.label}</Label>
                    {field.type === "text" && (
                        <Input
                            id={field.name}
                            value={formData[field.name] || ""}
                            onChange={(e) => handleChange(field.name, e.target.value)}
                        />
                    )}
                    {field.type === "textarea" && (
                        <Textarea
                            id={field.name}
                            value={formData[field.name] || ""}
                            onChange={(e) => handleChange(field.name, e.target.value)}
                        />
                    )}
                    {field.type === "select" && field.options && (
                        <select
                            id={field.name}
                            className="w-full border p-2 rounded"
                            value={formData[field.name] || ""}
                            onChange={(e) => handleChange(field.name, e.target.value)}
                        >
                            <option value="">Select one...</option>
                            {field.options.map((opt) => (
                                <option key={opt.value} value={opt.value}>
                                    {opt.label}
                                </option>
                            ))}
                        </select>
                    )}
                </div>
            ))}
            <Button type="submit">Submit</Button>
        </form>
    )
}

export default Form
