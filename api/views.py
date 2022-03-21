from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from home.models import Message
from .serializers import MessageSerializer


@api_view(['GET'])
def all_messages(request):
    msg = Message.objects.all()
    serializer = MessageSerializer(msg, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def message(request, pk):
    msg = Message.objects.get(id=pk)
    serializer = MessageSerializer(msg, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_message(request):
    usr = request.user
    data = request.data

    new_msg = Message.objects.create(username=usr, title=data['title'], text=data['text'])

    serializer = MessageSerializer(new_msg, many=False)
    return Response(serializer.data)
