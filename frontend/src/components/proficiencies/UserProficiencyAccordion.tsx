import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"
import { Card, CardContent } from "@/components/ui/card"
import { Category } from "@/types"
import { ProficiencySelector } from "@/components/proficiencies/ProficiencySelector"
import { useAuth } from "@/lib/authContext"

type UserProficiencyAccordionProps = {
    categories: Category[]
    userProficiencies: Record<number, number> // skill_id -> proficiency
    onProficiencyChange?: (skillId: number, level: number) => void
    editable?: boolean
}

const UserProficiencyAccordion = ({
    categories,
    userProficiencies,
    onProficiencyChange,
    editable = false,
}: UserProficiencyAccordionProps) => {
    const { user } = useAuth()

    return (
        <Accordion type="multiple">
            {categories.map((category) => (
                <AccordionItem key={category.id} value={`cat-${category.id}`}>
                    <AccordionTrigger>{category.name}</AccordionTrigger>
                    <AccordionContent>
                        <Card>
                            <CardContent className="space-y-4 p-4">
                                {category.skills.length > 0 ? (
                                    category.skills.map((skill) => {
                                        const current = userProficiencies[skill.id] || 0

                                        return (
                                            <div key={skill.id}>
                                                <div className="flex justify-between items-center">
                                                    <div>
                                                        <p className="font-medium">{skill.name}</p>
                                                        <p className="text-sm text-muted-foreground">{skill.description}</p>
                                                    </div>

                                                    <div className="min-w-[200px]">
                                                        <ProficiencySelector
                                                            value={current}
                                                            onChange={(level) =>
                                                                onProficiencyChange?.(skill.id, level)
                                                            }
                                                            editable={editable}
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    })
                                ) : (
                                    <p className="text-muted-foreground">No skills in this category.</p>
                                )}
                            </CardContent>
                        </Card>
                    </AccordionContent>
                </AccordionItem>
            ))}
        </Accordion>
    )
}

export default UserProficiencyAccordion
