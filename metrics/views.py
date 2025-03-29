from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LineSpeedSerializer, MetricsSerializer
from .business import MetricsService
import time

# Initialize the in-memory service
metrics_service = MetricsService()
# Must be updated with known line IDs, I put just 11 and 20 as it is in the example
metrics_service.initialize_lines([11, 20])


class LineSpeedView(APIView):
    """POST /linespeed - Handles incoming speed measurements"""

    def post(self, request):
        serializer = LineSpeedSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # If the line id is not pre-defined
            if data['line_id'] not in metrics_service.lines_data.keys():
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Get current timestamp in millis, If older than 60 minutes, discard
            if data['timestamp'] < int(time.time() * 1000) - 3600000:
                return Response(status=status.HTTP_204_NO_CONTENT)

            metrics_service.add_speed(data["line_id"], data["speed"], data["timestamp"])
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricsView(APIView):
    """GET /metrics/{lineid} - Retrieves metrics for a production line"""

    def get(self, request, lineid=None):
        if lineid is None:

            # Return metrics for all known lines
            metrics_data = []
            for line_id in metrics_service.lines_data.keys():
                metrics = metrics_service.get_metrics(line_id)
                if metrics:
                    metrics_data.append({"line_id": line_id, "metrics": metrics})
            return Response(metrics_data, status=status.HTTP_200_OK)

        if lineid not in metrics_service.lines_data.keys():
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Return metrics for a specific line
        metrics = metrics_service.get_metrics(int(lineid))
        return Response(metrics, status=status.HTTP_200_OK)
