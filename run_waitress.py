"""
Production server using Waitress (works on Windows, Linux, Mac)
"""
from waitress import serve
from wsgi import app
import os

if __name__ == '__main__':
    # Configuration for high concurrency
    print("="*60)
    print("QuizFlow Production Server (Waitress)")
    print("="*60)
    print("Server: Waitress")
    print("Host: 0.0.0.0:5000")
    print("Threads: 8")
    print("Max concurrent students: ~100")
    print("="*60)
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'development'
    
    serve(
        app,
        host='0.0.0.0',
        port=5000,
        threads=8,              # 8 threads for ~100 concurrent users
        channel_timeout=120,     # 2 minutes timeout
        connection_limit=200,    # Max 200 connections
        cleanup_interval=10,     # Cleanup every 10 seconds
        asyncore_use_poll=True   # Better performance on Windows
    )