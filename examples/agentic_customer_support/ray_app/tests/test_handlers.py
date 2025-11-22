"""Unit tests for Ray Serve handlers."""

import pytest
from ray_app.handlers.intent_classifier import IntentClassifier
from ray_app.handlers.knowledge_retriever import KnowledgeRetriever
from ray_app.handlers.response_generator import ResponseGenerator
from ray_app.handlers.response_validator import ResponseValidator


def test_intent_classifier():
    """Test intent classification."""
    classifier = IntentClassifier()
    ticket = {
        'ticket_id': 'TICKET-001',
        'customer_id': 'CUST-123',
        'message': 'I need a refund'
    }
    result = classifier.classify(ticket)
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
        'intent': 'refund'
    }
    result = retriever.retrieve(ticket)
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
        'intent': 'refund',
        'knowledge_context': [
            {'content': 'Refunds are processed within 5-7 business days.', 'source': 'refund_policy.md'}
        ]
    }
    result = generator.generate(ticket)
    assert 'generated_response' in result
    assert len(result['generated_response']) > 0


def test_response_validator():
    """Test response validation."""
    validator = ResponseValidator(threshold=0.7)
    ticket = {
        'ticket_id': 'TICKET-001',
        'customer_id': 'CUST-123',
        'message': 'I need a refund',
        'generated_response': 'Thank you for contacting us. We will process your refund within 5-7 business days.'
    }
    result = validator.validate(ticket)
    assert 'judge_score' in result
    assert result['judge_score'] >= 0.0
    assert result['judge_score'] <= 1.0
    assert 'validation_passed' in result
