"""Intent classification handler for Ray Serve."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class IntentClassifier:
    """Classifies customer support ticket intent and urgency."""

    def __init__(self):
        """Initialize the intent classifier."""
        logger.info("IntentClassifier initialized")

    def classify(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify ticket intent and urgency.

        Args:
            ticket_data: Dictionary containing ticket data

        Returns:
            Ticket data enriched with intent and urgency
        """
        message = ticket_data.get('message', '').lower()
        ticket_id = ticket_data.get('ticket_id')

        logger.info(f"Classifying intent for ticket: {ticket_id}")

        # Simple rule-based classification (replace with ML model in production)
        intent = self._classify_intent(message)
        urgency = self._classify_urgency(message)

        ticket_data['intent'] = intent
        ticket_data['urgency'] = urgency
        ticket_data['classification_confidence'] = 0.85

        return ticket_data

    def _classify_intent(self, message: str) -> str:
        """Classify intent using simple keyword matching."""
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
