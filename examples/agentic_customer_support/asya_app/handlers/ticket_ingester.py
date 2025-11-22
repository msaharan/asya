"""Ticket ingestion handler - receives and validates incoming tickets."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def process(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process incoming ticket.

    Args:
        payload: Dictionary containing ticket data with keys:
            - ticket_id: Unique ticket identifier
            - customer_id: Customer identifier
            - message: Customer message/text
            - source: Source of ticket (email, chat, etc.)
            - timestamp: Timestamp of ticket creation

    Returns:
        Enriched payload with validation status and metadata
    """
    logger.info(f"Processing ticket: {payload.get('ticket_id')}")

    # Validate required fields
    required_fields = ['ticket_id', 'customer_id', 'message']
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        logger.error(f"Missing required fields: {missing_fields}")
        payload['validation_status'] = 'invalid'
        payload['error'] = f"Missing required fields: {missing_fields}"
        return payload

    # Basic validation
    if not payload.get('message') or len(payload['message'].strip()) == 0:
        payload['validation_status'] = 'invalid'
        payload['error'] = "Message cannot be empty"
        return payload

    # Enrich with metadata
    payload['validation_status'] = 'valid'
    payload['message_length'] = len(payload['message'])
    payload['processed_at'] = __import__('datetime').datetime.utcnow().isoformat()

    logger.info(f"Ticket {payload['ticket_id']} validated successfully")
    return payload
