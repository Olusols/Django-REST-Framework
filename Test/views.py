from cgitb import lookup
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import TestApp
# Let's access the REST Framework
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from .serializers import ChoiceSerializer, TestAppSerializer, VoteSerializer
from rest_framework import generics, viewsets, status

from Test import serializers


# Create your views here.

def simple(request):
    method = request.method.lower()
    
    if method == 'get':
        
        return JsonResponse(
        {
        'response':'Welcome home',
        'method': request.method
        
        }
        )
        
    elif method == 'post':
        return JsonResponse(
            {
                'data': 'Added new data',
            }
        )
        
    return 'No data'

class SimpleAPI(APIView):
    
    
    
    
    def post(self, request):
        serializer = TestAppSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        print(request.data)
        
        new_test = TestApp.objects.create(
            name=request.data.get('name')
        )
        return JsonResponse({
            'data': serializer.data
        })
        
    def get(self, request):
        from .models import TestApp
        content  = TestApp.objects.all().values()
        
        
        return JsonResponse({
            'data': TestAppSerializer(content, many=True).data
        })
        
    def put(self, request,*args, **kwargs):
        model_id = kwargs.get('id', None)
       
        if not model_id:
           return JsonResponse({'error':'method "PUT" not allowed'})
        try:
           instance = TestApp.objects.get(id=model_id)
           
        except:
           return JsonResponse({'error':'Object does not exist'})
        
        serializer = TestAppSerializer(data = request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return JsonResponse({'data':serializer.data})
        

class SimpleGenerics(generics.ListCreateAPIView):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer
    
class SimpleGenericsUpdate(generics.UpdateAPIView):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer
    lookup_field = 'id'
    
    
    
####### LET'S GO DO VIEWSET

class SimpleViewSet(viewsets.ModelViewSet):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer
    
    
from .models import Poll 
from django.http import JsonResponse 
from django.shortcuts import render, get_object_or_404
def poll(request):
    
    poll = Poll.objects.all()[:20]
    data = {
        'result':
            
            list(poll.values('question', 'created_by__username', 'pub_date'))
    }
    
    return JsonResponse(data)


def poll_detail(request, id):

    poll = get_object_or_404(Poll,id=id)
    data = {
        'result':
            
            {
                
            'question': poll.question,
            'user': poll.created_by.username,
            'pub_date': poll.pub_date,
            
                
            }
    }
    
    return JsonResponse(data)

############# 

from rest_framework.views import APIView
from rest_framework.response import Response


from django.shortcuts import get_object_or_404
from .models import Poll, Choice
from .serializers import PollSerializer


class PollList(APIView):
    def get(self, request):
        polls = Poll.objects.all()[:20]
        data = PollSerializer(polls, many=True).data
        return Response(data)


class PollDetail(APIView):
   def get(self, request, pk):
       poll = get_object_or_404(Poll, pk=pk)
       data = PollSerializer(poll).data
       return Response(data)




from rest_framework import generics

class PollListSerial(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    
class PollCreateSerial(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = 'id'
    

class VoteCreate(generics.CreateAPIView):
    serializer_class  = VoteSerializer
    
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get('voted_by')
        data = {
            'choices': choice_pk,
            'poll': pk,
            'voted_by': voted_by
            
        }
        serialized = VoteSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs.get('pk'))
        return queryset
    serializer_class = ChoiceSerializer
    
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=self.kwargs.get('pk'))
        if not request.user == poll.created_by:
            raise PermissionDenied("You don't have access to this poll. The poll has to be yours")
        return super().post(request, *args, **kwargs)
        
    
    
from rest_framework.routers import DefaultRouter
from rest_framework.exceptions import PermissionDenied


class PollViewSet(viewsets.ModelViewSet):
    queryset  = Poll.objects.all()
    serializer_class = PollSerializer 
    
    
    
      

    def destroy(self, request, *args, **kwargs):
        
        poll = Poll.objects.get(id=self.kwargs.get('pk'))
        if not request.user == poll.created_by:
            raise PermissionDenied('You cannot delete this poll')
        return super().destroy(request,*args, **kwargs)
            


from .serializers import UserSerializer
from django.contrib.auth.models import User

class UserCreate(generics.ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    
from django.contrib.auth import authenticate

class LoginView(APIView):
    permission_classes = ()
    
    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            return Response({
                'token': user.auth_token.key
            })
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    