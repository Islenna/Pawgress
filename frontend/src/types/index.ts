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

export type Skill = {
    id: number;
    name: string;
    category_id: number;
    category_name: string;
    description: string;
    proficiency?: number;
};

export type Category = {
    id: number;
    name: string;
    description: string;
    skills: Skill[];
};

export type Proficiency = {
    id: number;
    user_id: number;
    skill_id: number;
    proficiency: number;
    signed_off_by?: number | null;
    signed_off_at?: string | null; // Usually comes as a string from 
    
};

