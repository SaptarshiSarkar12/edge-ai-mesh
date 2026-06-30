import sys
import time
from concurrent import futures
from pathlib import Path

import grpc
import torch

# Add "generated" folder to the Python path to ensure Protobuf imports work correctly
sys.path.append(str(Path(__file__).parent / "generated"))

import inference_pb2
import inference_pb2_grpc


class ComputeServicer(inference_pb2_grpc.EdgeComputeServicer):
    def RunInference(self, request, context):
        start_time = time.perf_counter()

        # Convert the incoming binary stream directly to a PyTorch tensor
        input_tensor = torch.tensor(request.data, dtype=torch.float32)

        # Run heavy math (this drops into C++, bypassing the Python GIL)
        weights = torch.ones_like(input_tensor) * 2.5
        result = input_tensor * weights

        # Calculate execution time in milliseconds
        exec_time = (time.perf_counter() - start_time) * 1000

        # Return the exact structure defined in the .proto file
        return inference_pb2.TensorResponse(
            output=result.tolist(),
            execution_time_ms=exec_time
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    inference_pb2_grpc.add_EdgeComputeServicer_to_server(ComputeServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 Compute Node (Real PyTorch NN) listening on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()