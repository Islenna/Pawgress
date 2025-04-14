// src/components/user/Login.tsx
import { useState } from "react"
import { useAuth } from "@/lib/authContext"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import PasswordInput from "../ui/PasswordInput"

const Login = () => {
    const { login } = useAuth()
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        try {
            await login(email.toLowerCase().trim(), password)
        } catch {
            setError("Invalid login. Please try again.")
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>
            <div>
                <Label htmlFor="password">Password</Label>
                <PasswordInput id="password" value={password} onChange={e => setPassword(e.target.value)} required />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button className="w-full" type="submit">Sign In</Button>
        </form>
    )
}
export default Login
