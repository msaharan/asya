"""Escalation handler - handles escalation to human agents."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def process(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle escalation to human agents.

    Args:
        payload: Ticket payload that needs escalation

    Returns:
        Payload with escalation information
    """
    ticket_id = payload.get('ticket_id')
    urgency = payload.get('urgency', 'low')
    intent = payload.get('intent', 'general')

    logger.info(f"Handling escalation for ticket: {ticket_id}")

    # Determine if escalation is needed
    should_escalate = (
        urgency == 'high' or
        payload.get('judge_score', 1.0) < 0.5 or
        payload.get('escalate', False)
    )

    if should_escalate:
        payload['escalated'] = True
        payload['escalation_reason'] = (
            'high_urgency' if urgency == 'high' else
            'low_quality_response' if payload.get('judge_score', 1.0) < 0.5 else
            'manual_escalation'
        )
        payload['assigned_to'] = 'human_agent_queue'
        payload['escalated_at'] = __import__('datetime').datetime.utcnow().isoformat()

        logger.info(f"Ticket {ticket_id} escalated to human agent: {payload['escalation_reason']}")
    else:
        payload['escalated'] = False
        logger.info(f"Ticket {ticket_id} does not require escalation")

    return payload
