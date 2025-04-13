// components/Form.tsx
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import {
    Select,
    SelectTrigger,
    SelectValue,
    SelectContent,
    SelectItem,
} from "@/components/ui/select"

export type Field = {
    name: string
    label: string
    type: FieldType
    options?: { label: string, value: string }[]
}

type FieldType = "text" | "textarea" | "select" | "date"

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
                    {field.type === "date" && (
                        <Input
                            id={field.name}
                            type="date"
                            value={formData[field.name] || ""}
                            onChange={(e) => handleChange(field.name, e.target.value)}
                        />
                    )}
                    {field.type === "select" && field.options && (
                        <Select onValueChange={(val) => handleChange(field.name, val)}>
                            <SelectTrigger id={field.name}>
                                <SelectValue placeholder="Select one..." />
                            </SelectTrigger>
                            <SelectContent className="max-h-72 overflow-y-auto z-50">
                                {field.options?.map((opt) => (
                                    <SelectItem key={opt.value} value={opt.value}>
                                        {opt.label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>


                    )}

                </div>
            ))}
            <Button type="submit">Submit</Button>
        </form>
    )
}

export default Form
