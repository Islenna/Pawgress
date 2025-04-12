import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"
import { Card, CardContent } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"

type Skill = {
    id: number
    name: string
    description: string
    proficiency?: number
}

type Category = {
    id: number
    name: string
    skills: Skill[]
}

const proficiencyLevels: Record<number, { label: string; description: string }> = {
    1: { label: "Awareness", description: "Knows of the skill; has not performed it." },
    2: { label: "Assisted", description: "Can perform with direct guidance." },
    3: { label: "Independent", description: "Can perform confidently without help." },
    4: { label: "Competent", description: "Trusted to handle this skill in tough scenarios." },
    5: { label: "Mentor", description: "Can teach and support others in mastering it." },
}


const SkillsPage = () => {
    const [categories, setCategories] = useState<Category[]>([])

    useEffect(() => {
        const fetchData = async () => {
            const [categoriesRes, proficienciesRes] = await Promise.all([
                axiosInstance.get("/categories"),
                axiosInstance.get("/users/mine"),
            ])

            const profMap = new Map<number, number>() // skill_id => proficiency
            proficienciesRes.data.forEach((p: any) => {
                profMap.set(p.skill.id, p.proficiency)
            })

            const merged = categoriesRes.data.map((cat: any) => ({
                ...cat,
                skills: cat.skills.map((skill: any) => ({
                    ...skill,
                    proficiency: profMap.get(skill.id) ?? 0,
                })),
            }))

            setCategories(merged)
        }

        fetchData()
    }, [])

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            <h2 className="text-2xl font-bold">Skill Categories</h2>
            <Accordion type="multiple">
                {categories.map((category) => (
                    <AccordionItem key={category.id} value={`cat-${category.id}`}>
                        <AccordionTrigger>{category.name}</AccordionTrigger>
                        <AccordionContent>
                            <Card>
                                <CardContent className="space-y-2 p-4">
                                    {category.skills.length > 0 ? (
                                        category.skills.map((skill) => {
                                            const level = proficiencyLevels[skill.proficiency ?? 0]
                                            return (
                                                <div key={skill.id}>
                                                    <div className="flex justify-between items-center">
                                                        <p className="font-medium">{skill.name}</p>
                                                        <Tooltip>
                                                            <TooltipTrigger asChild>
                                                                <span className="text-xs underline cursor-help text-muted-foreground">
                                                                    Level: {level?.label ?? "None"}
                                                                </span>
                                                            </TooltipTrigger>
                                                            <TooltipContent side="top">
                                                                {level?.description ?? "No proficiency assigned."}
                                                            </TooltipContent>
                                                        </Tooltip>
                                                    </div>
                                                    <p className="text-sm text-muted-foreground">{skill.description}</p>
                                                </div>
                                            )
                                        })
                                    ) : (
                                        <p className="text-muted-foreground">No skills assigned.</p>
                                    )}
                                </CardContent>
                            </Card>
                        </AccordionContent>
                    </AccordionItem>
                ))}
            </Accordion>
        </div>
    )
}

export default SkillsPage
