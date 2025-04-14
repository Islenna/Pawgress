import { useState } from "react"
import { useAuth } from "@/lib/authContext"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { toast } from "sonner"
import axiosInstance from "@/lib/axiosInstance"

const Register = () => {
    const { login } = useAuth()
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [firstName, setFirstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [licenseNumber, setLicenseNumber] = useState("")
    const [licenseExpiry, setLicenseExpiry] = useState("")
    const [isRVT, setIsRVT] = useState(false)
    const [error, setError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")

        if (password !== confirmPassword) {
            setError("Passwords do not match.")
            return
        }

        if (password.length < 8) {
            toast.error("Password must be at least 8 characters long.")
            return
        }

        try {
            const payload: Record<string, any> = {
                email: email.toLowerCase().trim(),
                password,
                first_name: firstName,
                last_name: lastName,
            }

            if (isRVT) {
                if (licenseNumber) payload.license_number = licenseNumber
                if (licenseExpiry) payload.license_expiry = licenseExpiry
            }

            await axiosInstance.post("/users/register", payload)
            toast.success("Account created. Logging in...")
            await login(email, password)
        } catch (err) {
            console.error(err)
            setError("Registration failed. Try a different email.")
            toast.error("Registration failed.")
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen px-4 bg-background">
            <Card className="w-full max-w-sm shadow-lg">
                <CardHeader>
                    <CardTitle className="text-center text-2xl">Create a new account</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <Label htmlFor="email">Email</Label>
                            <Input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="password">Password</Label>
                            <Input id="password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="confirm-password">Confirm Password</Label>
                            <Input id="confirm-password" type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="first-name">First Name</Label>
                            <Input id="first-name" type="text" value={firstName} onChange={e => setFirstName(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="last-name">Last Name</Label>
                            <Input id="last-name" type="text" value={lastName} onChange={e => setLastName(e.target.value)} required />
                        </div>

                        {/* RVT Checkbox */}
                        <div className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                id="is-rvt"
                                checked={isRVT}
                                onChange={(e) => setIsRVT(e.target.checked)}
                            />
                            <Label htmlFor="is-rvt" className="cursor-pointer">I’m an RVT</Label>
                        </div>

                        {/* Conditional RVT Fields */}
                        {isRVT && (
                            <>
                                <div>
                                    <Label htmlFor="license-number">License Number</Label>
                                    <Input id="license-number" type="text" value={licenseNumber} onChange={e => setLicenseNumber(e.target.value)} />
                                </div>
                                <div>
                                    <Label htmlFor="license-expiry">License Expiry</Label>
                                    <Input id="license-expiry" type="date" value={licenseExpiry} onChange={e => setLicenseExpiry(e.target.value)} />
                                </div>
                            </>
                        )}

                        {error && <p className="text-red-500 text-sm">{error}</p>}
                        <Button type="submit" className="w-full">Register</Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}

export default Register
