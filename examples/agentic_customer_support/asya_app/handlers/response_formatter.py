"""Response formatting handler - formats and finalizes response."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def process(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format and finalize the response.

    Args:
        payload: Ticket payload with generated response

    Returns:
        Payload with formatted final response
    """
    if payload.get('validation_status') != 'valid':
        return payload

    ticket_id = payload.get('ticket_id')
    generated_response = payload.get('generated_response', '')
    judge_score = payload.get('judge_score', 0.0)

    logger.info(f"Formatting response for ticket: {ticket_id}")

    # Format response with metadata
    formatted_response = {
        'ticket_id': ticket_id,
        'customer_id': payload.get('customer_id'),
        'response_text': generated_response,
        'intent': payload.get('intent'),
        'urgency': payload.get('urgency'),
        'quality_score': judge_score,
        'formatted_at': __import__('datetime').datetime.utcnow().isoformat(),
        'sources': payload.get('context_sources', [])
    }

    payload['formatted_response'] = formatted_response
    payload['status'] = 'completed'

    logger.info(f"Response formatted for ticket {ticket_id}")
    return payload
