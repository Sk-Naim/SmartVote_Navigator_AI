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
        if re.search(r"\b1[0-7]\b|under 18|too young", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="If you are under 18, you cannot vote yet. However, many states allow pre-registration at 16 or 17! You can also get involved by volunteering.",
                triggered_action="underage_info"
            )

        # 2. Registration Guide
        if re.search(r"not registered|how to register|unregistered", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="You must register to vote! You can typically register online, by mail, or in-person at the DMV depending on your location. Would you like a link to official registration forms?",
                triggered_action="registration_guide"
            )

        # 3. Already Registered
        if re.search(r"already registered|i am registered", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="Great! Since you are registered, the next step is researching your candidates or finding your polling location. What would you like to do?",
                triggered_action="step_3_research"
            )

        # 4. Location Query
        if re.search(r"where (do|can) i vote|polling|location|station|pin code", query_lower):
            # Extract possible zip/pin code using regex (5 or 6 digits for US/India)
            zip_match = re.search(r"\b\d{5,6}\b", query)
            extracted_zip = zip_match.group(0) if zip_match else "00000"
            return ChatResponse(
                session_id=session_id,
                reply=f"To find your polling booth, I can check our Google Maps integration. Would you like me to look up locations for ZIP {extracted_zip}?",
                triggered_action="trigger_maps",
                action_data={"zip_code": extracted_zip}
            )

        # 5. Reminder Request
        if re.search(r"remind|calendar|add to calendar|forget", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="I can add an election reminder directly to your Google Calendar. Should I generate the link?",
                triggered_action="trigger_calendar"
            )
            
        # 6. Safety / Neutrality Check
        if re.search(r"who to vote for|democrat|republican|which party|trump|biden", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="As an educational assistant, I remain strictly neutral and do not endorse any political party or candidate.",
                triggered_action="neutrality_enforced"
            )

        # 7. Confused User
        if re.search(r"confused|help|lost", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="It's perfectly normal to be overwhelmed! Let's simplify: 1. Ensure you are eligible. 2. Register to vote. 3. Find your polling location. Where should we start?",
                triggered_action="help_menu"
            )

        # 7.5. Voting Method (Mail-in vs In-Person)
        if re.search(r"voting method|mail(-| )in|absentee|in(-| )person", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="You typically have two main voting methods: In-person at a local polling station, or via Mail-in/Absentee ballot. Mail-in requires requesting a ballot in advance. Which do you prefer?",
                triggered_action="voting_method"
            )

        # 8. New Voter / Generic Start
        if re.search(r"hi|hello|start|new voter", query_lower):
            return ChatResponse(
                session_id=session_id,
                reply="Welcome to SmartVote Navigator! Are you a new voter? Let's start with checking your eligibility. Are you an 18+ citizen?",
                triggered_action="start_flow"
            )

        # Fallback (Simulated Vertex AI Smart Response)
        return ChatResponse(
            session_id=session_id,
            reply="I'm here to help you navigate the voting process. Could you clarify if you need help with Registration, Polling Locations, or Eligibility?",
            triggered_action="fallback"
        )

decision_engine = DecisionEngine()
