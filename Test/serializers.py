from rest_framework import serializers, status
from .models import Poll, TestApp, Vote, Choice

class SimpleObject():
    def __init__(self, name):
        self.name = name
        
class SimpleObjectSerailizer(serializers.Serializer):
    name = serializers.CharField()

def run_data():
    simple = SimpleObject('Olusols')
    ser = SimpleObjectSerailizer(simple)
    print(ser.data)
    
    
class TestApSerializer(serializers.Serializer):
    id  = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    
    def create(self, validated_data):
        return TestApp.objects.create(**validated_data)
    
    def update(self, instance,validated_data):
        
        TestApp.objects.filter(id=instance.id).update(**validated_data)
        return TestApp.objects.get(id=instance.id)
    
    


class TestAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestApp
        fields = '__all__'
        
        
####### Let's create serializers for Poll, Choice and Vote



class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = '__all__'
        
class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'
        
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        extra_kwargs = {
        
          'password': {
            'write_only': True,
        },
        
    }
        
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        
        return user
    
    