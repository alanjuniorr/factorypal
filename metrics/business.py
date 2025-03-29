from collections import deque
import time
import threading

# Maintain in-memory storage for speed data
class MetricsService:
    def __init__(self):
        self.lines_data = {}  # Dictionary: {line_id: deque([(timestamp, speed)])}
        self.lock = threading.Lock()  # Ensure thread safety

    def add_speed(self, line_id, speed, timestamp):
        """Handles adding speed data while maintaining a sliding 60-minute window"""

        with self.lock:

            queue = self.lines_data[line_id]
            queue.append((timestamp, speed))

            # Remove old values beyond 60 minutes
            while queue and queue[0][0] < int(time.time() * 1000) - 3600000:
                queue.popleft()


    def get_metrics(self, line_id):
        """Retrieve avg, min, and max speed values for the last 60 minutes"""

        with self.lock:
            if line_id not in self.lines_data or not self.lines_data[line_id]:
                return None

            speeds = [speed for _, speed in self.lines_data[line_id]]

            return {
                "avg": sum(speeds) / len(speeds),
                "max": max(speeds),
                "min": min(speeds),
            }


    def initialize_lines(self, known_lines):
        """Initialize the known production lines"""

        with self.lock:
            for line_id in known_lines:
                if line_id not in self.lines_data:
                    self.lines_data[line_id] = deque()
