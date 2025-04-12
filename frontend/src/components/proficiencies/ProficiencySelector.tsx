// src/components/proficiency/ProficiencySelector.tsx
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select"

type Props = {
    value: number
    onChange: (level: number) => void
    editable?: boolean
}

export const ProficiencySelector = ({ value, onChange, editable = false }: Props) => {
    const levels = [
        "None",
        "Awareness",
        "Assisted",
        "Independent",
        "Competent",
        "Mentor",
    ]

    if (!editable) {
        return (
            <span className="text-sm text-muted-foreground italic">
                {value > 0 ? `${value} – ${levels[value]}` : "Unrated"}
            </span>
        )
    }

    return (
        <Select
            value={value.toString()}
            onValueChange={(val) => onChange(parseInt(val))}
        >
            <SelectTrigger>
                <SelectValue placeholder="Select level" />
            </SelectTrigger>
            <SelectContent>
                {[1, 2, 3, 4, 5].map((n) => (
                    <SelectItem key={n} value={n.toString()}>
                        {n} – {levels[n]}
                    </SelectItem>
                ))}
            </SelectContent>
        </Select>
    )
}
