// src/types/index.ts
export interface User {
    id: number;
    username: string;
    email: string;
    role: "user" | "admin" | "superuser";
    is_active: boolean;
    license_number?: string | null;
    license_expiry?: string | null; // Usually comes as a string from JSON
}

export interface Skill {
    id: number;
    name: string;
    category: string;
    isSignedOff: boolean;
}
