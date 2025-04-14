import { useState } from "react"
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"
import { Card, CardContent } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { Category } from "@/types"
import { Button } from "@/components/ui/button"
import { Skill } from "@/types"

const proficiencyLevels: Record<number, { label: string; description: string; color: string }> = {
    1: { label: "Awareness", description: "Knows of the skill; has not performed it.", color: "text-gray-400" },
    2: { label: "Assisted", description: "Can perform with direct guidance.", color: "text-blue-400" },
    3: { label: "Independent", description: "Can perform confidently without help.", color: "text-green-400" },
    4: { label: "Competent", description: "Trusted to handle this skill in tough scenarios.", color: "text-yellow-400" },
    5: { label: "Mentor", description: "Can teach and support others in mastering it.", color: "text-purple-400" },
}

type SkillAccordionProps = {
    categories: Category[];
    editable?: boolean;
    onEditClick?: (skill: Skill) => void;
    onDeleteClick?: (id: number) => void;
};

const SkillAccordion = ({ categories, editable = false, onEditClick }: SkillAccordionProps) => {
    const [expandedId, setExpandedId] = useState<number | null>(null)

    return (
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
                                        const isExpanded = expandedId === skill.id

                                        return (
                                            <div key={skill.id} className="space-y-1">
                                                <div className="flex justify-between items-center">
                                                    <p className="font-medium">{skill.name}</p>
                                                    <div className="flex items-center gap-2">
                                                        <Tooltip>
                                                            <TooltipTrigger asChild>
                                                                <span className={`text-xs underline cursor-help ${level?.color ?? "text-muted-foreground"}`}>
                                                                    Level: {level?.label ?? "None"}
                                                                </span>
                                                            </TooltipTrigger>
                                                            <TooltipContent side="top">
                                                                {level?.description ?? "No proficiency assigned."}
                                                            </TooltipContent>
                                                        </Tooltip>
                                                        {editable && onEditClick && (
                                                            <Button size="sm" onClick={() => onEditClick(skill)}>Edit</Button>
                                                        )}
                                                    </div>
                                                </div>

                                                {isExpanded ? (
                                                    <p className="text-sm text-muted-foreground">{skill.description}</p>
                                                ) : (
                                                    <p className="text-sm text-muted-foreground line-clamp-3">{skill.description}</p>
                                                )}

                                                {skill.description.length > 150 && (
                                                    <button
                                                        className="text-xs text-blue-500 underline"
                                                        onClick={() =>
                                                            setExpandedId(isExpanded ? null : skill.id)
                                                        }
                                                    >
                                                        {isExpanded ? "Show Less" : "Read More"}
                                                    </button>
                                                )}

                                                {skill.signed_off_by_user && (
                                                    <p className="text-xs italic text-muted-foreground">
                                                        Signed off by {skill.signed_off_by_user.first_name} {skill.signed_off_by_user.last_name}
                                                        {skill.signed_off_at && (
                                                            <> on {new Date(skill.signed_off_at).toLocaleDateString()}</>
                                                        )}
                                                    </p>
                                                )}
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
    )
}

export default SkillAccordion
