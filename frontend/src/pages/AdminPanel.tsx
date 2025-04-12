// src/pages/AdminPanel.tsx
import { useEffect, useState } from "react"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import CreateCategory from "@/components/category/CreateCategory"
import CreateSkill from "@/components/skill/CreateSkill"
import CategoryTable from "@/components/category/CategoryTable"
import SkillTable from "@/components/skill/SkillTable"
import UserProficiencyTab from "@/components/proficiencies/UserProficiencyTab"
import axiosInstance from "@/lib/axiosInstance"
import { Category, Skill } from "@/types"

const AdminPanel = () => {
    const [categories, setCategories] = useState<Category[]>([])

    const fetchData = async () => {
        const [categoriesRes, skillsRes] = await Promise.all([
            axiosInstance.get("/categories"),
            axiosInstance.get("/skills")
        ])

        const grouped = categoriesRes.data.map((cat: Category) => ({
            ...cat,
            skills: skillsRes.data.filter((skill: Skill) => skill.category_id === cat.id)
        }))

        setCategories(grouped)
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            <h1 className="text-3xl font-bold">Admin Panel</h1>

            <Tabs defaultValue="categories" className="w-full">
                <TabsList>
                    <TabsTrigger value="categories">Categories</TabsTrigger>
                    <TabsTrigger value="skills">Skills</TabsTrigger>
                    <TabsTrigger value="proficiencies">Proficiencies</TabsTrigger>
                </TabsList>

                <TabsContent value="categories" className="space-y-4">
                    <CreateCategory onSuccess={fetchData} />
                    <CategoryTable categories={categories} fetchData={fetchData} />
                </TabsContent>

                <TabsContent value="skills" className="space-y-4">
                    <CreateSkill onSuccess={fetchData} />
                    <SkillTable categories={categories} fetchData={fetchData} />
                </TabsContent>

                <TabsContent value="proficiencies" className="space-y-4">
                    <UserProficiencyTab />
                </TabsContent>
            </Tabs>
        </div>
    )
}

export default AdminPanel
