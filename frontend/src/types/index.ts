// src/types/index.ts
export interface User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    role: "user" | "admin" | "superuser";
    is_active: boolean;
    license_number?: string | null;
    license_expiry?: string | null; // Usually comes as a string from JSON
}

export type Skill = {
    id: number
    name: string
    description: string
    category_id?: number
    proficiency?: number
    signed_off_by?: {
    first_name: string
    last_name: string
    }
    signed_off_at?: string
}


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

