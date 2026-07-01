from src.services.config_service import ConfigService


class DemoJobGenerator:
    """
    Generates realistic demo job descriptions for the project.
    Output format: TXT files.
    """

    def __init__(self):
        ConfigService.create_required_dirs()
        self.output_dir = ConfigService.JOBS_DIR

    def generate_all(self) -> list[str]:
        jobs = self._get_job_data()
        created_files = []

        for job in jobs:
            file_name = f"{job['job_id']}_{job['title'].replace(' ', '_')}.txt"
            file_path = self.output_dir / file_name

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(job["content"])

            created_files.append(str(file_path))

        return created_files

    def _get_job_data(self) -> list[dict]:
        return [
            self._job(
                "JOB-001",
                "Senior RF Planning Engineer",
                "Nokia Solutions Germany GmbH",
                "Bonn, Germany",
                "LTE, 5G NR, RF Planning, Atoll, QGIS, Coverage Planning, Capacity Planning, KPI Analysis, Drive Test Analysis, Python",
                "Perform LTE and 5G RF planning, coverage analysis, capacity planning, parameter planning, site modernization support, and technical reporting."
            ),
            self._job(
                "JOB-002",
                "RAN Optimization Engineer",
                "Ericsson GmbH",
                "Düsseldorf, Germany",
                "RAN Optimization, LTE, 5G, KPI Analysis, Handover Optimization, Interference Analysis, TEMS, Actix, SQL",
                "Analyze network KPIs, optimize accessibility and retainability, investigate dropped calls, improve throughput, and prepare cluster optimization reports."
            ),
            self._job(
                "JOB-003",
                "5G Performance Engineer",
                "Vodafone Germany",
                "Düsseldorf, Germany",
                "5G NR, LTE-A, Massive MIMO, KPI Monitoring, Network Performance, Python, SQL, Grafana",
                "Monitor 5G network performance, analyze counters, create dashboards, support rollout optimization, and identify performance bottlenecks."
            ),
            self._job(
                "JOB-004",
                "Python Backend Developer",
                "SAP",
                "Walldorf, Germany",
                "Python, FastAPI, REST APIs, Git, Docker, PostgreSQL, Unit Testing",
                "Develop backend APIs, maintain services, write clean Python code, build integrations, and support scalable enterprise applications."
            ),
            self._job(
                "JOB-005",
                "AI Engineer",
                "Bosch AI Labs",
                "Stuttgart, Germany",
                "Python, LangChain, LangGraph, OpenAI API, RAG, Vector Databases, Prompt Engineering, Docker",
                "Build LLM applications, RAG pipelines, document assistants, agent workflows, and AI automation prototypes."
            ),
            self._job(
                "JOB-006",
                "Data Analyst",
                "Siemens",
                "Munich, Germany",
                "SQL, Power BI, Excel, Python, Pandas, Data Visualization, KPI Dashboards",
                "Prepare reports, build dashboards, clean datasets, analyze KPIs, and support business decision-making."
            ),
            self._job(
                "JOB-007",
                "DevOps Engineer",
                "Amazon Web Services",
                "Berlin, Germany",
                "Docker, Kubernetes, CI/CD, GitLab, Linux, Terraform, AWS, Python Scripting",
                "Manage deployment pipelines, cloud infrastructure, Kubernetes clusters, monitoring, and automation."
            ),
            self._job(
                "JOB-008",
                "Cloud Engineer",
                "Capgemini",
                "Cologne, Germany",
                "AWS, Azure, Terraform, Docker, Linux, Networking, Cloud Migration, Monitoring",
                "Support cloud migration projects, manage cloud resources, improve security, and automate infrastructure."
            ),
            self._job(
                "JOB-009",
                "Project Manager",
                "BMW Group",
                "Munich, Germany",
                "Project Management, Agile, Scrum, Stakeholder Management, Risk Management, Budget Tracking, Jira",
                "Lead cross-functional technical projects, manage timelines, budgets, risks, and stakeholder communication."
            ),
            self._job(
                "JOB-010",
                "Business Analyst",
                "Allianz Technology",
                "Frankfurt, Germany",
                "Requirements Engineering, BPMN, Process Mapping, Stakeholder Interviews, Jira, Confluence, SQL Basics",
                "Gather requirements, model business processes, create user stories, and support digital transformation initiatives."
            ),
            self._job(
                "JOB-011",
                "HR Specialist",
                "DHL Group",
                "Bonn, Germany",
                "Recruitment, Employee Onboarding, HR Administration, Interview Coordination, HRIS, MS Office",
                "Support recruitment, onboarding, employee documentation, HR process coordination, and internal communication."
            ),
            self._job(
                "JOB-012",
                "Technical Recruiter",
                "Accenture",
                "Düsseldorf, Germany",
                "Talent Acquisition, CV Screening, LinkedIn Recruiting, Interview Scheduling, ATS, Candidate Communication",
                "Recruit IT and engineering candidates, screen profiles, coordinate interviews, and maintain ATS records."
            ),
            self._job(
                "JOB-013",
                "AI Consultant",
                "IBM Consulting",
                "Hamburg, Germany",
                "AI Strategy, Python, LLMs, RAG, Prompt Engineering, Client Workshops, Cloud AI",
                "Advise clients on AI adoption, build prototypes, prepare technical workshops, and support AI transformation projects."
            ),
            self._job(
                "JOB-014",
                "Network Automation Engineer",
                "Deutsche Telekom",
                "Bonn, Germany",
                "Python, REST APIs, Network Automation, LTE, 5G, SQL, Git, Docker",
                "Automate network operations, build scripts, integrate APIs, support telecom engineering teams, and improve workflow efficiency."
            ),
            self._job(
                "JOB-015",
                "Data Engineer",
                "Mercedes-Benz Tech Innovation",
                "Stuttgart, Germany",
                "Python, SQL, ETL, Data Pipelines, Cloud, Docker, Spark, Data Modeling",
                "Build data pipelines, manage ETL workflows, support analytics platforms, and improve data quality."
            ),
        ]

    def _job(
        self,
        job_id: str,
        title: str,
        company: str,
        location: str,
        skills: str,
        responsibilities: str,
    ) -> dict:
        content = f"""
Job ID: {job_id}

Job Title: {title}
Company: {company}
Location: {location}
Employment Type: Full-Time
Work Model: Hybrid

About the Role
{company} is looking for a motivated {title} to join our professional team in Germany. The role requires strong technical skills, analytical thinking, communication skills, and the ability to work in international teams.

Key Responsibilities
{responsibilities}

Required Skills
{skills}

Preferred Skills
Python automation, documentation, stakeholder communication, agile working methods, and experience in multicultural project environments.

Qualifications
Bachelor's or Master's degree in a relevant field.
Relevant professional experience in the target role.
Strong analytical and communication skills.
Fluent English. German language skills are an advantage.

Benefits
Competitive salary, hybrid work, flexible working hours, training budget, modern office environment, and international projects.
""".strip()

        return {
            "job_id": job_id,
            "title": title,
            "content": content,
        }
    
    