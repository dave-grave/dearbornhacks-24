import AcademicAdvisorChat from "./academic-advisor-chat";

export default function AdvisorPage() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold text-center mb-6">
        Academic Advisor AI
      </h1>
      <AcademicAdvisorChat />
    </div>
  );
}
