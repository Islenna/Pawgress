import { useEffect, useState } from "react"
import { useAuth } from "@/lib/authContext"
import axiosInstance from "@/lib/axiosInstance"
import { Card, CardContent } from "@/components/ui/card"
import Form, { Field } from "@/components/shared/Form"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { toast } from "sonner"

type CERecord = {
    id: number
    ce_type: string
    ce_date: string
    ce_hours: number
    ce_description: string
    ce_file_path?: string
    created_at: string
    updated_at: string
}

const ceFields: Field[] = [
    { name: "ce_type", label: "Type (e.g., Anesthesia, Live)", type: "text" },
    { name: "ce_hours", label: "Hours (e.g., 5)", type: "text" },
    { name: "ce_description", label: "Description (e.g., Conference, Webinar, etc.)", type: "textarea" },
    { name: "ce_date", label: "Date (YYYY-MM-DD)", type: "date" }
]

const CEManagement = () => {
    const { user } = useAuth()
    const [records, setRecords] = useState<CERecord[]>([])
    const [loading, setLoading] = useState(true)
    const [showForm, setShowForm] = useState(false)
    const [uploadFile, setUploadFile] = useState<File | null>(null)
    const [editingId, setEditingId] = useState<number | null>(null)
    const [editFormData, setEditFormData] = useState<Record<string, string>>({})
    const [editUploadFile, setEditUploadFile] = useState<File | null>(null)

    useEffect(() => {
        const fetchRecords = async () => {
            try {
                const res = await axiosInstance.get(`/ce_records/user/${user?.id}`)
                setRecords(res.data)
            } catch (err) {
                console.error("Failed to fetch CE records", err)
            } finally {
                setLoading(false)
            }
        }
        if (user?.id) fetchRecords()
    }, [user])

    if (loading) return <p className="text-center mt-10 text-muted-foreground">Loading CE records...</p>

    const totalHours = records.reduce((sum, record) => sum + record.ce_hours, 0)

    const handleCECreate = async (data: Record<string, string>) => {
        if (
            !data.ce_type.trim() ||
            !data.ce_date ||
            !data.ce_hours.trim() ||
            !data.ce_description.trim()
        ) {
            toast.warning("Please fill out all fields before submitting.")
            return
        }
        try {
            const res = await axiosInstance.post("/ce_records/", {
                ...data,
                ce_hours: parseInt(data.ce_hours),
                ce_date: new Date(data.ce_date).toISOString(),
            })

            const newRecordId = res.data.id

            // Handle file upload if one exists
            if (uploadFile) {
                const formData = new FormData()
                formData.append("file", uploadFile)

                await axiosInstance.post(`/ce_records/${newRecordId}/upload`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                })
            }

            // Refresh CE list
            const updated = await axiosInstance.get(`/ce_records/user/${user?.id}`)
            setRecords(updated.data)
            setShowForm(false)
            setUploadFile(null)
        } catch (err) {
            console.error("Error creating CE record", err)
        }
    }

    const today = new Date().toISOString().slice(0, 10) // "YYYY-MM-DD"
    const defaultValues = {
        ce_type: "",
        ce_date: today,
        ce_hours: "",
        ce_description: "",
    }
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

    const handleCEUpdate = async (id: number, data: Record<string, string>) => {
        try {
            await axiosInstance.put(`/ce_records/${id}`, {
                ...data,
                ce_hours: parseInt(data.ce_hours),
                ce_date: new Date(data.ce_date).toISOString(),
            })
            toast.success("CE record updated!")

            if (editUploadFile) {
                const formData = new FormData()
                formData.append("file", editUploadFile)
                await axiosInstance.post(`/ce_records/${id}/upload`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                })
            }

            const updated = await axiosInstance.get(`/ce_records/user/${user?.id}`)
            setRecords(updated.data)
            setEditingId(null)
            setEditUploadFile(null)
        } catch (err) {
            console.error("Error updating CE record", err)
            toast.error("Failed to update CE record.")
        }

    }
    const isImage = (path?: string) => !!path && /\.(png|jpe?g|gif)$/i.test(path)
    const handleDownloadAll = async () => {
        try {
            const response = await axiosInstance.get(`/ce_records/${user?.id}/download`, {
                responseType: "blob",
            })
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement("a")
            link.href = url
            link.setAttribute("download", "ce_records.zip")
            document.body.appendChild(link)
            link.click()
            toast.success("Certificates downloaded!")
        }
        catch (err) {
            console.error("Error downloading certificates", err)
            toast.error("Failed to download certificates.")
        }

    }

    return (
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
            <h1 className="text-3xl font-bold mb-4">📚 CE Management</h1>

            {/* Progress Bar */}
            <div>
                <h2 className="text-xl font-semibold mb-2">CE Progress</h2>
                <div className="w-full bg-muted rounded-full h-4">
                    <div
                        className={`h-4 rounded-full ${totalHours >= 20 ? "bg-green-500" : "bg-blue-500"
                            }`}
                        style={{ width: `${Math.min((totalHours / 20) * 100, 100)}%` }}
                    ></div>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">
                    {totalHours} / 20 hours required
                    {totalHours >= 20 && " ✅ You’re ready for re-certification! 🎉"}
                </p>

                {totalHours > 20 && (
                    <p className="mt-2 text-sm font-semibold text-purple-400 animate-pulse">
                        🌟 Overachiever! You’ve logged {totalHours} hours.
                    </p>
                )}
            </div>
            <Button
                variant="outline"
                onClick={() => {
                    window.open(`${BACKEND_URL}/api/ce_records/user/${user?.id}/download-all`, "_blank")
                }}
            >
                ⬇️ Download All CE Records
            </Button>
            {/* Add CE button and form */}
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold">Records</h2>
                <Button onClick={() => setShowForm(!showForm)}>➕ Add CE Record</Button>
            </div>

            {showForm && (
                <div className="bg-muted p-4 rounded-md mt-4">
                    <Form fields={ceFields} onSubmit={handleCECreate} defaultValues={defaultValues} />
                    <div className="mt-2">
                        <Label htmlFor="ceUpload">Attach Certificate (optional):</Label>
                        <Input
                            id="ceUpload"
                            type="file"
                            onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                        />
                    </div>
                </div>
            )}

            {/* CE Cards */}
            {records.length === 0 ? (
                <p className="text-muted-foreground">No CE records found.</p>
            ) : (
                records

                    .sort((a, b) => new Date(b.ce_date).getTime() - new Date(a.ce_date).getTime())

                    .map((rec) => (
                        <Card key={rec.id}>

                            <CardContent className="p-4 space-y-2">
                                <p><strong>Type:</strong> {rec.ce_type}</p>
                                <p><strong>Date:</strong> {new Date(rec.ce_date).toLocaleDateString()}</p>
                                <p><strong>Hours:</strong> {rec.ce_hours}</p>
                                <p><strong>Description:</strong> {rec.ce_description}</p>

                                {rec.ce_file_path && isImage(rec.ce_file_path) && (
                                    <img
                                        src={`${BACKEND_URL}${rec.ce_file_path}`}
                                        alt="Uploaded CE File"
                                        className="max-h-48 mt-2 rounded border"
                                    />
                                )}



                                <div className="flex gap-2 mt-2">
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => {
                                            setEditingId(rec.id)
                                            setEditFormData({
                                                ce_type: rec.ce_type,
                                                ce_date: rec.ce_date.slice(0, 10),
                                                ce_hours: rec.ce_hours.toString(),
                                                ce_description: rec.ce_description,
                                            })
                                        }}
                                    >
                                        ✏️ Edit
                                    </Button>
                                    <Button
                                        variant="destructive"
                                        size="sm"
                                        onClick={async () => {
                                            try {
                                                await axiosInstance.delete(`/ce_records/${rec.id}`)
                                                toast.success("CE record deleted.")
                                                const updated = await axiosInstance.get(`/ce_records/user/${user?.id}`)
                                                setRecords(updated.data)
                                            } catch (err) {
                                                toast.error("Failed to delete record")
                                            }
                                        }}
                                    >
                                        🗑️ Delete
                                    </Button>
                                </div>

                                {editingId === rec.id && (
                                    <div className="bg-muted p-4 rounded-md mt-4">
                                        <Form
                                            fields={ceFields}
                                            onSubmit={(data) => handleCEUpdate(rec.id, data)}
                                            defaultValues={editFormData}
                                        />
                                        <div className="mt-2">
                                            <Label>Replace Certificate (optional):</Label>
                                            <Input
                                                type="file"
                                                onChange={(e) => setEditUploadFile(e.target.files?.[0] || null)}
                                            />
                                        </div>
                                        <Button variant="ghost" onClick={() => setEditingId(null)}>
                                            Cancel
                                        </Button>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    ))
            )}

        </div>
    )

}

export default CEManagement
