import re


class AIService:
    KNOWN_SKILLS = {
        "python",
        "java",
        "javascript",
        "typescript",
        "angular",
        "react",
        "node",
        "fastapi",
        "django",
        "sql",
        "postgresql",
        "mysql",
        "aws",
        "docker",
        "kubernetes",
        "git",
        "html",
        "css",
    }

    def parse_resume(self, text: str) -> dict:
        lowered = text.lower()
        skills = sorted([skill for skill in self.KNOWN_SKILLS if re.search(rf"\b{re.escape(skill)}\b", lowered)])
        experience_years = self._extract_experience_years(lowered)
        education = self._extract_education(text)
        return {
            "skills": skills,
            "experience_years": experience_years,
            "education": education,
        }

    def generate_candidate_summary(self, candidate_name: str, skills: list[str], experience_years: float, education: str | None) -> str:
        top_skills = ", ".join(skills[:6]) if skills else "general software development"
        edu = education or "education details not clearly listed"
        lines = [
            f"{candidate_name} appears to be a strong candidate for technical roles.",
            f"Key skill areas include {top_skills}.",
            f"Estimated hands-on experience is around {experience_years:.1f} years.",
            "Profile indicates practical exposure to real-world project delivery.",
            f"Education background: {edu}.",
            "Candidate may be a good fit for teams needing quick onboarding.",
        ]
        return " ".join(lines)

    def improve_job_description(self, title: str, department: str, description: str, skills: list[str], experience_required: float) -> str:
        skills_line = ", ".join(skills)
        return (
            f"We are hiring a {title} for the {department} team. "
            f"The role requires approximately {experience_required:.1f}+ years of relevant experience. "
            f"Core technical skills: {skills_line}. "
            "The selected candidate will collaborate across teams, build reliable solutions, "
            "and contribute to continuous improvement in delivery quality. "
            f"Role context: {description}"
        )

    def generate_match_explanation(
        self,
        candidate_name: str,
        job_title: str,
        matching_skills: list[str],
        missing_skills: list[str],
        experience_match_pct: float,
    ) -> str:
        matched = ", ".join(matching_skills) if matching_skills else "no direct skill overlap yet"
        missing = ", ".join(missing_skills) if missing_skills else "no major skill gaps"
        return (
            f"{candidate_name} vs {job_title}: matched skills include {matched}. "
            f"Potential gaps: {missing}. Experience alignment is {experience_match_pct:.2f}%. "
            "Overall this score reflects current fit based on available structured data."
        )

    def _extract_experience_years(self, text: str) -> float:
        years_patterns = [
            r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
            r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        ]
        for pattern in years_patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        return 0.0

    def _extract_education(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            lowered = line.lower()
            if any(x in lowered for x in ["b.tech", "bachelor", "master", "mca", "bca", "phd", "degree"]):
                return line
        return "Not specified"

