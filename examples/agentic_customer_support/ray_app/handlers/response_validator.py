"""Response validation handler for Ray Serve."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ResponseValidator:
    """Validates generated responses using LLM judge."""

    def __init__(self, threshold: float = 0.7):
        """
        Initialize the response validator.

        Args:
            threshold: Minimum quality score threshold (0-1)
        """
        self.threshold = float(threshold)
        logger.info(f"ResponseValidator initialized (threshold={threshold})")

    def validate(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate response quality.

        Args:
            ticket_data: Ticket data with generated response

        Returns:
            Ticket data enriched with validation results
        """
        ticket_id = ticket_data.get('ticket_id')
        generated_response = ticket_data.get('generated_response', '')
        original_message = ticket_data.get('message', '')

        logger.info(f"Validating response for ticket: {ticket_id}")

        score = self._judge_response(original_message, generated_response)

        ticket_data['judge_score'] = score
        ticket_data['validation_passed'] = score >= self.threshold
        ticket_data['needs_refinement'] = score < self.threshold

        if score < self.threshold:
            logger.warning(f"Response for ticket {ticket_id} scored {score:.2f} < {self.threshold}")
        else:
            logger.info(f"Response for ticket {ticket_id} passed validation with score {score:.2f}")

        return ticket_data

    def _judge_response(self, original_message: str, response: str) -> float:
        """Judge response quality (mock implementation)."""
        if not response or len(response.strip()) < 10:
            return 0.3

        if len(response) < 50:
            return 0.5

        good_phrases = ['thank you', 'help', 'assist', 'understand', 'provide']
        has_good_phrases = any(phrase in response.lower() for phrase in good_phrases)

        if has_good_phrases and len(response) > 100:
            return 0.85
        elif has_good_phrases:
            return 0.75
        else:
            return 0.65
