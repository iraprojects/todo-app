""" from rest_framework import viewsets
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class TaskListApiView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailApiView(APIView):
    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get_subtasks(self, pk):
        parent_task = self.get_task(pk)
        if parent_task:
            subtask = SubTask.objects.filter(task=parent_task)
            return subtask
        return None

    def get(self, request, pk):
        task = self.get_task(pk)
        if task:
            serializer = TaskSerializer(task)
            subtasks = self.get_subtasks(pk)
            if subtasks:
                subtask_serializer = SubTaskSerializer(subtasks, many=True)
                response_data = {
                    "task": serializer.data,
                    "subtasks": subtask_serializer.data,
                }
                return Response(response_data)
            return Response(serializer.data)
        return Response(
            {"status": "NOT FOUND", "details": f"Task {pk} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    def post(self, request, pk):
        parent_task = self.get_task(pk)
        if not parent_task:
            return Response(
                {"status": "NOT FOUND", "details": f"Task {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=parent_task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = self.get_task(pk)
        if not task:
            return Response(
                {"status": "NOT FOUND", "details": f"Task {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_task(pk)
        if not task:
            return Response(
                {"status": "NOT FOUND", "details": f"Task {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubtaskView(APIView):
    def get(self, request):
        subtask = SubTask.objects.all()
        serializer = SubTaskSerializer(subtask, many=True)
        return Response(serializer.data)


class SubtaskViewDetail(APIView):
    def get_subtask(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_subtask(pk)
        if subtask:
            serializer = SubTaskSerializer(subtask)
            return Response(serializer.data)
        return Response(
            {"status": "NOT FOUND", "details": f"Task {pk} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    def put(self, request, pk):
        subtask = self.get_subtask(pk)
        if not subtask:
            return Response(
                {"status": "NOT FOUND", "details": f"Task {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_subtask(pk)
        if not subtask:
            return Response(
                {"status": "NOT FOUND", "details": f"Task {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
