from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LogSerializer
from .models import Log
from common.permission import HasRolePermission
from rest_framework.permissions import IsAuthenticated
from .serializers import LogSerializer
from .pagination import LogPagination



class DashboardView(APIView):
    permission_classes = [IsAuthenticated, HasRolePermission]
    required_roles = ["analyst", "admin"]

    def get(self, request):
        return render(request, "analytics/dashboard.html")
    



class LogsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = Log.objects.all().order_by("-timestamp")

        paginator = LogPagination()
        paginated_logs = paginator.paginate_queryset(logs, request)

        serializer = LogSerializer(paginated_logs, many=True)

        return paginator.get_paginated_response(serializer.data)