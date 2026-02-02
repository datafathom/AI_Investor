import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VotingService:
    """
    Phase 208.3: Family Council Voting System.
    Backend logic for Quadratic Voting on philanthropic initiatives.
    """

    def __init__(self):
        self.active_proposals = [
            {"id": 1, "topic": "Clean Water Initiative", "votes": 0},
            {"id": 2, "topic": "AI Safety Research", "votes": 0}
        ]
        self.user_credits = {"Alice": 100, "Bob": 100}

    def cast_vote(self, user: str, proposal_id: int, credits_spent: int) -> Dict[str, Any]:
        """
        Quadratic Voting: Cost = (Votes)^2.
        """
        if user not in self.user_credits:
            return {"status": "ERROR", "message": "User not found"}
            
        if self.user_credits[user] < credits_spent:
            return {"status": "ERROR", "message": "Insufficient credits"}
            
        # Calculate vote power (square root of credits spent)
        vote_power = int(credits_spent ** 0.5)
        
        logger.info(f"{user} spent {credits_spent} credits for {vote_power} votes on Prop {proposal_id}")
        
        self.user_credits[user] -= credits_spent
        
        # Update proposal (Mock logic)
        for p in self.active_proposals:
            if p["id"] == proposal_id:
                p["votes"] += vote_power
                
        return {
            "status": "VOTED",
            "votes_cast": vote_power,
            "remaining_credits": self.user_credits[user]
        }
