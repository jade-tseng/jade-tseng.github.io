#!/usr/bin/env python3
"""
Find Spotify track IDs that have preview URLs available
"""

import requests
import base64
import json

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

def search_artist_tracks(artist_name, token):
    """Search for tracks by an artist and return ones with previews"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Search for the artist
    search_url = f'https://api.spotify.com/v1/search?q=artist:{artist_name}&type=track&limit=50'
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    
    tracks = response.json()['tracks']['items']
    
    # Find tracks with preview URLs
    preview_tracks = []
    for track in tracks:
        if track['preview_url']:
            preview_tracks.append({
                'name': track['name'],
                'id': track['id'],
                'artist': track['artists'][0]['name'],
                'preview_url': track['preview_url']
            })
    
    return preview_tracks

def main():
    print("🔍 Finding Spotify tracks with preview URLs...")
    
    try:
        token = get_spotify_token()
        print("✅ Got Spotify token")
        
        # Artists from our chart
        artists = [
            "Bad Bunny",
            "The Weeknd", 
            "Drake",
            "Taylor Swift",
            "Post Malone",
            "Ed Sheeran",
            "Ariana Grande",
            "Olivia Rodrigo",
            "Eminem"
        ]
        
        results = {}
        
        for artist in artists:
            print(f"\n🎵 Searching for {artist} tracks with previews...")
            try:
                preview_tracks = search_artist_tracks(artist, token)
                if preview_tracks:
                    # Get the most popular track with preview
                    best_track = preview_tracks[0]
                    results[artist] = best_track
                    print(f"✅ Found: {best_track['name']} (ID: {best_track['id']})")
                else:
                    print(f"❌ No preview tracks found for {artist}")
            except Exception as e:
                print(f"❌ Error searching {artist}: {e}")
        
        # Print results in format for easy copy-paste
        print("\n" + "="*60)
        print("🎯 TRACK IDs WITH PREVIEW URLs:")
        print("="*60)
        
        for artist, track in results.items():
            print(f"{artist}: {track['id']} ({track['name']})")
        
        print("\n" + "="*60)
        print("📋 COPY-PASTE FORMAT FOR music-chart.html:")
        print("="*60)
        
        for artist, track in results.items():
            print(f'// {artist}: "{track["id"]}" - {track["name"]}')
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
