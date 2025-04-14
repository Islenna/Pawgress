import { useState } from "react"
import { User } from "@/types"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"

type Props = {
    users: User[]
    value: string
    onChange: (val: string) => void
}

const UserSearchSelect = ({ users, value, onChange }: Props) => {
    const [searchQuery, setSearchQuery] = useState("")
    const [showDropdown, setShowDropdown] = useState(false)

    const filteredUsers = users.filter(user => {
        const fullName = `${user.first_name || ""} ${user.last_name || ""}`.toLowerCase()
        return fullName.includes(searchQuery.toLowerCase())
    })

    return (
        <div className="relative w-full">
            <Input
                placeholder="Search users..."
                value={searchQuery}
                onChange={(e) => {
                    setSearchQuery(e.target.value)
                    setShowDropdown(true)
                }}
                onFocus={() => setShowDropdown(true)}
                className="mb-1"
            />
            {showDropdown && searchQuery && (
                <ScrollArea className="absolute z-10 w-full max-h-60 bg-muted rounded-md border shadow-md overflow-y-auto">
                    {filteredUsers.length > 0 ? (
                        filteredUsers.map(user => (
                            <div
                                key={user.id}
                                className="px-4 py-2 hover:bg-accent cursor-pointer"
                                onClick={() => {
                                    onChange(user.id.toString())
                                    setSearchQuery(`${user.first_name} ${user.last_name}`)
                                    setShowDropdown(false)
                                }}
                            >
                                {user.first_name} {user.last_name}
                            </div>
                        ))
                    ) : (
                        <div className="px-4 py-2 text-muted-foreground">No users found.</div>
                    )}
                </ScrollArea>
            )}
        </div>
    )
}

export default UserSearchSelect
