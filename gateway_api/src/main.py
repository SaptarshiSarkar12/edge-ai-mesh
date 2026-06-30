import sys
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
import grpc

# Add "generated" folder to the Python path to ensure Protobuf imports work correctly
sys.path.append(str(Path(__file__).parent / "generated"))

import inference_pb2
import inference_pb2_grpc

app = FastAPI(title="Edge AI Mesh Gateway")


@app.post("/predict")
async def predict(payload: List[float]):
    if not payload:
        raise HTTPException(status_code=400, detail="Payload cannot be empty")

    # Open an async network channel to the Compute Node
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = inference_pb2_grpc.EdgeComputeStub(channel)

        # Package the JSON HTTP payload into strict Protobuf binary
        request = inference_pb2.TensorRequest(
            model_name="v1-matrix",
            data=payload
        )

        try:
            # Send over the network and await the response without blocking FastAPI
            response = await stub.RunInference(request)

            return {
                "status": "success",
                "compute_time_ms": round(response.execution_time_ms, 4),
                "result": list(response.output)
            }
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Compute Node Error: {e.details()}")