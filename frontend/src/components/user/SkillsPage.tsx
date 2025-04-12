import { useEffect, useState } from "react"
import axiosInstance from "@/lib/axiosInstance"
import SkillAccordion from '@/components/skill/SkillAccordion'
import SearchBar from "@/components/shared/SearchBar"
import { Category } from "@/types"

const SkillsPage = () => {
    const [categories, setCategories] = useState<Category[]>([])
    const [search, setSearch] = useState("")

    useEffect(() => {
        const fetchData = async () => {
            const [categoriesRes, proficienciesRes] = await Promise.all([
                axiosInstance.get("/categories"),
                axiosInstance.get("/users/mine"),
            ])

            const profMap = new Map<number, number>()
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

    // filter categories + skills by search
    const filtered = categories.map(cat => ({
        ...cat,
        skills: cat.skills.filter(skill =>
            skill.name.toLowerCase().includes(search.toLowerCase()) ||
            skill.description.toLowerCase().includes(search.toLowerCase())
        )
    })).filter(cat => cat.skills.length > 0)

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            <h2 className="text-2xl font-bold">Skill Categories</h2>
            <SearchBar value={search} onChange={setSearch} placeholder="Search your skills..." />
            {filtered.length > 0 ? (
                <SkillAccordion categories={filtered} />
            ) : (
                <p className="text-muted-foreground text-center mt-4">
                    No matching skills found.
                </p>
            )}

        </div>
    )
}

export default SkillsPage
