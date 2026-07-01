from src.llm import LLMManager
from src.services.logger_service import LoggerService
from src.services.vector_store_service import VectorStoreService


class HumanInteractionAgent:
    def __init__(self):
        self.logger = LoggerService.get_logger("HumanInteractionAgent")
        self.llm = LLMManager()
        self.vector_store = VectorStoreService()

    def _active_llm_provider(self) -> str:
        try:
            return self.llm.get_status().get("active_provider", "openai")
        except Exception:
            return "openai"

    def _is_ollama(self) -> bool:
        return self._active_llm_provider() == "ollama"

    def _truncate_text(self, text: str, max_chars: int = 2500) -> str:
        if not text:
            return ""
        return text[:max_chars] + "\n\n[Text shortened.]" if len(text) > max_chars else text

    def _build_context(self, rag_results: list, max_chars_per_item: int = 1200) -> str:
        parts = []
        for item in rag_results:
            parts.append(
                f"Document ID: {item.get('document_id')}\n"
                f"Metadata: {item.get('metadata')}\n"
                f"Text: {self._truncate_text(item.get('text', ''), max_chars_per_item)}"
            )
        return "\n\n".join(parts)

    def _generate(self, prompt: str) -> str:
        return self.llm.generate(prompt)

    def _is_error_response(self, text: str) -> bool:
        markers = [
            "Ollama HTTP error",
            "Ollama took too long",
            "Could not connect to Ollama",
            "Unexpected Ollama error",
            "Ollama is not available",
        ]
        return any(marker in str(text) for marker in markers)

    def record_decision(self, decision: str, notes: str = "") -> dict:
        decision = decision.lower()
        if decision not in ["approve", "reject", "pending"]:
            raise ValueError("Decision must be approve, reject, or pending.")
        return {"decision": decision, "notes": notes}

    def answer_question(self, question: str) -> dict:
        top_k = 2 if self._is_ollama() else 5
        rag_results = self.vector_store.search(question, top_k=top_k)

        context = self._build_context(
            rag_results,
            max_chars_per_item=700 if self._is_ollama() else 1500,
        )

        prompt = f"""
Answer the user's question using only the context.

Question:
{question}

Context:
{context}

If the context is insufficient, say so clearly.
"""

        answer = self._generate(prompt)

        return {
            "question": question,
            "answer": answer,
            "rag_results": rag_results,
        }

    def suggest_next_action(self, question: str, answer: str) -> str:
        if self._is_error_response(answer):
            return "Use OpenAI or reduce prompt/context size before trying Ollama again."

        if self._is_ollama():
            return "Ask a more specific follow-up question or switch to OpenAI for deeper reasoning."

        prompt = f"""
Suggest one practical next action.

Question:
{question}

Answer:
{answer}

Return one short sentence only.
"""
        return self._generate(prompt)

    def explain_match_result(self, match_result: dict) -> str:
        prompt = f"""
Explain this candidate-job match result.

Match Result:
{match_result}

Include:
- Why the score was given
- Strengths
- Weaknesses
- Missing skills
- Human recommendation
"""
        return self._generate(prompt)

    def provide_career_coaching(self, user_goal: str) -> dict:
        top_k = 2 if self._is_ollama() else 5
        rag_results = self.vector_store.search(user_goal, top_k=top_k)

        context = self._build_context(
            rag_results,
            max_chars_per_item=700 if self._is_ollama() else 1500,
        )

        prompt = f"""
You are an AI Career Coach.

Do not rank stored candidates.
Use context only as background.

Career Goal:
{user_goal}

Context:
{context}

Provide:
1. Current starting point
2. Target role direction
3. Useful existing skills
4. Missing skills
5. Tools to learn
6. Certifications
7. Portfolio project ideas
8. CV improvements
9. 30-60-90 day roadmap
10. Practical next steps
"""
        advice = self._generate(prompt)

        return {
            "user_goal": user_goal,
            "career_advice": advice,
            "rag_results": rag_results,
        }

    def improve_resume_advice(self, resume_goal: str) -> dict:
        top_k = 2 if self._is_ollama() else 5
        rag_results = self.vector_store.search(resume_goal, top_k=top_k)

        context = self._build_context(
            rag_results,
            max_chars_per_item=700 if self._is_ollama() else 1500,
        )

        prompt = f"""
Give resume improvement advice.

Goal:
{resume_goal}

Context:
{context}

Cover:
- CV summary
- skills
- experience
- missing keywords
- ATS improvements
- role alignment
"""
        advice = self._generate(prompt)

        return {
            "resume_goal": resume_goal,
            "resume_advice": advice,
            "rag_results": rag_results,
        }

    def review_uploaded_resume(self, resume_text: str, target_goal: str = "") -> dict:
        resume_text = self._truncate_text(
            resume_text,
            max_chars=3500 if self._is_ollama() else 9000,
        )

        prompt = f"""
Review this resume for the target goal.

Target Goal:
{target_goal or "Not specified"}

Resume:
{resume_text}

Provide:
1. Overall assessment
2. Strong areas
3. Weak areas
4. Missing keywords
5. ATS improvements
6. Section-by-section feedback
7. Priority improvements
8. Final recommendation
"""
        feedback = self._generate(prompt)

        return {
            "target_goal": target_goal,
            "resume_feedback": feedback,
        }

    def recruiter_search_advice(self, recruiter_query: str) -> dict:
        top_k = 3 if self._is_ollama() else 8
        rag_results = self.vector_store.search(recruiter_query, top_k=top_k)

        context = self._build_context(
            rag_results,
            max_chars_per_item=700 if self._is_ollama() else 1500,
        )

        prompt = f"""
You are an AI Recruiter Assistant.

Recruiter Query:
{recruiter_query}

Context:
{context}

Provide:
1. Relevant candidates
2. Why they are relevant
3. Risks
4. Missing information
5. Interview focus areas
6. Shortlisting recommendation
"""
        advice = self._generate(prompt)

        return {
            "recruiter_query": recruiter_query,
            "recruiter_advice": advice,
            "rag_results": rag_results,
        }

    def compare_candidates_for_role(
        self,
        candidate_a: str,
        candidate_b: str,
        target_role: str,
        human_feedback: str = "",
    ) -> dict:
        query = f"{candidate_a} {candidate_b} {target_role}"
        top_k = 3 if self._is_ollama() else 8
        rag_results = self.vector_store.search(query, top_k=top_k)

        context = self._build_context(
            rag_results,
            max_chars_per_item=700 if self._is_ollama() else 1500,
        )

        prompt = f"""
Compare two stored candidates for a target role.

Candidate A:
{candidate_a}

Candidate B:
{candidate_b}

Target Role:
{target_role}

Human Feedback:
{human_feedback or "No human feedback provided."}

Context:
{context}

Provide:
1. Candidate A strengths and weaknesses
2. Candidate B strengths and weaknesses
3. Role fit comparison
4. AI recommendation
5. Human feedback impact
6. AI vs human agreement
7. AI vs human disagreement
8. Final balanced recommendation
9. Interview focus areas
"""
        comparison = self._generate(prompt)

        return {
            "candidate_a": candidate_a,
            "candidate_b": candidate_b,
            "target_role": target_role,
            "human_feedback": human_feedback,
            "comparison": comparison,
            "rag_results": rag_results,
        }

    def compare_uploaded_resumes_for_role(
        self,
        resume_a_text: str,
        resume_b_text: str,
        target_role: str,
        human_feedback: str = "",
    ) -> dict:
        resume_a_text = self._truncate_text(
            resume_a_text,
            max_chars=3000 if self._is_ollama() else 8000,
        )
        resume_b_text = self._truncate_text(
            resume_b_text,
            max_chars=3000 if self._is_ollama() else 8000,
        )

        prompt = f"""
Compare two uploaded resumes for a target role.

Target Role:
{target_role}

Human Feedback:
{human_feedback or "No human feedback provided."}

Candidate A Resume:
{resume_a_text}

Candidate B Resume:
{resume_b_text}

Provide:
1. Candidate A strengths and weaknesses
2. Candidate B strengths and weaknesses
3. Role fit comparison
4. Human feedback impact
5. AI vs human agreement
6. AI vs human disagreement
7. Final balanced recommendation
8. Hiring risk assessment
9. Interview focus areas
10. Suggested next step
"""
        comparison = self._generate(prompt)

        return {
            "target_role": target_role,
            "human_feedback": human_feedback,
            "comparison": comparison,
        }

    def structured_recruiter_evaluation(
        self,
        ai_recommendation: str,
        preferred_candidate: str,
        confidence: int,
        human_reasons: list[str],
        human_notes: str,
    ) -> dict:
        prompt = f"""
You are a Human-in-the-Loop Recruiter Decision Assistant.

AI Recommendation:
{ai_recommendation}

Human Preferred Candidate:
{preferred_candidate}

Human Confidence:
{confidence}/5

Human Reasons:
{human_reasons}

Human Notes:
{human_notes}

Provide:
1. Summary of AI recommendation
2. Summary of human judgment
3. Where AI and human agree
4. Where AI and human differ
5. Risks of following AI only
6. Risks of following human only
7. Final consensus recommendation
8. Next hiring action
"""
        result = self._generate(prompt)

        return {
            "preferred_candidate": preferred_candidate,
            "confidence": confidence,
            "human_reasons": human_reasons,
            "human_notes": human_notes,
            "evaluation": result,
        }

    def generate_learning_hub_plan(
        self,
        target_role: str,
        current_background: str,
        weekly_hours: int,
    ) -> dict:
        prompt = f"""
You are an AI Learning Hub advisor.

Target Role:
{target_role}

Current Background:
{current_background}

Available Learning Time:
{weekly_hours} hours per week

Create a practical learning plan with:
1. Skill gap analysis
2. Core skills to learn
3. Tools/platforms to practice
4. Certifications
5. Project ideas
6. 30-day plan
7. 60-day plan
8. 90-day plan
9. Portfolio recommendations
10. Interview preparation topics
"""
        plan = self._generate(prompt)

        return {
            "target_role": target_role,
            "current_background": current_background,
            "weekly_hours": weekly_hours,
            "learning_plan": plan,
        }

        
        