import flask
from flask import jsonify, make_response

from app.models import Post

blueprint = flask.Blueprint('api', __name__)

@blueprint.route('/api/posts')
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if not posts:
        return jsonify({'message': 'No posts found'}), 200
    return jsonify({
        'posts': [item.to_dict() for item in posts]
    })

@blueprint.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return jsonify({
        'post': post.to_dict()
    })
