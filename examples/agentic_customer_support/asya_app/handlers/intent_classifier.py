"""Intent classification handler - classifies ticket intent and urgency."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class IntentClassifier:
    """Classifies customer support ticket intent and urgency."""

    def __init__(self, model_path: str = None):
        """
        Initialize the intent classifier.

        Args:
            model_path: Optional path to a classification model
        """
        # In a real implementation, you would load a model here
        # For MVP, we'll use simple rule-based classification
        self.model_path = model_path
        logger.info(f"IntentClassifier initialized (model_path={model_path})")

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify ticket intent and urgency.

        Args:
            payload: Ticket payload from previous stage

        Returns:
            Payload enriched with intent and urgency classifications
        """
        if payload.get('validation_status') != 'valid':
            logger.warning(f"Skipping classification for invalid ticket: {payload.get('ticket_id')}")
            return payload

        ticket_id = payload.get('ticket_id')
        message = payload.get('message', '').lower()

        logger.info(f"Classifying intent for ticket: {ticket_id}")

        # Simple rule-based classification (replace with ML model in production)
        intent = self._classify_intent(message)
        urgency = self._classify_urgency(message)

        payload['intent'] = intent
        payload['urgency'] = urgency
        payload['classification_confidence'] = 0.85  # Placeholder

        logger.info(f"Ticket {ticket_id} classified: intent={intent}, urgency={urgency}")
        return payload

    def _classify_intent(self, message: str) -> str:
        """Classify intent using simple keyword matching."""
        # Simple keyword-based classification
        if any(word in message for word in ['refund', 'return', 'money back']):
            return 'refund'
        elif any(word in message for word in ['broken', 'not working', 'error', 'bug']):
            return 'technical_issue'
        elif any(word in message for word in ['cancel', 'stop', 'unsubscribe']):
            return 'cancellation'
        elif any(word in message for word in ['how', 'what', 'where', 'when', 'why']):
            return 'question'
        else:
            return 'general'

    def _classify_urgency(self, message: str) -> str:
        """Classify urgency level."""
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        if any(word in message for word in urgent_keywords):
            return 'high'
        elif any(word in message for word in ['soon', 'quickly', 'fast']):
            return 'medium'
        else:
            return 'low'
