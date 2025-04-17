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
    is_demo_user: boolean;
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
    signed_off_by_user?: User // This is the user who signed off the skill
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

export type Shoutout = {
    id: number;
    message: string;
    created_at: string;
    sender_first_name?: string;
    recipient_first_name?: string;
};

export type CE = {
    id: number;
    user_id: number;
    ce_type: string;
    ce_hours: number;
    ce_date: string; // Usually comes as a string from JSON
    ce_approved_by?: number | null; // This is the user who approved the CE
    ce_approved_at?: string | null; // Usually comes as a string from JSON
};

export type MetricsResponse = {
    total_skills: number
    total_proficiencies: number
    signed_off_proficiencies: number
    avg_proficiency_per_skill: Record<number, number> // skill_id -> avg
    category_breakdown: {
    category: string
    total: number
    signed_off: number
    avg_proficiency: number
    }[]
}