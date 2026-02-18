#!/usr/bin/env python3
"""
Flask backend for Spotify API integration
Handles token acquisition and API proxying to avoid CORS issues
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import base64
import time
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Spotify API credentials
CLIENT_ID = '44dd5c1f9fa4405c92e27a9fa236e124'
CLIENT_SECRET = '85ab203ffe05451c8e81cc66e3ef1087'

# Token cache
token_cache = {
    'access_token': None,
    'expires_at': 0
}

def get_spotify_token():
    """Get or refresh Spotify access token"""
    current_time = time.time()
    
    # Return cached token if still valid (with 5 minute buffer)
    if token_cache['access_token'] and current_time < (token_cache['expires_at'] - 300):
        return token_cache['access_token']
    
    # Request new token
    auth_string = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {'grant_type': 'client_credentials'}
    
    try:
        response = requests.post('https://accounts.spotify.com/api/token', 
                               headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        
        # Cache the token
        token_cache['access_token'] = token_data['access_token']
        token_cache['expires_at'] = current_time + token_data['expires_in']
        
        return token_data['access_token']
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting Spotify token: {e}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'music-wrapper.html')

@app.route('/music-chart.html')
def chart():
    """Serve the chart page"""
    return send_from_directory('.', 'music-chart.html')

@app.route('/api/spotify/token', methods=['GET'])
def get_token():
    """Get Spotify access token"""
    token = get_spotify_token()
    if token:
        return jsonify({'access_token': token, 'status': 'success'})
    else:
        return jsonify({'error': 'Failed to get token', 'status': 'error'}), 500

@app.route('/api/spotify/track/<track_id>', methods=['GET'])
def get_track(track_id):
    """Get track information from Spotify API"""
    token = get_spotify_token()
    if not token:
        return jsonify({'error': 'No access token available', 'status': 'error'}), 500
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', 
                              headers=headers)
        response.raise_for_status()
        
        track_data = response.json()
        
        # Return relevant track information
        return jsonify({
            'status': 'success',
            'id': track_data['id'],
            'name': track_data['name'],
            'artists': [artist['name'] for artist in track_data['artists']],
            'preview_url': track_data.get('preview_url'),
            'external_urls': track_data['external_urls']
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch track: {str(e)}', 'status': 'error'}), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test endpoint to verify backend is working"""
    return jsonify({
        'status': 'success',
        'message': 'Spotify backend is running!',
        'timestamp': time.time()
    })

@app.route('/debug')
def debug():
    """Debug endpoint to check token status"""
    token = get_spotify_token()
    return jsonify({
        'has_token': token is not None,
        'token_preview': token[:20] + '...' if token else None,
        'expires_at': token_cache['expires_at'],
        'current_time': time.time(),
        'time_until_expiry': token_cache['expires_at'] - time.time() if token else None
    })

if __name__ == '__main__':
    print("🎵 Starting Spotify Backend Server...")
    print("📍 Server will run on http://localhost:5001")
    print("🎯 Main app: http://localhost:5001/")
    print("🧪 Test endpoint: http://localhost:5001/api/test")
    print("🐛 Debug endpoint: http://localhost:5001/debug")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
