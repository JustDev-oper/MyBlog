#!/usr/bin/env python
"""Initialize the database with all tables."""
import os
import sys

from app import app, db
from app.models import User, Post, Like, FeaturedPosts

def init_database():
    """Create all database tables."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")

if __name__ == '__main__':
    init_database()

