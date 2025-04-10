export interface User {
    id: number;
    username: string;
    email: string;
    role: "user" | "admin" | "superuser";
    skills?: string[]; // Optional for creation
    }

export interface Skill {
    id: number;
    name: string;
    category: string;
    isSignedOff: boolean;
}
