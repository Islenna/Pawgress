// src/pages/AdminPanel.tsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import CreateCategory from "@/components/category/CreateCategory"
import CreateSkill from "@/components/skill/CreateSkill"

const AdminPanel = () => {
    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            <h1 className="text-3xl font-bold">Admin Panel</h1>

            <Tabs defaultValue="categories" className="w-full">
                <TabsList>
                    <TabsTrigger value="categories">Categories</TabsTrigger>
                    <TabsTrigger value="skills">Skills</TabsTrigger>
                </TabsList>

                <TabsContent value="categories" className="space-y-4">
                    <CreateCategory />
                    {/* CategoryTable will go here */}
                </TabsContent>

                <TabsContent value="skills" className="space-y-4">
                    <CreateSkill />
                    {/* SkillTable will go here */}
                </TabsContent>
            </Tabs>
        </div>
    )
}

export default AdminPanel
