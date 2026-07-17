#!/usr/bin/env python3
import requests
import re
from datetime import datetime

def fetch_leetcode_stats(username):
    """Fetch real-time LeetCode stats using GraphQL API"""
    
    query = """
    query getUserProfile($username: String!) {
        allQuestionsCount {
            difficulty
            count
        }
        matchedUser(username: $username) {
            username
            profile {
                realName
                userAvatar
            }
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
                totalSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
        }
    }
    """
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.post(
            'https://leetcode.com/graphql',
            json={'query': query, 'variables': {'username': username}},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and data['data']['matchedUser']:
                user_data = data['data']['matchedUser']
                ac_stats = user_data['submitStats']['acSubmissionNum']
                
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
                
                return stats
        
        print(f"Error: {response.status_code}")
        return None
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_readme(stats):
    """Update README with real stats"""
    
    if not stats:
        print("Could not fetch stats")
        return
    
    # Create the new stats section
    stats_section = f"""<table>
<tr>
<td align="center"><strong>Total Solved</strong></td>
<td align="center"><strong>Easy</strong></td>
<td align="center"><strong>Medium</strong></td>
<td align="center"><strong>Hard</strong></td>
</tr>
<tr>
<td align="center">
<a href="https://leetcode.com/u/Abhishek_126/" target="_blank">
<img src="https://img.shields.io/badge/{stats['total']}-Solved-brightgreen?style=for-the-badge&logo=leetcode&logoColor=white" />
</a>
</td>
<td align="center">
<img src="https://img.shields.io/badge/{stats['easy']}-Easy-green?style=for-the-badge&logo=leetcode" />
</td>
<td align="center">
<img src="https://img.shields.io/badge/{stats['medium']}-Medium-orange?style=for-the-badge&logo=leetcode" />
</td>
<td align="center">
<img src="https://img.shields.io/badge/{stats['hard']}-Hard-red?style=for-the-badge&logo=leetcode" />
</td>
</tr>
</table>

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

**[View Full LeetCode Profile →](https://leetcode.com/u/Abhishek_126/)**"""
    
    # Read current README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the stats section (between the table markers)
    pattern = r'(<table>.*?</table>.*?\*\*\[View Full LeetCode Profile.*?\)\*\*)'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
    else:
        # If pattern not found, just return without updating
        print("Stats section pattern not found in README")
        return
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated README with real stats:")
    print(f"   Total: {stats['total']}")
    print(f"   Easy: {stats['easy']}")
    print(f"   Medium: {stats['medium']}")
    print(f"   Hard: {stats['hard']}")

if __name__ == '__main__':
    print("🔄 Fetching real-time LeetCode stats...")
    stats = fetch_leetcode_stats('Abhishek_126')
    
    if stats:
        update_readme(stats)
    else:
        print("❌ Failed to fetch LeetCode stats")
