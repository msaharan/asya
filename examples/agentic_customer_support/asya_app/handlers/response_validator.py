"""Response validation handler - validates response quality using LLM judge."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ResponseValidator:
    """Validates generated responses using LLM judge."""

    def __init__(self, judge_model_path: str = None, threshold: float = 0.7):
        """
        Initialize the response validator.

        Args:
            judge_model_path: Optional path to judge LLM model
            threshold: Minimum quality score threshold (0-1)
        """
        self.judge_model_path = judge_model_path
        self.threshold = float(threshold)
        logger.info(f"ResponseValidator initialized (threshold={threshold})")

    def process(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate response quality and potentially modify route.

        This handler uses envelope mode for dynamic routing.

        Args:
            envelope: Asya envelope containing payload and route

        Returns:
            Envelope with validation results and potentially modified route
        """
        payload = envelope.get('payload', {})
        route = envelope.get('route', {})

        if payload.get('validation_status') != 'valid':
            return envelope

        ticket_id = payload.get('ticket_id')
        generated_response = payload.get('generated_response', '')
        original_message = payload.get('message', '')

        logger.info(f"Validating response for ticket: {ticket_id}")

        # Judge response quality
        score = self._judge_response(original_message, generated_response)

        payload['judge_score'] = score
        payload['validation_passed'] = score >= self.threshold

        if score < self.threshold:
            logger.warning(
                "Response for ticket %s scored %.2f < %.2f; mark for refinement",
                ticket_id,
                score,
                self.threshold,
            )
            payload['needs_refinement'] = True
        else:
            logger.info(f"Response for ticket {ticket_id} passed validation with score {score:.2f}")

        # Advance route
        route['current'] = route.get('current', 0) + 1

        return envelope

    def _judge_response(self, original_message: str, response: str) -> float:
        """
        Judge response quality using LLM.

        Returns a score between 0 and 1.
        """
        # Mock implementation - in production, use actual LLM judge
        # Simple heuristic: check if response is not empty and has reasonable length
        if not response or len(response.strip()) < 10:
            return 0.3

        # Check if response addresses the original message
        if len(response) < 50:
            return 0.5

        # Check for key phrases that indicate good response
        good_phrases = ['thank you', 'help', 'assist', 'understand', 'provide']
        has_good_phrases = any(phrase in response.lower() for phrase in good_phrases)

        if has_good_phrases and len(response) > 100:
            return 0.85
        elif has_good_phrases:
            return 0.75
        else:
            return 0.65
