from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utc_now():
    """Return current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


class Category(db.Model):
    """Category model for organizing blog posts."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    emoji = db.Column(db.String(10), default='')
    display_order = db.Column(db.Integer, default=0)
    
    # Relationship
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Post(db.Model):
    """Blog post model."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), default='')
    read_time = db.Column(db.String(20), default='5 min read')
    published_date = db.Column(db.DateTime, default=utc_now)
    updated_date = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    
    # Foreign Key
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Meta fields for SEO
    meta_description = db.Column(db.String(300), default='')
    meta_keywords = db.Column(db.String(300), default='')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    @property
    def formatted_date(self):
        """Return formatted publication date."""
        return self.published_date.strftime('%B %d, %Y')
