from flask import Response
from . import bp


@bp.route('/robots.txt')
def robots():
    """
    Since all content requires authentication, I disallow everything
    except public pages (login, register).
    """
    content = """User-agent: *
Disallow: /
Allow: /login
Allow: /register
Crawl-delay: 30
"""
    return Response(content, mimetype='text/plain')