import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { ReactNode } from "react"

type ModalProps = {
    isOpen: boolean
    onClose: () => void
    title: string
    onSave: () => void
    children?: ReactNode
    submitLabel?: string // ✅ Add this
}

const CommonModal = ({ isOpen, onClose, title, onSave, children, submitLabel = "Save" }: ModalProps) => {
    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent aria-describedby="modal-description">
                <DialogHeader>
                    <DialogTitle>{title}</DialogTitle>
                </DialogHeader>
                <div id="modal-description" className="py-4">{children}</div>
                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>Cancel</Button>
                    <Button onClick={onSave}>{submitLabel}</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}

export default CommonModal
