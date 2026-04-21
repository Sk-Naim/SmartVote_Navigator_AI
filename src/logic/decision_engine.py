import re
from typing import Tuple, Optional, Dict, Any
from src.models.schemas import ChatResponse

class DecisionEngine:
    def process_query(self, session_id: str, query: str) -> ChatResponse:
        """
        Rule-based intent router ensuring neutral, accurate, and 
        structured navigation through the election process.
        Returns a ChatResponse which may contain trigger tags for frontend/API downstream logic.
        """
        query_lower = query.lower()

        # 1. Underage Check
        if re.search(r"\b(1[0-7]|under 18|too young|minor|child)\b", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="If you are under 18, you cannot vote yet. However, many states and regions allow pre-registration at 16 or 17! You can also get involved by volunteering to help polling workers.",
                triggered_action="underage_info"
            )

        # 2. Registration Guide
        if re.search(r"(how (to|can i) register|not registered|unregistered|registration process|voter card)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="You must be registered to vote! Most places allow you to register online, by mail, or in-person at a government office. Would you like a guide on the specific registration steps for your area?",
                triggered_action="registration_guide"
            )

        # 3. Already Registered
        if re.search(r"(already registered|i am (a )?registered|i've registered)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="Excellend! Since you are already registered, you are ready for the next steps: researching candidates and finding your polling location. Which should we look into first?",
                triggered_action="step_3_research"
            )

        # 4. Location Query
        if re.search(r"(where (do|can) i vote|polling|location|station|pin code|zip code|booth)", query_lower):
            # Extract possible zip/pin code using regex (5 or 6 digits)
            zip_match = re.search(r"\b\d{5,6}\b", query)
            extracted_zip = zip_match.group(0) if zip_match else "unknown"
            
            if extracted_zip == "unknown":
                return ChatResponse(
                    session_id=session_id,
                    reply="I'd be happy to find your polling location! Could you please provide your 5 or 6 digit ZIP/PIN code?",
                    triggered_action="request_zip"
                )
            
            return ChatResponse(
                session_id=session_id,
                reply=f"To find your nearest polling booth, I've checked our database for code {extracted_zip}. Here is the closest station I found!",
                triggered_action="trigger_maps",
                action_data={"zip_code": extracted_zip}
            )

        # 5. Reminder Request
        if re.search(r"(remind|calendar|add to calendar|forget|reminder|alert)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="Consistency is key! I can add an election reminder directly to your Google Calendar so you don't miss the date. Click the link below to set it up!",
                triggered_action="trigger_calendar"
            )
            
        # 6. Safety / Neutrality Check
        if re.search(r"(who (to|should i) vote for|democrat|republican|which party|trump|biden|modi|rahul|candidate recommendation)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="As an educational assistant, I remain strictly neutral. I cannot endorse any political party or candidate. My goal is to help you understand *how* to vote, while *who* to vote for is entirely your personal decision.",
                triggered_action="neutrality_enforced"
            )

        # 7. Confused User
        if re.search(r"(confused|help|lost|what do i do|guide me)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="No worries, I'm here to simplify the process. There are 3 main steps: 1. Eligibility, 2. Registration, 3. Voting. Which one would you like to explore right now?",
                triggered_action="help_menu"
            )

        # 7.5. Voting Method (Mail-in vs In-Person)
        if re.search(r"(voting method|how (do|can) i cast my vote|mail(-| )in|absentee|in(-| )person|ways to vote)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="There are two main ways to vote: In-person at your local polling station, or via Mail-in (Absentee) ballot. Mail-in voting usually requires a prior request. Which method would you like more details on?",
                triggered_action="voting_method"
            )

        # 8. New Voter / Generic Start
        if re.search(r"(hi|hello|start|new voter|hey|greetings)", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="Welcome to SmartVote Navigator AI! I'm your assistant for a smooth voting experience. Are you a new voter looking for a guide, or do you have a specific question?",
                triggered_action="start_flow"
            )

        # Fallback (Simulated Vertex AI Smart Response)
        return ChatResponse(
            session_id=session_id,
            reply="I'm here to help you navigate the voting process perfectly. You can ask me about Registration, Eligibility, finding your Polling Station (provide a PIN/ZIP), or Setting Reminders. What can I do for you?",
            triggered_action="fallback"
        )

decision_engine = DecisionEngine()
