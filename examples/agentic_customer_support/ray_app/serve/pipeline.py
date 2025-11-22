"""Ray Serve deployment graph for customer support pipeline."""

import logging
from typing import Dict, Any

from ray import serve
from ray.serve import Application

from ray_app.handlers.intent_classifier import IntentClassifier
from ray_app.handlers.knowledge_retriever import KnowledgeRetriever
from ray_app.handlers.response_generator import ResponseGenerator
from ray_app.handlers.response_validator import ResponseValidator

logger = logging.getLogger(__name__)


@serve.deployment(
    name="intent-classifier",
    num_replicas=2,
    autoscaling_config={
        "min_replicas": 0,
        "max_replicas": 10,
        "target_num_ongoing_requests_per_replica": 5,
    }
)
class IntentClassifierDeployment:
    """Ray Serve deployment for intent classification."""

    def __init__(self):
        self.classifier = IntentClassifier()

    async def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle classification request."""
        return self.classifier.classify(request)


@serve.deployment(
    name="knowledge-retriever",
    num_replicas=2,
    autoscaling_config={
        "min_replicas": 0,
        "max_replicas": 10,
        "target_num_ongoing_requests_per_replica": 5,
    }
)
class KnowledgeRetrieverDeployment:
    """Ray Serve deployment for knowledge retrieval."""

    def __init__(self):
        self.retriever = KnowledgeRetriever()

    async def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle knowledge retrieval request."""
        return self.retriever.retrieve(request)


@serve.deployment(
    name="response-generator",
    num_replicas=1,
    autoscaling_config={
        "min_replicas": 0,
        "max_replicas": 5,
        "target_num_ongoing_requests_per_replica": 2,
    }
)
class ResponseGeneratorDeployment:
    """Ray Serve deployment for response generation."""

    def __init__(self):
        self.generator = ResponseGenerator()

    async def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle response generation request."""
        return self.generator.generate(request)


@serve.deployment(
    name="response-validator",
    num_replicas=1,
    autoscaling_config={
        "min_replicas": 0,
        "max_replicas": 5,
        "target_num_ongoing_requests_per_replica": 5,
    }
)
class ResponseValidatorDeployment:
    """Ray Serve deployment for response validation."""

    def __init__(self):
        self.validator = ResponseValidator(threshold=0.7)

    async def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle response validation request."""
        return self.validator.validate(request)


@serve.deployment(
    name="customer-support-pipeline",
    route_prefix="/support"
)
class CustomerSupportPipeline:
    """Main pipeline orchestrator."""

    def __init__(
        self,
        intent_classifier,
        knowledge_retriever,
        response_generator,
        response_validator
    ):
        self.intent_classifier = intent_classifier
        self.knowledge_retriever = knowledge_retriever
        self.response_generator = response_generator
        self.response_validator = response_validator

    async def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process customer support ticket through the pipeline.

        Args:
            request: Dictionary containing ticket data:
                - ticket_id: Unique ticket identifier
                - customer_id: Customer identifier
                - message: Customer message/text
                - source: Source of ticket (email, chat, etc.)

        Returns:
            Dictionary with formatted response
        """
        # Validate input
        if not request.get('message') or len(request.get('message', '').strip()) == 0:
            return {
                'error': 'Message cannot be empty',
                'ticket_id': request.get('ticket_id')
            }

        ticket_data = request.copy()
        ticket_data['validation_status'] = 'valid'

        try:
            # Step 1: Classify intent
            ticket_data = await self.intent_classifier.remote(ticket_data)

            # Step 2: Retrieve knowledge
            ticket_data = await self.knowledge_retriever.remote(ticket_data)

            # Step 3: Generate response
            ticket_data = await self.response_generator.remote(ticket_data)

            # Step 4: Validate response
            ticket_data = await self.response_validator.remote(ticket_data)

            # Step 5: Format response
            formatted_response = {
                'ticket_id': ticket_data.get('ticket_id'),
                'customer_id': ticket_data.get('customer_id'),
                'response_text': ticket_data.get('generated_response'),
                'intent': ticket_data.get('intent'),
                'urgency': ticket_data.get('urgency'),
                'quality_score': ticket_data.get('judge_score'),
                'formatted_at': __import__('datetime').datetime.utcnow().isoformat(),
                'sources': ticket_data.get('context_sources', [])
            }

            ticket_data['formatted_response'] = formatted_response
            ticket_data['status'] = 'completed'

            return ticket_data

        except Exception as e:
            logger.error(f"Error processing ticket {ticket_data.get('ticket_id')}: {e}")
            return {
                'error': str(e),
                'ticket_id': ticket_data.get('ticket_id'),
                'status': 'failed'
            }


# Build the deployment graph
def build_app() -> Application:
    """Build the Ray Serve application."""
    intent_classifier = IntentClassifierDeployment.bind()
    knowledge_retriever = KnowledgeRetrieverDeployment.bind()
    response_generator = ResponseGeneratorDeployment.bind()
    response_validator = ResponseValidatorDeployment.bind()

    pipeline = CustomerSupportPipeline.bind(
        intent_classifier,
        knowledge_retriever,
        response_generator,
        response_validator
    )

    return pipeline
