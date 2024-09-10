from rest_framework import serializers

from blog.models import Post
from accounts.models import Profile


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_content_snippet")
    relative_url = serializers.URLField(source="get_relative_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "author",
            "title",
            "content",
            "snippet",
            "category",
            "published_status",
            "published_at",
            "relative_url",
            "absolute_url",
        ]
        read_only_fields = [
            "author",
            "published_status",
            "published_at",
        ]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
