from rest_framework import serializers

from blog.models import Post, Ingredient

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'clories', 'price', 'created_date', 'image', 'type')

    def get_validation_exclusions(selfself, *args, **kwargs):
        exclussions = super(PostSerializer, self)