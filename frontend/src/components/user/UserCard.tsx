import React from "react";
import { User } from "../../types";

interface UserCardProps {
    user: User;
}

const UserCard: React.FC<UserCardProps> = ({ user }) => {
    return (
        <div className="border p-4 rounded shadow-sm bg-white">
            <h2 className="text-xl font-bold">{`${user.first_name} ${user.last_name}`
}</h2>
            <p>Email: {user.email}</p>
            <p className="text-sm text-gray-600">Role: {user.role}</p>
        </div>
    );
};

export default UserCard;
