#!/usr/bin/env python3
import requests
import re
from datetime import datetime

def fetch_leetcode_stats(username):
    """Fetch real-time LeetCode stats using GraphQL API"""
    
    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"🔄 Fetching stats for {username}...")
        response = requests.post(
            'https://leetcode.com/graphql',
            json={'query': query, 'variables': {'username': username}},
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and data['data']['matchedUser']:
                ac_stats = data['data']['matchedUser']['submitStats']['acSubmissionNum']
                
                # Extract stats by difficulty
                stats = {
                    'total': 0,
                    'easy': 0,
                    'medium': 0,
                    'hard': 0
                }
                
                for item in ac_stats:
                    if item['difficulty'] == 'All':
                        stats['total'] = item['count']
                    elif item['difficulty'] == 'Easy':
                        stats['easy'] = item['count']
                    elif item['difficulty'] == 'Medium':
                        stats['medium'] = item['count']
                    elif item['difficulty'] == 'Hard':
                        stats['hard'] = item['count']
                
                print(f"✅ Stats fetched successfully!")
                print(f"   Total: {stats['total']}")
                print(f"   Easy: {stats['easy']}")
                print(f"   Medium: {stats['medium']}")
                print(f"   Hard: {stats['hard']}")
                
                return stats
            else:
                print("❌ User not found or no submission stats")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_readme(stats):
    """Update README with real stats"""
    
    if not stats:
        print("❌ Could not fetch stats, skipping update")
        return False
    
    try:
        # Read current README
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create replacement for each badge
        total_badge = f'<img src="https://img.shields.io/badge/{stats["total"]}-Solved-brightgreen?style=for-the-badge&logo=leetcode&logoColor=white" />'
        easy_badge = f'<img src="https://img.shields.io/badge/{stats["easy"]}-Easy-green?style=for-the-badge&logo=leetcode" />'
        medium_badge = f'<img src="https://img.shields.io/badge/{stats["medium"]}-Medium-orange?style=for-the-badge&logo=leetcode" />'
        hard_badge = f'<img src="https://img.shields.io/badge/{stats["hard"]}-Hard-red?style=for-the-badge&logo=leetcode" />'
        
        # Replace Loading badges with real stats
        new_content = content
        new_content = new_content.replace(
            '<img src="https://img.shields.io/badge/Loading...-Solved-brightgreen?style=for-the-badge&logo=leetcode&logoColor=white" />',
            total_badge
        )
        new_content = new_content.replace(
            '<img src="https://img.shields.io/badge/Loading...-Easy-green?style=for-the-badge&logo=leetcode" />',
            easy_badge
        )
        new_content = new_content.replace(
            '<img src="https://img.shields.io/badge/Loading...-Medium-orange?style=for-the-badge&logo=leetcode" />',
            medium_badge
        )
        new_content = new_content.replace(
            '<img src="https://img.shields.io/badge/Loading...-Hard-red?style=for-the-badge&logo=leetcode" />',
            hard_badge
        )
        
        # Update timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
        new_content = re.sub(
            r'\*\*Last Updated:\*\*.*',
            f'**Last Updated:** {timestamp}',
            new_content
        )
        
        # Write updated README
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ README updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("🔄 Updating LeetCode Stats...")
    print("=" * 50)
    
    stats = fetch_leetcode_stats('Abhishek_126')
    
    if stats:
        update_readme(stats)
    else:
        print("❌ Failed to fetch LeetCode stats")
    
    print("=" * 50)

