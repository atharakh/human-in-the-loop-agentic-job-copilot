from src.services.config_service import ConfigService


class DemoResumeGenerator:
    """
    Generates 12 realistic dummy European-style CVs for project demo.
    Output format: TXT files.
    """

    def __init__(self):
        ConfigService.create_required_dirs()
        self.output_dir = ConfigService.CVS_DIR

    def generate_all(self) -> list[str]:
        resumes = self._get_resume_data()
        created_files = []

        for resume in resumes:
            file_name = f"{resume['candidate_id']}_{resume['role'].replace(' ', '_')}.txt"
            file_path = self.output_dir / file_name

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(resume["content"])

            created_files.append(str(file_path))

        return created_files

    def _get_resume_data(self) -> list[dict]:
        return [
            self._resume(
                "CAND-001",
                "Aamir Khan",
                "RF Planning Engineer",
                "Bonn, Germany",
                "aamir.khan@example.com",
                "LTE, 5G NR, RF Planning, Atoll, QGIS, Coverage Planning, Capacity Planning, KPI Analysis, Drive Test Analysis, Python",
                "8 years",
                "Senior RF Planning Engineer at TelNet Solutions GmbH, Cologne. Responsible for LTE and 5G radio planning, site design, coverage prediction, parameter planning, and network modernization projects.",
                "MSc Telecommunications Engineering, University of Stuttgart",
                "English fluent, German B1"
            ),
            self._resume(
                "CAND-002",
                "Sara Müller",
                "RAN Optimization Engineer",
                "Düsseldorf, Germany",
                "sara.mueller@example.com",
                "RAN Optimization, LTE, 5G, KPI Analysis, Handover Optimization, Interference Analysis, TEMS, Actix, SQL, Excel",
                "6 years",
                "RAN Optimization Engineer at ConnectWave AG. Worked on accessibility, retainability, mobility KPIs, dropped call analysis, throughput optimization, and cluster drive test reporting.",
                "BSc Electrical Engineering, FH Aachen",
                "German native, English fluent"
            ),
            self._resume(
                "CAND-003",
                "Jonas Weber",
                "5G Performance Engineer",
                "Hamburg, Germany",
                "jonas.weber@example.com",
                "5G NR, LTE-A, Massive MIMO, KPI Monitoring, Network Performance, Python, Grafana, SQL, Automation",
                "4 years",
                "5G Performance Engineer at NorthMobile GmbH. Monitored network quality, analyzed performance counters, created dashboards, and supported 5G rollout optimization.",
                "MSc Communication Systems, TU Hamburg",
                "German native, English fluent"
            ),
            self._resume(
                "CAND-004",
                "Elena Rossi",
                "Python Developer",
                "Berlin, Germany",
                "elena.rossi@example.com",
                "Python, FastAPI, Django, REST APIs, Git, Docker, PostgreSQL, Streamlit, Unit Testing",
                "3 years",
                "Python Backend Developer at SoftCore Labs. Developed REST APIs, internal dashboards, automation scripts, and backend integrations for enterprise applications.",
                "BSc Computer Science, University of Bologna",
                "English fluent, German A2, Italian native"
            ),
            self._resume(
                "CAND-005",
                "David Schneider",
                "AI Engineer",
                "Munich, Germany",
                "david.schneider@example.com",
                "Python, LangChain, LangGraph, OpenAI API, RAG, Vector Databases, Prompt Engineering, Machine Learning, Docker",
                "4 years",
                "AI Engineer at Applied Intelligence GmbH. Built LLM-based assistants, RAG pipelines, document processing workflows, and automation tools for business teams.",
                "MSc Artificial Intelligence, TU Munich",
                "German native, English fluent"
            ),
            self._resume(
                "CAND-006",
                "Nadia Becker",
                "Data Analyst",
                "Frankfurt, Germany",
                "nadia.becker@example.com",
                "SQL, Power BI, Excel, Python, Pandas, Data Visualization, Reporting, KPI Dashboards",
                "2 years",
                "Junior Data Analyst at FinanceData GmbH. Created business dashboards, cleaned datasets, prepared KPI reports, and supported management reporting.",
                "BSc Business Analytics, Frankfurt University of Applied Sciences",
                "German fluent, English fluent"
            ),
            self._resume(
                "CAND-007",
                "Markus Stein",
                "DevOps Engineer",
                "Cologne, Germany",
                "markus.stein@example.com",
                "Docker, Kubernetes, CI/CD, GitLab, Linux, Terraform, AWS, Monitoring, Python Scripting",
                "7 years",
                "Senior DevOps Engineer at CloudOps GmbH. Managed CI/CD pipelines, Kubernetes clusters, cloud infrastructure, and deployment automation.",
                "BSc Information Technology, University of Cologne",
                "German native, English fluent"
            ),
            self._resume(
                "CAND-008",
                "Fatima Ali",
                "Cloud Engineer",
                "Bonn, Germany",
                "fatima.ali@example.com",
                "AWS, Azure, Cloud Migration, Terraform, Docker, Linux, Networking, Security Basics, Monitoring",
                "5 years",
                "Cloud Engineer at RheinCloud Services. Supported cloud migration projects, managed infrastructure as code, and improved cloud security and monitoring.",
                "MSc Information Systems, University of Bonn",
                "English fluent, German B1"
            ),
            self._resume(
                "CAND-009",
                "Thomas Fischer",
                "Project Manager",
                "Dortmund, Germany",
                "thomas.fischer@example.com",
                "Project Management, Agile, Scrum, Stakeholder Management, Risk Management, Budget Tracking, Jira, Confluence",
                "9 years",
                "Project Manager at IndustrialTech GmbH. Led cross-functional IT and telecom projects, managed timelines, budgets, risks, and stakeholder communication.",
                "MBA Project Management, Cologne Business School",
                "German native, English fluent"
            ),
            self._resume(
                "CAND-010",
                "Laura Schmidt",
                "Business Analyst",
                "Essen, Germany",
                "laura.schmidt@example.com",
                "Requirements Engineering, BPMN, Process Mapping, Stakeholder Interviews, Jira, Confluence, Excel, SQL Basics",
                "5 years",
                "Business Analyst at ProcessWorks GmbH. Gathered requirements, modeled business processes, supported digital transformation projects, and prepared user stories.",
                "MSc Business Information Systems, University of Duisburg-Essen",
                "German native, English fluent"
            ),
            self._resume(
                "CAND-011",
                "Mariam Yilmaz",
                "HR Specialist",
                "Bremen, Germany",
                "mariam.yilmaz@example.com",
                "Recruitment, Employee Onboarding, HR Administration, Interview Coordination, German Labor Law Basics, MS Office, HRIS",
                "6 years",
                "HR Specialist at PeopleFirst GmbH. Managed recruitment coordination, onboarding, employee records, and HR process documentation.",
                "BA Human Resource Management, Hochschule Bremen",
                "German fluent, English fluent, Turkish native"
            ),
            self._resume(
                "CAND-012",
                "Oliver Neumann",
                "Recruiter",
                "Stuttgart, Germany",
                "oliver.neumann@example.com",
                "Talent Acquisition, CV Screening, LinkedIn Recruiting, Interview Scheduling, Candidate Communication, ATS, Employer Branding",
                "4 years",
                "Technical Recruiter at TalentBridge GmbH. Recruited IT and engineering candidates, screened CVs, coordinated interviews, and maintained ATS records.",
                "BA Business Administration, University of Stuttgart",
                "German native, English fluent"
            ),
        ]

    def _resume(
        self,
        candidate_id: str,
        name: str,
        role: str,
        location: str,
        email: str,
        skills: str,
        experience: str,
        work_experience: str,
        education: str,
        languages: str,
    ) -> dict:
        content = f"""
Candidate ID: {candidate_id}

{name}
{role}
Location: {location}
Email: {email}

Professional Summary
Experienced {role} with {experience} of professional experience. Strong background in technical analysis, stakeholder communication, structured reporting, and practical problem solving. Looking for a challenging role in Germany or remote within Europe.

Core Skills
{skills}

Professional Experience
{work_experience}

Education
{education}

Certifications
Relevant professional trainings and internal company certifications related to the target role.

Languages
{languages}

Additional Information
Available for hybrid or remote work. Open to international and multicultural teams.
""".strip()

        return {
            "candidate_id": candidate_id,
            "role": role,
            "content": content,
        }
    
    