// src/components/shoutout/ShoutoutFeed.tsx

import { Shoutout } from "@/types"
import { Card, CardDescription } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

const ShoutoutFeed = ({ shoutouts }: { shoutouts: Shoutout[] }) => {
    if (shoutouts.length === 0) {
        return <p className="text-muted-foreground text-center">No shoutouts yet. Be the first to spread the love!</p>
    }



    return (
        <div className="space-y-4">
            <h2 className="text-xl font-semibold">Shoutouts 🎉</h2>
            <Separator />
            {shoutouts.map((s) => {
                return (
                    <Card key={s.id} className="w-full max-w-sm mx-auto bg-muted">
                        <CardDescription>
                            <span className="font-semibold">{s.sender_first_name || "Someone"}</span>
                            {s.recipient_first_name ? (
                                <> gave a shoutout to <span className="font-semibold">{s.recipient_first_name}</span>:</>
                            ) : (
                                <> says:</>
                            )}
                            <br />
                            <span className="italic text-muted-foreground">"{s.message}"</span>
                        </CardDescription>
                        <p className="text-xs text-muted-foreground mt-2">
                            {new Date(s.created_at).toLocaleString(undefined, {
                                timeZoneName: "short",
                                hour: "2-digit",
                                minute: "2-digit",
                                year: "numeric",
                                month: "short",
                                day: "numeric",
                            })}
                        </p>


                    </Card>
                )
            })}
        </div >
    )
}

export default ShoutoutFeed
