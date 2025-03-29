from rest_framework import serializers

class LineSpeedSerializer(serializers.Serializer):
    line_id = serializers.IntegerField()
    speed = serializers.FloatField()
    timestamp = serializers.IntegerField()

class MetricsSerializer(serializers.Serializer):
    avg = serializers.FloatField()
    max = serializers.FloatField()
    min = serializers.FloatField()
