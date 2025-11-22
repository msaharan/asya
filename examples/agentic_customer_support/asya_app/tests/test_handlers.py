"""Unit tests for Asya handlers."""

import pytest
from handlers.ticket_ingester import process as ingest_ticket
from handlers.intent_classifier import IntentClassifier
from handlers.knowledge_retriever import KnowledgeRetriever
from handlers.response_generator import ResponseGenerator
from handlers.response_validator import ResponseValidator


def test_ticket_ingester_valid():
    """Test ticket ingestion with valid ticket."""
    ticket = {
        'ticket_id': 'TICKET-001',
        'customer_id': 'CUST-123',
        'message': 'I need help with my order',
        'source': 'email'
    }
    result = ingest_ticket(ticket)
    assert result['validation_status'] == 'valid'
    assert 'message_length' in result
    assert 'processed_at' in result


def test_ticket_ingester_invalid():
    """Test ticket ingestion with invalid ticket."""
    ticket = {
        'ticket_id': 'TICKET-002',
        'customer_id': 'CUST-123'
        # Missing message
    }
    result = ingest_ticket(ticket)
    assert result['validation_status'] == 'invalid'
    assert 'error' in result


def test_intent_classifier():
    """Test intent classification."""
    classifier = IntentClassifier()
    ticket = {
        'ticket_id': 'TICKET-001',
        'customer_id': 'CUST-123',
        'message': 'I need a refund',
        'validation_status': 'valid'
    }
    result = classifier.process(ticket)
    assert result['intent'] == 'refund'
    assert result['urgency'] in ['low', 'medium', 'high']
    assert 'classification_confidence' in result


def test_knowledge_retriever():
    """Test knowledge retrieval."""
    retriever = KnowledgeRetriever()
    ticket = {
        'ticket_id': 'TICKET-001',
        'customer_id': 'CUST-123',
        'message': 'I need a refund',
        'validation_status': 'valid',
        'intent': 'refund'
    }
    result = retriever.process(ticket)
    assert 'knowledge_context' in result
    assert len(result['knowledge_context']) > 0
    assert 'context_sources' in result


def test_response_generator():
    """Test response generation."""
    generator = ResponseGenerator()
    ticket = {
        'ticket_id': 'TICKET-001',
        'customer_id': 'CUST-123',
        'message': 'I need a refund',
        'validation_status': 'valid',
        'intent': 'refund',
        'knowledge_context': [
            {'content': 'Refunds are processed within 5-7 business days.', 'source': 'refund_policy.md'}
        ]
    }
    result = generator.process(ticket)
    assert 'generated_response' in result
    assert len(result['generated_response']) > 0


def test_response_validator():
    """Test response validation."""
    validator = ResponseValidator(threshold=0.7)
    envelope = {
        'payload': {
            'ticket_id': 'TICKET-001',
            'customer_id': 'CUST-123',
            'message': 'I need a refund',
            'validation_status': 'valid',
            'generated_response': 'Thank you for contacting us. We will process your refund within 5-7 business days.'
        },
        'route': {
            'actors': ['ticket-ingester', 'intent-classifier', 'response-validator'],
            'current': 2
        }
    }
    result = validator.process(envelope)
    assert 'judge_score' in result['payload']
    assert result['payload']['judge_score'] >= 0.0
    assert result['payload']['judge_score'] <= 1.0
