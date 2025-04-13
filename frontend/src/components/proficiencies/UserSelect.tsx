import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { User } from "@/types";

type Props = {
    users: User[];
    value: string;
    onChange: (val: string) => void;
};

const UserSelect = ({ users, value, onChange }: Props) => (
    <Select onValueChange={onChange} value={value}>
        <SelectTrigger><SelectValue placeholder="Select User" /></SelectTrigger>
        <SelectContent>
            {users.map(u => (
                <SelectItem key={u.id} value={u.id.toString()}>
                    {u.first_name} {u.last_name}
                </SelectItem>

            ))}
        </SelectContent>
    </Select>
);

export default UserSelect;