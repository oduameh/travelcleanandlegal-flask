# Travel Clean & Legal - Flask Application

A Flask-based website for Nigerian emigration guides. Built with Flask, SQLAlchemy, and Flask-Admin.

## Features

- **Dynamic Blog System**: Posts stored in SQLite database with categories
- **Admin Panel**: Full content management at `/admin`
- **Responsive Design**: Mobile-friendly layout using the original CSS
- **SEO Optimized**: Meta tags, Open Graph, and JSON-LD structured data
- **Google AdSense Ready**: ads.txt, robots.txt, and sitemap.xml properly configured

## Quick Start

### 1. Create Virtual Environment

```bash
cd travelcleanandlegal.com-flask
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Seed the Database

Import all existing blog posts from the original HTML files:

```bash
python seed_data.py
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Important URLs

- **Home**: `http://localhost:5000/`
- **Admin Panel**: `http://localhost:5000/admin`
- **ads.txt**: `http://localhost:5000/ads.txt` (Google AdSense verification)
- **robots.txt**: `http://localhost:5000/robots.txt`
- **Sitemap**: `http://localhost:5000/sitemap.xml`

## Admin Panel

Access the admin panel at `http://localhost:5000/admin` to:

- Add/Edit/Delete categories
- Add/Edit/Delete blog posts
- Use the rich text editor (CKEditor) for post content

## Project Structure

```
travelcleanandlegal.com-flask/
├── app.py              # Main Flask application
├── wsgi.py             # WSGI entry point for production
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── seed_data.py        # Database seeding script
├── .env.example        # Environment variables template
├── static/
│   ├── ads.txt         # Google AdSense verification
│   ├── robots.txt      # Search engine directives
│   ├── css/
│   │   └── styles.css  # Site styles
│   └── images/
│       └── favicon.svg # Site favicon
├── templates/
│   ├── admin/          # Admin panel templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── blog.html       # Blog listing
│   ├── post.html       # Individual post
│   ├── about.html      # About page
│   ├── contact.html    # Contact page
│   ├── privacy.html    # Privacy policy
│   ├── terms.html      # Terms of service
│   ├── 404.html        # Not found page
│   └── 500.html        # Server error page
└── instance/
    └── site.db         # SQLite database (auto-created)
```

## Configuration

Environment variables (set in `.env` or system environment):

- `SECRET_KEY`: Secret key for session management (required for production)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SITE_URL`: Production URL

Edit `config.py` to customize:

- `SITE_NAME`: Website name
- `CONTACT_EMAIL`: Contact email address
- `ADSENSE_CLIENT_ID`: Google AdSense publisher ID

## Production Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn wsgi:app -b 0.0.0.0:8000 -w 4
```

### Using Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8000", "-w", "4"]
```

### Production Checklist

- [ ] Set `SECRET_KEY` via environment variable (generate secure random string)
- [ ] Use PostgreSQL for high traffic (`DATABASE_URL=postgresql://...`)
- [ ] Configure reverse proxy (Nginx/Caddy)
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Set up monitoring and logging
- [ ] Configure backup for database

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name travelcleanandlegal.live;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

## Google AdSense Setup

The ads.txt file is automatically served at `/ads.txt`. After deployment:

1. Visit `https://yourdomain.com/ads.txt` to verify it's accessible
2. In Google AdSense, click "Check again" to verify
3. Allow 24-48 hours for Google to recognize the file

## License

All rights reserved. Travel Clean & Legal.
