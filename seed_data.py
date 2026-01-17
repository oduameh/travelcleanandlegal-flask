"""
Seed script to populate the database with categories and blog posts.
Imports content from the original static HTML files.
"""

import os
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from slugify import slugify

from app import create_app
from models import db, Category, Post


# Category definitions with display order
CATEGORIES = [
    {'name': 'United Kingdom', 'slug': 'uk', 'emoji': '🇬🇧', 'display_order': 1},
    {'name': 'Canada', 'slug': 'canada', 'emoji': '🇨🇦', 'display_order': 2},
    {'name': 'Germany', 'slug': 'germany', 'emoji': '🇩🇪', 'display_order': 3},
    {'name': 'Australia', 'slug': 'australia', 'emoji': '🇦🇺', 'display_order': 4},
    {'name': 'United States', 'slug': 'usa', 'emoji': '🇺🇸', 'display_order': 5},
    {'name': 'Ireland', 'slug': 'ireland', 'emoji': '🇮🇪', 'display_order': 6},
    {'name': 'Netherlands', 'slug': 'netherlands', 'emoji': '🇳🇱', 'display_order': 7},
    {'name': 'New Zealand', 'slug': 'new-zealand', 'emoji': '🇳🇿', 'display_order': 8},
    {'name': 'Portugal', 'slug': 'portugal', 'emoji': '🇵🇹', 'display_order': 9},
    {'name': 'UAE', 'slug': 'uae', 'emoji': '🇦🇪', 'display_order': 10},
    {'name': 'Healthcare', 'slug': 'healthcare', 'emoji': '🏥', 'display_order': 11},
    {'name': 'IELTS', 'slug': 'ielts', 'emoji': '📝', 'display_order': 12},
    {'name': 'Study Abroad', 'slug': 'study', 'emoji': '🎓', 'display_order': 13},
    {'name': 'Tech', 'slug': 'tech', 'emoji': '💻', 'display_order': 14},
    {'name': 'Planning & Finance', 'slug': 'planning', 'emoji': '💰', 'display_order': 15},
]


# Map post slugs to categories
POST_CATEGORY_MAP = {
    # UK Posts
    'uk-skilled-worker-visa-nigeria-2025': 'uk',
    'uk-care-worker-visa-nigeria-2025': 'uk',
    'uk-student-visa-nigeria-2025': 'uk',
    'how-to-get-job-uk-nigeria': 'uk',
    'uk-dependent-visa-families-nigeria': 'uk',
    'open-uk-bank-account-nigeria': 'uk',
    'uk-accommodation-new-arrivals-nigeria': 'uk',
    'uk-cv-guide-nigerians': 'uk',
    'uk-global-talent-visa-nigerians-2025': 'uk',
    'uk-graduate-visa-nigeria-2025': 'uk',
    
    # Canada Posts
    'canada-express-entry-nigeria-2025': 'canada',
    'canada-study-permit-nigerians-2025': 'canada',
    'canada-provincial-nominee-program-nigeria-2025': 'canada',
    
    # Germany Posts
    'germany-opportunity-card-nigeria-2025': 'germany',
    
    # Australia Posts
    'australia-skilled-migration-nigerians-2025': 'australia',
    
    # USA Posts
    'usa-visa-nigerians-2025': 'usa',
    
    # Ireland Posts
    'nigeria-to-ireland-work-visa-2025': 'ireland',
    
    # Netherlands Posts
    'netherlands-highly-skilled-migrant-visa-nigerians-2025': 'netherlands',
    
    # New Zealand Posts
    'new-zealand-skilled-worker-visa-nigerians-2025': 'new-zealand',
    
    # Portugal Posts
    'portugal-d7-visa-nigerians-2025': 'portugal',
    
    # UAE Posts
    'dubai-uae-work-visa-nigerians-2025': 'uae',
    
    # Healthcare Posts
    'nursing-abroad-nigerian-nurses-guide': 'healthcare',
    'nmc-cbt-osce-nigerian-nurses-guide': 'healthcare',
    'healthcare-abroad-nigerians-guide-2025': 'healthcare',
    
    # IELTS Posts
    'ielts-preparation-nigeria-complete-guide': 'ielts',
    'ielts-vs-pte-nigerians': 'ielts',
    
    # Study Abroad Posts
    'masters-abroad-nigeria-scholarships-2025': 'study',
    'statement-of-purpose-guide-nigerians-2025': 'study',
    'study-abroad-application-timeline-nigerians-2025': 'study',
    
    # Tech Posts
    'tech-jobs-abroad-nigerian-developers': 'tech',
    
    # Planning & Finance Posts
    'proof-of-funds-visa-application-nigeria': 'planning',
    'cost-of-living-abroad-nigerian-comparison': 'planning',
    'how-much-save-before-relocating-nigeria': 'planning',
    'best-cities-nigerians-abroad': 'planning',
    'common-visa-mistakes-nigerians': 'planning',
    'building-credit-score-abroad-nigerians-2025': 'planning',
    'sending-money-nigeria-abroad-2025': 'planning',
    'cultural-adjustment-nigerians-abroad-2025': 'planning',
    'visa-interview-tips-nigerians-2025': 'planning',
}


def extract_post_content(html_path):
    """Extract post data from an HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Extract title
    title_tag = soup.find('h1', class_='article__title')
    title = title_tag.get_text(strip=True) if title_tag else ''
    
    # Extract meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    excerpt = meta_desc.get('content', '') if meta_desc else ''
    
    # Extract meta keywords
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    keywords = meta_keywords.get('content', '') if meta_keywords else ''
    
    # Extract featured image
    featured_img = soup.find('img', class_='article__featured-image')
    image_url = featured_img.get('src', '') if featured_img else ''
    
    # Extract article content
    content_div = soup.find('div', class_='article__content')
    content = ''
    if content_div:
        # Get inner HTML
        content = ''.join(str(child) for child in content_div.children)
    
    # Extract read time from meta
    meta_items = soup.find_all('span', class_='article__meta-item')
    read_time = '10 min read'
    for item in meta_items:
        text = item.get_text(strip=True)
        if 'min read' in text:
            read_time = text
            break
    
    # Get filename without extension for slug
    filename = os.path.basename(html_path)
    slug = filename.replace('.html', '')
    
    return {
        'title': title,
        'slug': slug,
        'excerpt': excerpt,
        'content': content,
        'image_url': image_url,
        'read_time': read_time,
        'meta_description': excerpt,
        'meta_keywords': keywords,
    }


def seed_categories():
    """Create all categories."""
    print("Seeding categories...")
    for cat_data in CATEGORIES:
        existing = Category.query.filter_by(slug=cat_data['slug']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
            print(f"  Created category: {cat_data['name']}")
        else:
            print(f"  Category exists: {cat_data['name']}")
    db.session.commit()
    print(f"Created {len(CATEGORIES)} categories.\n")


def seed_posts(posts_dir):
    """Import posts from HTML files."""
    print("Seeding posts...")
    
    if not os.path.exists(posts_dir):
        print(f"Posts directory not found: {posts_dir}")
        return
    
    html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
    
    created_count = 0
    for html_file in html_files:
        html_path = os.path.join(posts_dir, html_file)
        
        try:
            post_data = extract_post_content(html_path)
            
            # Skip if post already exists
            existing = Post.query.filter_by(slug=post_data['slug']).first()
            if existing:
                print(f"  Post exists: {post_data['slug']}")
                continue
            
            # Determine category
            category_slug = POST_CATEGORY_MAP.get(post_data['slug'], 'planning')
            category = Category.query.filter_by(slug=category_slug).first()
            
            if not category:
                # Default to first category if not found
                category = Category.query.first()
            
            # Determine if featured (first 6 posts in UK, Canada, Germany)
            is_featured = category_slug in ['uk', 'canada', 'germany'] and created_count < 6
            
            post = Post(
                title=post_data['title'],
                slug=post_data['slug'],
                excerpt=post_data['excerpt'][:500] if post_data['excerpt'] else 'Guide for Nigerians relocating abroad.',
                content=post_data['content'] or '<p>Content coming soon.</p>',
                image_url=post_data['image_url'],
                read_time=post_data['read_time'],
                category_id=category.id,
                is_featured=is_featured,
                is_published=True,
                meta_description=post_data['meta_description'][:300] if post_data['meta_description'] else '',
                meta_keywords=post_data['meta_keywords'][:300] if post_data['meta_keywords'] else '',
                published_date=datetime.now(timezone.utc)
            )
            
            db.session.add(post)
            created_count += 1
            print(f"  Created post: {post_data['title'][:50]}...")
            
        except Exception as e:
            print(f"  Error processing {html_file}: {e}")
    
    db.session.commit()
    print(f"\nCreated {created_count} posts.")


def main():
    """Main seed function."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out to preserve data)
        # print("Clearing existing data...")
        # Post.query.delete()
        # Category.query.delete()
        # db.session.commit()
        
        # Seed categories
        seed_categories()
        
        # Seed posts from the original HTML files
        posts_dir = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'travelcleanandlegal.com', 
            'posts'
        )
        posts_dir = os.path.abspath(posts_dir)
        
        seed_posts(posts_dir)
        
        print("\nSeeding complete!")
        print(f"Categories: {Category.query.count()}")
        print(f"Posts: {Post.query.count()}")


if __name__ == '__main__':
    main()
