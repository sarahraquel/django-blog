import graphene
from graphene_django.types import DjangoObjectType
from blog.models.post import Post
from blog.models.comment import Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(object):
    all_posts = graphene.List(PostType)
    all_comments = graphene.List(CommentType)
    post = graphene.Field(PostType, id=graphene.Int(),
                              title=graphene.String())

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.select_related('post').all()

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Post.objects.get(pk=id)

        if title is not None:
            return Post.objects.get(title__contains=title)

        return None
