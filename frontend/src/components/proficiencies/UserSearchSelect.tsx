import { User } from "@/types"
import {
    Command,
    CommandInput,
    CommandItem,
    CommandList,
    CommandEmpty,
    CommandGroup,
} from "@/components/ui/command"
import { ScrollArea } from "@/components/ui/scroll-area"

type Props = {
    users: User[]
    value: string
    onChange: (val: string) => void
}

const UserSearchSelect = ({ users, value, onChange }: Props) => {
    const selected = users.find(u => u.id.toString() === value)

    return (
        <Command className="rounded-md border shadow-md w-full max-w-md">
            <CommandInput placeholder="Search users..." />
            <CommandList>
                <CommandEmpty>No users found.</CommandEmpty>
                <ScrollArea className="max-h-60">
                    <CommandGroup heading="Users">
                        {users.map(user => (
                            <CommandItem
                                key={user.id}
                                value={user.id.toString()}
                                onSelect={() => onChange(user.id.toString())}
                            >
                                {user.first_name} {user.last_name}
                            </CommandItem>
                        ))}
                    </CommandGroup>
                </ScrollArea>
            </CommandList>
        </Command>
    )
}

export default UserSearchSelect
