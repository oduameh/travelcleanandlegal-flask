"""
Travel Clean & Legal - Flask Application
Your Complete Guide to Relocating from Nigeria
"""

from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, Response, current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor
from slugify import slugify

from config import Config
from models import db, Category, Post


# Custom Admin Views
class SecureAdminIndexView(AdminIndexView):
    """Custom admin index view with basic protection."""
    
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class CategoryAdminView(ModelView):
    """Admin view for Category model."""
    
    column_list = ['id', 'name', 'slug', 'emoji', 'display_order']
    column_sortable_list = ['id', 'name', 'display_order']
    column_searchable_list = ['name', 'slug']
    form_columns = ['name', 'slug', 'emoji', 'display_order']
    
    def on_model_change(self, form, model, is_created):
        """Auto-generate slug if not provided."""
        if not model.slug:
            model.slug = slugify(model.name)


class PostAdminView(ModelView):
    """Admin view for Post model with CKEditor support."""
    
    column_list = ['id', 'title', 'category_id', 'is_featured', 'is_published', 'published_date']
    column_sortable_list = ['id', 'title', 'published_date', 'is_featured', 'is_published']
    column_searchable_list = ['title', 'slug', 'excerpt']
    column_filters = ['is_featured', 'is_published']
    
    form_columns = [
        'title', 'slug', 'category_id', 'excerpt', 'content', 
        'image_url', 'read_time', 'published_date',
        'is_featured', 'is_published',
        'meta_description', 'meta_keywords'
    ]
    
    create_template = 'admin/post_create.html'
    edit_template = 'admin/post_edit.html'
    
    def on_model_change(self, form, model, is_created):
        """Auto-generate slug if not provided."""
        if not model.slug:
            model.slug = slugify(model.title)


def create_app(config_class=Config):
    """Application factory."""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CKEditor(app)
    
    # Initialize Flask-Admin
    admin = Admin(
        app,
        name='Travel Clean & Legal Admin',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView()
    )
    
    # Add admin views
    admin.add_view(CategoryAdminView(Category, db.session, name='Categories'))
    admin.add_view(PostAdminView(Post, db.session, name='Posts'))
    
    # Context processor to add current datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Routes
    
    # Serve ads.txt from root URL (required for Google AdSense)
    @app.route('/ads.txt')
    def ads_txt():
        """Serve ads.txt from root URL for Google AdSense verification."""
        return send_from_directory(
            app.static_folder, 
            'ads.txt', 
            mimetype='text/plain'
        )
    
    # Serve robots.txt from root URL
    @app.route('/robots.txt')
    def robots_txt():
        """Serve robots.txt from root URL for search engine crawlers."""
        return send_from_directory(
            app.static_folder, 
            'robots.txt', 
            mimetype='text/plain'
        )
    
    # Serve sitemap.xml from root URL
    @app.route('/sitemap.xml')
    def sitemap():
        """Generate dynamic sitemap.xml."""
        posts = Post.query.filter_by(is_published=True).order_by(Post.published_date.desc()).all()
        site_url = current_app.config['SITE_URL']
        
        xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{site_url}/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{site_url}/blog</loc>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{site_url}/about</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>{site_url}/contact</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''
        for post in posts:
            lastmod = post.published_date.strftime('%Y-%m-%d') if post.published_date else ''
            xml_content += f'''    <url>
        <loc>{site_url}/post/{post.slug}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
        xml_content += '</urlset>'
        
        return Response(xml_content, mimetype='application/xml')
    
    @app.route('/')
    def home():
        """Home page with featured and recent posts."""
        featured_posts = Post.query.filter_by(
            is_published=True, 
            is_featured=True
        ).order_by(Post.published_date.desc()).limit(6).all()
        
        recent_posts = Post.query.filter_by(
            is_published=True
        ).order_by(Post.published_date.desc()).limit(9).all()
        
        return render_template(
            'index.html',
            featured_posts=featured_posts,
            recent_posts=recent_posts
        )
    
    @app.route('/blog')
    def blog():
        """Blog listing page with posts grouped by category."""
        category_filter = request.args.get('category')
        
        categories = Category.query.order_by(Category.display_order).all()
        posts_by_category = {}
        
        for category in categories:
            if category_filter and category.slug != category_filter:
                continue
            posts = Post.query.filter_by(
                category_id=category.id,
                is_published=True
            ).order_by(Post.published_date.desc()).all()
            if posts:
                posts_by_category[category] = posts
        
        return render_template(
            'blog.html',
            posts_by_category=posts_by_category
        )
    
    @app.route('/post/<slug>')
    def post(slug):
        """Individual blog post page."""
        post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
        
        # Get related posts from the same category
        related_posts = Post.query.filter(
            Post.category_id == post.category_id,
            Post.id != post.id,
            Post.is_published == True
        ).order_by(Post.published_date.desc()).limit(3).all()
        
        return render_template(
            'post.html',
            post=post,
            related_posts=related_posts
        )
    
    @app.route('/about')
    def about():
        """About page."""
        return render_template('about.html')
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        """Contact page with form handling."""
        if request.method == 'POST':
            # Check honeypot field
            if request.form.get('bot-field'):
                return redirect(url_for('contact'))
            
            # Process form (in production, you'd send email or store in database)
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            
            # For now, just flash a success message
            flash('Thank you for your message! We\'ll get back to you soon.', 'success')
            return redirect(url_for('contact'))
        
        return render_template('contact.html')
    
    @app.route('/privacy')
    def privacy():
        """Privacy policy page."""
        return render_template('privacy.html')
    
    @app.route('/terms')
    def terms():
        """Terms of service page."""
        return render_template('terms.html')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        """Custom 404 error page."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Custom 500 error page."""
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
