# views.py
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_target  # your shredding core function


class ShredStartAPI(APIView):
    """
    API endpoint to start the file shredding process synchronously.
    Compatible with frontend sending:
      - target_path
      - passes
      - chunk_size_mb
      - wipe_free_space
    """

    def post(self, request, *args, **kwargs):
        # Log incoming request for debugging
        print("\n=== INCOMING SHRED REQUEST ===")
        print(request.data)
        print("==============================\n")

        # --- Parse input safely ---
        try:
            data = request.data
            target_path = data.get('target_path')
            passes = int(data.get('passes', 7))
            chunk_size_mb = int(data.get('chunk_size_mb', 50))
            # Convert string "true"/"false" to boolean
            wipe_free = str(data.get('wipe_free_space', 'false')).lower() == 'true'

        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid input types for 'passes' or 'chunk_size_mb'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not target_path:
            return Response({"error": "Missing 'target_path'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # --- Run shredding synchronously ---
        try:
            print(f"DEBUG: Starting shredding for {target_path}")
            result = process_target(target_path, passes, chunk_size_mb, wipe_free)

            return Response({
                "status": "success",
                "message": f"Shredding completed successfully for {target_path}.",
                "result": result
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("\n--- SHRED TASK FAILED ---")
            traceback.print_exc()
            return Response({
                "status": "failure",
                "error": "Shredding failed during execution.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ShredStatusAPI(APIView):
    """
    Placeholder status endpoint for compatibility with frontend.
    Since shredding is synchronous, this just returns a static message.
    """
    def get(self, request, task_id, *args, **kwargs):
        return Response({
            "status": "Synchronous mode: no task tracking. Task ID received."
        }, status=status.HTTP_200_OK)
