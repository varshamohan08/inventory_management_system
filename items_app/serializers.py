from rest_framework import serializers
from .models import Item
from user_app.serializers import UserSerializer

class itemSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M %p', read_only=True)
    updated_by = UserSerializer(read_only=True)
    updated_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M %p', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_by', 'created_date', 'updated_by', 'updated_date', 'bln_active']

    def validate(self, attrs):
        name = attrs.get('name')
        
        if self.instance:
            if Item.objects.filter(name=name).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'name': 'Item with this name already exists.'})
        else:
            if Item.objects.filter(name=name).exists():
                raise serializers.ValidationError({'name': 'Item with this name already exists.'})

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):

        validated_data.pop('created_by', None)
        validated_data.pop('created_date', None)
        validated_data.pop('updated_by', None)
        validated_data.pop('updated_date', None)

        request = self.context.get('request')
        validated_data['updated_by'] = request.user

        instance = super().update(instance, validated_data)
        instance.save()
        
        return instance
