import pytest
from feed.models import Post, Comment
import django.contrib.auth


User = django.contrib.auth.get_user_model()
POST_TITLE = "Some First Post Title"
POST_CONTENT = "Some first post content here"


@pytest.fixture
def users(db):
    user0 = User.objects.create_user('user1', password='pass123')
    user1 = User.objects.create_user('user2', password='pass321')
    return [user0, user1]


@pytest.fixture
def post0(db, users):
    return Post.posts.create(title=POST_TITLE, content=POST_CONTENT, author=users[0])


COMMENT1_CONTENT = "Some first comment content goes here"
COMMENT2_CONTENT = "Some second comment content goes here"


@pytest.fixture
def comments(post0, users):
    comment0 = Comment(author=users[1], post_parent=post0, content=COMMENT1_CONTENT)
    comment1 = Comment(author=users[0], post_parent=post0, comment_parent=comment0, content=COMMENT2_CONTENT)
    return [comment0, comment1]


@pytest.mark.django_db
class TestPostCommentRelation:
    # Testing post model and comment model relation

    def test_post_removal_to_comment(self, post0, comments):
        # Testing that a parent post removal also removes the comment
        # In this case the post parent of comments[0] is post0
        post0.save()
        comments[0].save()
        post0.delete()
        assert post0 not in Post.posts.main_feed()
        assert comments[0] not in Comment.comments.all()

    def test_comment_removal_to_post(self, post0, comments):
        # Testing that a comment removal doesn't also removes the parent post
        # In this case the post parent of comments[0] is post0
        post0.save()
        comments[0].save()
        comments[0].delete()
        assert comments[0] not in Comment.comments.all()
        assert post0 in Post.posts.main_feed()
