# Pawgress — ToDo.md

---

## ✅ Current Features

- Full JWT-based Auth system with role-based access (user, admin, superuser)
- Clinic-scoped data separation
- CRUD for Users, Skills, Categories, Proficiencies
- Skill proficiency system with 1–5 level ranking and sign-off tracking
- User and Admin dashboards with shared SkillAccordion component
- Logging of activity (e.g., skill updates, logins)
- Tailwind + Shadcn styling framework
- Password update functionality with backend validation
- Cleaned up username → full_name transition app-wide
- Toggleable password input field (show/hide)
- User registration now enforces password length via schema validation
- Hosted at Pawgress.tech!
- Admin Metrics in place

---

## 🖥️ Frontend

- [x] Choose layout/design framework
- [x] User Dashboard (displays license info, skills, etc.)
- [x] Admin Dashboard (Categories, Skills, Proficiencies tabs)
- [x] Category & Skill Creation via modals
- [x] Display & edit user proficiencies
- [x] Upload CE certificates (file upload + display)
- [x] Show "Signed off by [Admin] on [Date]" in User view
- [x] Add color-coded levels to ProficiencySelector
- [x] Add better mobile styling for SkillAccordion
- [x] Filter/Search by category or skill in user view
- [x] Admin view/edit users
- [x] Settings/Profile page for user info and license details
- [x] Prevent users changing Superuser's role
- [x] Frontend category deletion protection
    ### Admin Metrics
    - [x] New AdminMetrics Page
    - [x] Chart components
    - [x] Display


---

## 🛠️ Backend

- [x] CRUD for all models: User, Skill, Category, Proficiency
- [x] JWT Auth with role support
- [x] Activity Logging (per-clinic visibility)
- [x] Nested response models (user → categories → skills → proficiencies)
- [x] Per-user skill tracking with sign-off metadata (who/when)
- [x] Duplicate protections on skill/category creation
- [x] File upload endpoint for CE docs
- [x] Endpoint to view CE upload history per user
- [x] Better UX for finding users to assign proficiencies.
- [ ] Endpoint for CSV export of skill data per clinic or user
- [ ] Onboarding seeder for demo mode (create dummy users/data)

    ### Admin Metrics
    - [x] New route
    - [x] Number of signed-off proficiencies
    - [x] Avg proficiency per skill
    - [x] Breakdown per category

---

## 🧪 Testing

- [x] Core CRUD tests (skills, categories, proficiencies)
- [x] Test for auth-required routes (admin vs user)
- [x] File upload tests (accepts valid formats, rejects large/invalid files)
- [x] Export tests (CSV, CE data)

---

## 💡 Future Ideas

- [x] CE credit / expenditure tracker (add CE, track hours)
- [ ] Certification expiration tracker (e.g. license renewal)
- [ ] User metric views
- [ ] Add clinics, and then users to clinics.
- [ ] Email reminders for expiring licenses or missing CE
- [x] Shoutout/Recognition box (e.g. “Shoutout to Jen for 10 IV catheters today!”)
- [x] Demo mode for new clinics to try out features
- [x] Admin metrics dashboard (charts: % signed off, avg proficiency per skill)

---

## 📊 Proficiency Levels

| Level | Label        | Description                                           |
|-------|--------------|-------------------------------------------------------|
| 1     | Awareness    | Knows of the skill; has not performed it             |
| 2     | Assisted     | Can perform with direct guidance                     |
| 3     | Independent  | Can perform confidently without help                 |
| 4     | Competent    | Trusted to handle this skill in tough scenarios      |
| 5     | Mentor       | Can teach and support others in mastering it         |