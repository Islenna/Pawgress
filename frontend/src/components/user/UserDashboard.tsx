// src/components/dashboard/UserDashboard.tsx

import { useEffect, useState, useMemo } from "react"
import { useAuth } from "@/lib/authContext"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogTrigger, DialogContent, DialogTitle } from "@/components/ui/dialog"
import { Link } from "react-router-dom"
import axiosInstance from "@/lib/axiosInstance"
import { toast } from "sonner"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import PasswordInput from "../ui/PasswordInput"
import CommonModal from "@/components/shared/Modal"
import ShoutoutFeed from "@/components/shoutout/ShoutoutFeed"
import ShoutoutForm from "@/components/shoutout/ShoutoutForm"
import { Shoutout } from "@/types"

const UserDashboard = () => {
    const { user, setUser } = useAuth()
    const [firstName, setFirstName] = useState(user?.first_name || "")
    const [lastName, setLastName] = useState(user?.last_name || "")
    const [licenseNumber, setLicenseNumber] = useState(user?.license_number || "")
    const [licenseExpiry, setLicenseExpiry] = useState(user?.license_expiry || "")
    const [email, setEmail] = useState(user?.email || "")
    const [currentPassword, setCurrentPassword] = useState("")
    const [newPassword, setNewPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [showShoutoutModal, setShowShoutoutModal] = useState(false)
    const [shoutouts, setShoutouts] = useState<Shoutout[]>([])

    // Load shoutouts on page load
    const fetchShoutouts = async () => {
        try {
            const res = await axiosInstance.get("/shoutouts")
            setShoutouts(res.data)
        } catch {
            toast.error("Couldn't load shoutouts")
            setShoutouts([])
        }
    }

    useEffect(() => {
        fetchShoutouts()
    }, [])

    const hasChanges = useMemo(() => {
        return (
            firstName !== (user?.first_name || "") ||
            lastName !== (user?.last_name || "") ||
            licenseNumber !== (user?.license_number || "") ||
            licenseExpiry !== (user?.license_expiry || "")
        )
    }, [firstName, lastName, licenseNumber, licenseExpiry, user])

    const handlePasswordUpdate = async () => {
        if (newPassword !== confirmPassword) {
            toast.error("New passwords do not match.")
            return
        }
        try {
            await axiosInstance.put("/users/update-password", {
                current_password: currentPassword,
                new_password: newPassword,
            })
            toast.success("Password updated successfully!")
            setCurrentPassword("")
            setNewPassword("")
            setConfirmPassword("")
        } catch (err: any) {
            const errors = err.response?.data?.detail
            if (Array.isArray(errors)) {
                toast.error(errors[0]?.msg || "Password update failed.")
            } else {
                toast.error(typeof errors === "string" ? errors : "Password update failed.")
            }
        }
    }



    if (!user) {
        return <p className="text-center mt-10 text-muted-foreground">Loading user info...</p>
    }
    const handleUpdateUser = async () => {
        try {
            await axiosInstance.put(`/users/${user!.id}`, {
                first_name: firstName,
                last_name: lastName,
                license_number: licenseNumber,
                license_expiry: licenseExpiry,
            })
    
            // Refresh updated user info into context
            const response = await axiosInstance.get("/users/me")
            setUser(response.data)
    
            toast.success("User info updated successfully!")
        } catch (err: any) {
            const errors = err.response?.data?.detail
            if (Array.isArray(errors)) {
                toast.error(errors[0]?.msg || "Update failed.")
            } else {
                toast.error(typeof errors === "string" ? errors : "Update failed.")
            }
        }
    }

    return (
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
            <h1 className="text-3xl font-bold text-center">
                Welcome back, {`${user.first_name} ${user.last_name}`} 👋
            </h1>

            <Card>
                <CardContent className="space-y-4 p-6">
                    <div className="space-y-1">
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>License #:</strong> {user.license_number || "Not set"}</p>
                        <p><strong>License Expiry:</strong> {user.license_expiry ? new Date(user.license_expiry).toLocaleDateString() : "Not set"}</p>
                    </div>

                    <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 pt-4 border-t border-muted">
                        <Button variant="secondary" asChild>
                            <Link to="/ce">CE Management</Link>
                        </Button>

                        <div className="flex flex-col sm:flex-row gap-2">
                            <Button asChild>
                                <Link to="/skills">View Skills</Link>
                            </Button>

                            <Dialog>
                                <DialogTrigger asChild>
                                    <Button variant="outline">Account Settings</Button>
                                </DialogTrigger>
                                <DialogContent className="space-y-4 overflow-visible max-h-screen z-[100]">
                                    <DialogTitle>Account Settings</DialogTitle>

                                    {/* Basic Info Section */}
                                    <div className="space-y-2">
                                        <Input
                                            value={firstName}
                                            onChange={(e) => setFirstName(e.target.value)}
                                            placeholder="Preferred Name"
                                        />
                                        <Input
                                            value={lastName}
                                            onChange={(e) => setLastName(e.target.value)}
                                            placeholder="Last Name"
                                        />
                                        <Input
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            placeholder="Email"
                                            disabled
                                        />
                                        <Input
                                            value={licenseNumber}
                                            onChange={(e) => setLicenseNumber(e.target.value)}
                                            placeholder="License Number"
                                        />
                                        <Input
                                            type="date"
                                            value={licenseExpiry}
                                            onChange={(e) => setLicenseExpiry(e.target.value)}
                                            placeholder="License Expiry"
                                        />
                                        <Button onClick={handleUpdateUser} disabled={!hasChanges}>
                                            Update Info
                                        </Button>
                                    </div>
                                    <Separator className="my-4" />
                                    {/* Password Change Section */}
                                    <div className="space-y-2">
                                        <PasswordInput
                                            value={currentPassword}
                                            onChange={(e) => setCurrentPassword(e.target.value)}
                                            placeholder="Current Password"
                                        />
                                        <PasswordInput
                                            value={newPassword}
                                            onChange={(e) => setNewPassword(e.target.value)}
                                            placeholder="New Password"
                                        />
                                        <PasswordInput
                                            value={confirmPassword}
                                            onChange={(e) => setConfirmPassword(e.target.value)}
                                            placeholder="Confirm New Password"
                                        />
                                        <Button onClick={handlePasswordUpdate}>Update Password</Button>
                                    </div>
                                </DialogContent>


                            </Dialog>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card className="w-full max-w-sm mx-auto">
                <CardContent className="p-6 space-y-4">
                    <div className="flex flex-col items-center gap-2 sm:flex-row sm:justify-between">
                        <h2 className="text-xl font-semibold">Shoutouts</h2>
                        <Button onClick={() => setShowShoutoutModal(true)}>Give a Shoutout</Button>
                    </div>

                    <ShoutoutFeed shoutouts={shoutouts} />

                    <CommonModal
                        isOpen={showShoutoutModal}
                        onClose={() => setShowShoutoutModal(false)}
                        title="Give a Shoutout"
                        onSave={() => { }}
                    >
                        <ShoutoutForm
                            onClose={() => setShowShoutoutModal(false)}
                            onShoutoutSent={fetchShoutouts}
                        />
                    </CommonModal>
                </CardContent>
            </Card>
        </div>
    )
}

export default UserDashboard
