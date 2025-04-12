import React from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

type ModalProps = {
    title: string
    isOpen: boolean
    onClose: () => void
    onSubmit?: () => void
    children: React.ReactNode
    submitLabel?: string
}

const CommonModal: React.FC<ModalProps> = ({ title, isOpen, onClose, onSubmit, children, submitLabel }) => {
    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>{title}</DialogTitle>
                </DialogHeader>
                <div className="space-y-4">{children}</div>
                {onSubmit && (
                    <DialogFooter className="mt-4">
                        <Button variant="secondary" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button onClick={onSubmit}>{submitLabel || "Save"}</Button>
                    </DialogFooter>
                )}
            </DialogContent>
        </Dialog>
    )
}

export default CommonModal
