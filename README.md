# Edge AI Inference Mesh

Distributed microservices architecture for AI inference at the edge

## Usage

There are currently two services available:

1. [**Compute Node**](./compute_node) - This service currently multiplies a weight matrix by an input vector.
2. [**Gateway API**](./gateway_api) - This service provides a REST API for clients to send requests to the compute nodes.

The services communicate with each other using gRPC. The gRPC server is implemented in the **Compute Node** service, while the **Gateway API** service acts as a gRPC client. The gRPC contract is defined in the [`protos`](./protos) directory.

You can start the services using the following commands:

1. Start the **Compute Node** service:
   ```bash
   cd compute_node
   uv run src/main.py
   ```
   
2. Start the **Gateway API** service in a separate terminal:
   ```bash
   cd gateway_api
   uv run uvicorn src.main:app --reload
   ```
   
You can then send requests to the **Gateway API** service using the following endpoint:

```
POST http://localhost:8000/inference
Content-Type: application/json
{
  "input_vector": [1.0, 2.0, 3.0]
}
```

## Roadmap

This is a work in progress, and I'm planning to:

- Add real AI inference capabilities to the **Compute Node** service.
- Implement a more robust service discovery mechanism for the **Gateway API** to find available compute nodes.
- Add authentication and authorization to the **Gateway API** service.
- Implement logging and monitoring for both services using OpenTelemetry.
- Move the gateway API and other backend services (except the compute node) to Java based microservices for better scalability and maintainability.
- Utilise a message broker like Kafka for high throughput and low latency communication between services.
- Use Kubernetes for orchestration and deployment of the services in a production environment.