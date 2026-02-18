#!/usr/bin/env python3
"""
Test well-known Spotify track IDs to find ones with preview URLs
"""

import requests
import base64

# Spotify API credentials
CLIENT_ID = '44dd5c1f9fa4405c92e27a9fa236e124'
CLIENT_SECRET = '85ab203ffe05451c8e81cc66e3ef1087'

def get_spotify_token():
    """Get Spotify access token"""
    auth_string = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {'grant_type': 'client_credentials'}
    
    response = requests.post('https://accounts.spotify.com/api/token', 
                           headers=headers, data=data)
    response.raise_for_status()
    
    return response.json()['access_token']

def test_track(track_id, token, description=""):
    """Test a specific track ID"""
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
        
        if response.status_code == 404:
            print(f"❌ {description}: Track not found (404)")
            return None
        
        response.raise_for_status()
        track_data = response.json()
        
        has_preview = track_data.get('preview_url') is not None
        status = "✅ HAS PREVIEW" if has_preview else "❌ No preview"
        
        print(f"{status} {description}: {track_data['name']} by {track_data['artists'][0]['name']}")
        
        if has_preview:
            return {
                'id': track_id,
                'name': track_data['name'],
                'artist': track_data['artists'][0]['name'],
                'preview_url': track_data['preview_url']
            }
        
        return None
        
    except Exception as e:
        print(f"❌ {description}: Error - {e}")
        return None

def main():
    print("🔍 Testing known Spotify track IDs for preview URLs...")
    
    try:
        token = get_spotify_token()
        print("✅ Got Spotify token\n")
        
        # Well-known track IDs that are more likely to have previews
        test_tracks = [
            # Current tracks from our chart
            ("6Sq7ltF9Qa7SNqBwlj0tbn", "Bad Bunny - Current"),
            ("0VjIjW4GlULA6L5Ym3OwlG", "The Weeknd - Current"),
            ("1zi7xx7UVEFkmKfv06H8x0", "Drake - Current"),
            ("1BxfuPKGuaTgP7aM0Bbdwr", "Taylor Swift - Current"),
            ("0RiRZpuVRbi7oqRdSMwhQY", "Post Malone - Current"),
            ("7qiZfU4dY1lWllzX7mPBI3", "Ed Sheeran - Current"),
            ("6ocbgoVGwYJhOv1GgI9NsF", "Ariana Grande - Current"),
            ("4uLU6hMCjMI75M1A2tKUQC", "MUSIC LAB JPN - Current"),
            ("5wANPM4fQCJwkGd4rN57mH", "Olivia Rodrigo - Current"),
            ("7w9bgPAmPTtrkt2v16QWvQ", "Eminem - Current"),
            
            # Some popular tracks that often have previews
            ("4iV5W9uYEdYUVa79Axb7Rh", "Never Gonna Give You Up - Rick Astley"),
            ("0VjIjW4GlULA6L5Ym3OwlG", "Blinding Lights - The Weeknd"),
            ("7qiZfU4dY1lWllzX7mPBI3", "Shape of You - Ed Sheeran"),
            ("6habFhsOp2NvshLv26DqMb", "Someone Like You - Adele"),
            ("1mea3bSkSGXuIRvnydlB5b", "Bohemian Rhapsody - Queen"),
        ]
        
        working_tracks = []
        
        for track_id, description in test_tracks:
            result = test_track(track_id, token, description)
            if result:
                working_tracks.append(result)
        
        print("\n" + "="*60)
        print("🎯 TRACKS WITH WORKING PREVIEW URLs:")
        print("="*60)
        
        if working_tracks:
            for track in working_tracks:
                print(f"✅ {track['artist']} - {track['name']}")
                print(f"   ID: {track['id']}")
                print(f"   Preview: {track['preview_url'][:50]}...")
                print()
        else:
            print("❌ No tracks with preview URLs found!")
            print("\n💡 This might be due to:")
            print("   - Regional restrictions")
            print("   - Spotify API limitations")
            print("   - Account type restrictions")
            print("   - Temporary API issues")
        
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
