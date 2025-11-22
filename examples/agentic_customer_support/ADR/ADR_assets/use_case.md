## Use case

### Minimal viable use-case

An agentic customer support system that processes customer inquiries through a multi-stage pipeline:

1. **Ticket Ingestion**: Receive customer support tickets (text, email, chat)
2. **Intent Classification**: Classify the intent/urgency of the ticket
3. **Knowledge Base Retrieval**: Retrieve relevant information from knowledge base
4. **Response Generation**: Generate response using LLM with context
5. **Response Validation**: Judge/validate the generated response quality
6. **Response Formatting**: Format and finalize the response
7. **Escalation Handling**: Route to human agent if needed

### Pipeline Flow

```
Ticket → Classify → Retrieve → Generate → Validate → Format → Output
                                    ↓
                              (if low score)
                                    ↓
                              Escalate
```

### Key Requirements

- **Scalability**: Handle bursty traffic (10x scale-up during peak hours)
- **Cost Efficiency**: Scale to zero during off-peak hours
- **Latency**: Near-realtime (< 5 seconds end-to-end for simple queries)
- **Reliability**: Retry failed stages, handle errors gracefully
- **Observability**: Track metrics, latency, and errors at each stage

### Comparison Criteria

When comparing Ray Serve vs Asya, we'll evaluate:

1. **Development Experience**
   - Code simplicity (pure Python vs infrastructure code)
   - Testing ease
   - Local development workflow

2. **Deployment & Operations**
   - Kubernetes integration
   - Scaling behavior (0→N scaling)
   - Resource utilization
   - Configuration complexity

3. **Performance**
   - End-to-end latency
   - Throughput under load
   - Resource efficiency

4. **Reliability**
   - Error handling
   - Retry mechanisms
   - Message durability

5. **Cost**
   - Infrastructure overhead
   - Scaling costs
   - Development/maintenance time
