// permissions.ts

import { toast } from "sonner";
import { User } from "@/types";

export function blockDemoAction(user: User | null, action?: string): boolean {
    if (user?.is_demo_user) {
    toast.warning(`Demo users cannot ${action || "perform this action"}.`);
    return true;
    }
    return false;
}
