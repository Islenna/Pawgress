import { Input } from "@/components/ui/input"

type SearchBarProps = {
    value: string
    onChange: (value: string) => void
    placeholder?: string
}

const SearchBar = ({ value, onChange, placeholder = "Search..." }: SearchBarProps) => {
    return (
        <div className="w-full max-w-md">
            <Input
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
            />
        </div>
    )
}

export default SearchBar
