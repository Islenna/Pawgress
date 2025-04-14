import React, { useEffect, useState } from "react"
import { toast } from "sonner"
import axiosInstance from "@/lib/axiosInstance"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import UserSearchSelect from "@/components/proficiencies/UserSearchSelect"
import { User } from "@/types"

type ShoutoutFormProps = {
    onClose: () => void
    onShoutoutSent?: () => void
}

const ShoutoutForm = ({ onClose, onShoutoutSent }: ShoutoutFormProps) => {
    const [users, setUsers] = useState<User[]>([])
    const [message, setMessage] = useState("")
    const [targetUserId, setTargetUserId] = useState("")

    useEffect(() => {
        axiosInstance.get("/users/")
            .then(res => setUsers(res.data))
            .catch(() => toast.error("Failed to load users"))
    }, [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await axiosInstance.post("/shoutouts/", {
                message,
                target_user_id: targetUserId ? parseInt(targetUserId) : null,
            })
            toast.success("Shoutout sent!")
            onClose()
            onShoutoutSent?.() // ✅ refresh if provided
        } catch {
            toast.error("Failed to send shoutout.")
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block mb-1 font-medium">Message</label>
                <Textarea value={message} onChange={(e) => setMessage(e.target.value)} />
            </div>

            <div>
                <label className="block mb-1 font-medium">Give this shoutout to someone?</label>
                <UserSearchSelect users={users} value={targetUserId} onChange={setTargetUserId} />
            </div>

            <div className="flex justify-end gap-2 pt-4">
                <Button variant="outline" type="button" onClick={onClose}>Cancel</Button>
                <Button type="submit">Send Shoutout</Button>
            </div>
        </form>
    )
}

export default ShoutoutForm
