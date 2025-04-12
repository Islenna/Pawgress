// src/context/AuthContext.tsx
import { createContext, useContext, useEffect, useState } from "react";
import axiosInstance from "@/lib/axiosInstance";
import { useNavigate } from "react-router-dom";
import { User } from "@/types"; // Adjust the import path as necessary


interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (emailOrUsername: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
    const navigate = useNavigate();

    useEffect(() => {
        if (token && !user) {
            // Try to fetch /me
            axiosInstance
                .get("/users/me")
                .then((res) => setUser(res.data))
                .catch(() => logout()); // Token might be invalid
        }
    }, [token]);

    const login = async (usernameOrEmail: string, password: string) => {
        const formData = new URLSearchParams();
        formData.append("username", usernameOrEmail);
        formData.append("password", password);

        const res = await axiosInstance.post("/auth/login", formData, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        const { access_token } = res.data;
        localStorage.setItem("token", access_token);
        setToken(access_token);

        const userRes = await axiosInstance.get("/users/me");
        setUser(userRes.data);
        navigate("/"); // Or wherever
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
        setToken(null);
        navigate("/");
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hook
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error("useAuth must be used within an AuthProvider");
    return context;
};
