"""Response generation handler for Ray Serve."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Generates customer support responses using LLM."""

    def __init__(self):
        """Initialize the response generator."""
        logger.info("ResponseGenerator initialized")

    def generate(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate response using LLM with context.

        Args:
            ticket_data: Ticket data with knowledge context

        Returns:
            Ticket data enriched with generated response
        """
        message = ticket_data.get('message', '')
        intent = ticket_data.get('intent', 'general')
        knowledge_context = ticket_data.get('knowledge_context', [])
        ticket_id = ticket_data.get('ticket_id')

        logger.info(f"Generating response for ticket: {ticket_id}")

        context_text = '\n'.join([ctx.get('content', '') for ctx in knowledge_context])
        response = self._generate_response(message, intent, context_text)

        ticket_data['generated_response'] = response
        ticket_data['response_generated_at'] = __import__('datetime').datetime.utcnow().isoformat()

        return ticket_data

    def _generate_response(self, message: str, intent: str, context: str) -> str:
        """Generate response using LLM (mock implementation)."""
        response_templates = {
            'refund': f"Thank you for contacting us. Based on your inquiry: '{message}', I understand you're requesting a refund. {context} Please provide your order ID and we'll process your refund within 5-7 business days.",
            'technical_issue': f"I see you're experiencing a technical issue: '{message}'. {context} Let me help you troubleshoot this. Can you provide more details about when this issue started?",
            'cancellation': f"Thank you for reaching out. Regarding your cancellation request: '{message}'. {context} You can manage your subscription from your account settings.",
            'question': f"Thank you for your question: '{message}'. {context} I hope this information helps. If you need further assistance, please let me know.",
            'general': f"Thank you for contacting us about: '{message}'. {context} I'm here to help. Could you provide more details so I can assist you better?"
        }

        return response_templates.get(intent, response_templates['general'])
