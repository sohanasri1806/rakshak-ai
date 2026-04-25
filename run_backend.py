#!/usr/bin/env python
import sys
import os

# Try to start Flask with error reporting
try:
    print("🔍 Starting Rakshak AI Backend...")
    print("📦 Checking dependencies...")
    
    from flask import Flask
    print("✓ Flask imported")
    
    from google import generativeai
    print("✓ Google Generative AI imported (with deprecation warning - OK)")
    
    print("\n⚠️  MySQL connection may hang if database not configured.")
    print("📌 Proceeding with app initialization...\n")
    
    # Now try actual app
    from app import app
    
    print("✓ App loaded successfully!")
    print(f"\n🚀 Starting Flask server on http://0.0.0.0:5000")
    print("📱 Mobile app should connect to: http://192.168.16.81:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"\n❌ Error starting app: {type(e).__name__}")
    print(f"   {str(e)}")
    print("\n💡 Common issues:")
    print("   - MySQL server not running on localhost:3306")
    print("   - Gemini API key not set")
    print("   - Database 'rakshak_db' not created")
    print("\nTo troubleshoot, check:")
    print("   1. MySQL service status")
    print("   2. Gemini API key in app.py")
    print("   3. Database configuration")
    sys.exit(1)
