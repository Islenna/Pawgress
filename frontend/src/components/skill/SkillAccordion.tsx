import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"
import { Card, CardContent } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { Category } from "@/types"
import { Button } from "@/components/ui/button" // Needed for edit button
import { Skill } from "@/types" // Needed for skill type

const proficiencyLevels: Record<number, { label: string; description: string }> = {
    1: { label: "Awareness", description: "Knows of the skill; has not performed it." },
    2: { label: "Assisted", description: "Can perform with direct guidance." },
    3: { label: "Independent", description: "Can perform confidently without help." },
    4: { label: "Competent", description: "Trusted to handle this skill in tough scenarios." },
    5: { label: "Mentor", description: "Can teach and support others in mastering it." },
}

type SkillAccordionProps = {
    categories: Category[];
    editable?: boolean;
    onEditClick?: (skill: Skill) => void;
    onDeleteClick?: (id: number) => void;
};


const SkillAccordion = ({ categories, editable = false, onEditClick }: SkillAccordionProps) => {
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
                                        return (
                                            <div key={skill.id} className="space-y-1">
                                                <div className="flex justify-between items-center">
                                                    <p className="font-medium">{skill.name}</p>
                                                    <div className="flex items-center gap-2">
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
                                                        {editable && onEditClick && (
                                                            <Button size="sm" onClick={() => onEditClick(skill)}>Edit</Button>
                                                        )}
                                                    </div>
                                                </div>

                                                <p className="text-sm text-muted-foreground">{skill.description}</p>

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
