"""Knowledge base retrieval handler for Ray Serve."""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class KnowledgeRetriever:
    """Retrieves relevant information from knowledge base."""

    def __init__(self):
        """Initialize the knowledge retriever."""
        self._mock_kb = self._init_mock_kb()
        logger.info("KnowledgeRetriever initialized")

    def retrieve(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve relevant knowledge base entries.

        Args:
            ticket_data: Ticket data with intent classification

        Returns:
            Ticket data enriched with knowledge base context
        """
        intent = ticket_data.get('intent', 'general')
        message = ticket_data.get('message', '')
        ticket_id = ticket_data.get('ticket_id')

        logger.info(f"Retrieving knowledge for ticket: {ticket_id}, intent: {intent}")

        relevant_context = self._retrieve_context(message, intent)

        ticket_data['knowledge_context'] = relevant_context
        ticket_data['context_sources'] = [ctx.get('source') for ctx in relevant_context]

        return ticket_data

    def _retrieve_context(self, message: str, intent: str) -> List[Dict[str, Any]]:
        """Retrieve relevant context from knowledge base."""
        context_map = {
            'refund': [
                {
                    'content': 'Refunds are processed within 5-7 business days. Contact support with order ID.',
                    'source': 'refund_policy.md',
                    'relevance_score': 0.9
                }
            ],
            'technical_issue': [
                {
                    'content': 'For technical issues, try clearing cache and cookies. If problem persists, contact support.',
                    'source': 'troubleshooting.md',
                    'relevance_score': 0.85
                }
            ],
            'cancellation': [
                {
                    'content': 'You can cancel your subscription from account settings. Cancellations take effect at end of billing period.',
                    'source': 'cancellation_policy.md',
                    'relevance_score': 0.9
                }
            ],
            'question': [
                {
                    'content': 'For general questions, check our FAQ section or contact support.',
                    'source': 'faq.md',
                    'relevance_score': 0.7
                }
            ]
        }

        return context_map.get(intent, [
            {
                'content': 'For assistance, please contact our support team.',
                'source': 'general_support.md',
                'relevance_score': 0.5
            }
        ])

    def _init_mock_kb(self) -> Dict[str, Any]:
        """Initialize mock knowledge base."""
        return {
            'refund_policy.md': 'Refund policy content...',
            'troubleshooting.md': 'Troubleshooting guide...',
            'cancellation_policy.md': 'Cancellation policy...',
            'faq.md': 'Frequently asked questions...',
        }
