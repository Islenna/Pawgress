import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { MetricsResponse } from "@/types"
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

function AdminMetricsPage() {
    const [metrics, setMetrics] = useState<MetricsResponse | null>(null)

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await axiosInstance.get("/metrics")
                setMetrics(response.data)
            } catch (err) {
                console.error("Error fetching metrics:", err)
                setError("Failed to load metrics")
            } finally {
                setLoading(false)
            }
        }

        fetchMetrics()
    }, [])

    if (loading) return <p>Loading metrics...</p>
if (error) return <p className="text-red-500">{error}</p>
if (!metrics) return null

const categoryProficiencyData = metrics.category_breakdown.map(cat => ({
    category: cat.category,
    avg: cat.avg_proficiency
}))

const proficiencyDistribution = [1, 2, 3, 4, 5].map(level => ({
    level: `Level ${level}`,
    count: Object.values(metrics.avg_proficiency_per_skill).filter(
        (val) => Math.round(val) === level
    ).length
}))


    return (
        <div className="max-w-4xl mx-auto mt-8 p-4">
            <h1 className="text-xl font-bold mb-4">📈 Admin Metrics</h1>

            <div className="grid gap-2">
                <p><strong>Total Skills:</strong> {metrics.total_skills}</p>
                <p><strong>Total Proficiencies:</strong> {metrics.total_proficiencies}</p>
                <p><strong>Signed Off Proficiencies:</strong> {metrics.signed_off_proficiencies}</p>
                <Tabs defaultValue="overview">
                    <TabsList>
                        <TabsTrigger value="overview">Overview</TabsTrigger>
                        <TabsTrigger value="top">Top Skills</TabsTrigger>
                        <TabsTrigger value="bottom">Needs Work</TabsTrigger>
                        <TabsTrigger value="dist">Proficiency Dist</TabsTrigger>
                        <TabsTrigger value="category">By Category</TabsTrigger>
                    </TabsList>

                    <TabsContent value="overview">
                        {/* Existing overview layout here */}
                    </TabsContent>
                    <TabsContent value="top" className="min-h-[400px]">
                        <h2 className="font-semibold mb-2">Top Skills by Average Proficiency</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
                                data={Object.entries(metrics.avg_proficiency_per_skill)
                                    .map(([name, avg]) => ({
                                        name: name.length > 25 ? name.slice(0, 22) + "…" : name,
                                        avg
                                    }))

                                    .sort((a, b) => b.avg - a.avg)
                                    .slice(0, 5)} // top 5
                            >
                                <XAxis
                                    dataKey="name"
                                    interval={0}
                                    tick={({ x, y, payload }) => (
                                        <text
                                            x={x}
                                            y={y}
                                            dy={16}
                                            textAnchor="end"
                                            transform={`rotate(-35, ${x}, ${y})`}
                                            fill="white"
                                            fontSize={12}
                                        >
                                            {payload.value}
                                        </text>
                                    )}
                                />
                                <YAxis domain={[0, 5]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: "#1f1f1f", color: "#fff", borderRadius: 8 }}
                                    cursor={{ fill: "#333" }}
                                />

                                <Bar dataKey="avg" fill="#6366f1" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </TabsContent>
                    <TabsContent value="bottom">
                        <h2 className="font-semibold mb-2">Skills Needing Improvement</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart margin={{ top: 20, right: 30, left: 20, bottom: 80 }}

                                data={Object.entries(metrics.avg_proficiency_per_skill)
                                    .map(([name, avg]) => ({
                                        name: name.length > 25 ? name.slice(0, 22) + "…" : name,
                                        avg
                                    }))
                                    .sort((a, b) => a.avg - b.avg) // sort ascending
                                    .slice(0, 5) // bottom 5
                                }
                            >
                                <XAxis
                                    dataKey="name"
                                    interval={0}
                                    tick={({ x, y, payload }) => (
                                        <text
                                            x={x}
                                            y={y}
                                            dy={16}
                                            textAnchor="end"
                                            transform={`rotate(-35, ${x}, ${y})`}
                                            fill="white"
                                            fontSize={12}
                                        >
                                            {payload.value}
                                        </text>
                                    )}
                                />
                                <YAxis domain={[0, 5]} />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: "#1f1f1f",
                                        color: "#fff",
                                        borderRadius: 8
                                    }}
                                    cursor={{ fill: "#333" }}
                                />
                                <Bar dataKey="avg" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </TabsContent>
                    <TabsContent value="dist">
                        <h2 className="font-semibold mb-2">Proficiency Distribution</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
                                data={proficiencyDistribution}>
                                <XAxis dataKey="level" />
                                <YAxis allowDecimals={false} />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: "#1f1f1f",
                                        color: "#fff",
                                        borderRadius: 8
                                    }}
                                />
                                <Bar dataKey="count" fill="#10b981" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </TabsContent>
                    <TabsContent value="category">
                        <h2 className="font-semibold mb-2">Average Proficiency by Category</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
                                data={categoryProficiencyData}>
                                <XAxis
                                    dataKey="category"
                                    interval={0}
                                    tick={({ x, y, payload }) => (
                                        <text
                                            x={x}
                                            y={y}
                                            dy={16}
                                            textAnchor="end"
                                            transform={`rotate(-25, ${x}, ${y})`}
                                            fill="white"
                                            fontSize={12}
                                        >
                                            {payload.value}
                                        </text>
                                    )}
                                />
                                <YAxis domain={[0, 5]} allowDecimals={false} />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: "#1f1f1f",
                                        color: "#fff",
                                        borderRadius: 8
                                    }}
                                />
                                <Bar dataKey="avg" fill="#fbbf24" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </TabsContent>


                </Tabs>
                {/* <h2 className="mt-4 font-semibold">Average Proficiency per Skill:</h2>
                <ul className="pl-4 list-disc">
                    {Object.entries(metrics.avg_proficiency_per_skill).map(([skillName, avg]) => (
                        skillName ? (
                            <li key={skillName}>
                                <strong>{skillName}</strong>: {avg.toFixed(2)}
                            </li>
                        ) : null
                    ))}
                </ul> */}
                <Separator className="my-6" />

                <h2 className="mt-4 font-semibold">Category Breakdown:</h2>
                <Accordion type="multiple">
                    {metrics.category_breakdown.map(cat => (
                        <AccordionItem key={cat.category} value={cat.category}>
                            <AccordionTrigger>{cat.category}</AccordionTrigger>
                            <AccordionContent>
                                <p>Total Skills: {cat.total}</p>
                                <p>Signed Off: {cat.signed_off}</p>
                                <p>Avg Proficiency: {cat.avg_proficiency.toFixed(2)}</p>
                            </AccordionContent>
                        </AccordionItem>
                    ))}
                </Accordion>

            </div>
        </div>
    )
}

export default AdminMetricsPage
