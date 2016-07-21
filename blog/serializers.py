from rest_framework import serializers

from blog.models import Post, Ingredient


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'clories', 'price', 'created_date', 'image', 'type')

    def get_validation_exclusions(self, *args, **kwargs):
        exclussions = super(PostSerializer, self)