#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_github_user_stats(username):
    """Fetch real GitHub user statistics"""
    url = f"https://api.github.com/users/{username}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'followers': data.get('followers', 0),
                'public_repos': data.get('public_repos', 0),
                'public_gists': data.get('public_gists', 0),
                'bio': data.get('bio', ''),
                'location': data.get('location', ''),
            }
    except Exception as e:
        print(f"Error fetching user stats: {e}")
    return None

def fetch_top_repositories(username, limit=6):
    """Fetch user's top repositories by stars"""
    url = f"https://api.github.com/users/{username}/repos?sort=stars&direction=desc&per_page={limit}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            repos = response.json()
            return [
                {
                    'name': repo['name'],
                    'url': repo['html_url'],
                    'description': repo['description'] or 'No description',
                    'stars': repo['stargazers_count'],
                    'language': repo['language'] or 'Unknown',
                    'topics': repo.get('topics', [])
                }
                for repo in repos
            ]
    except Exception as e:
        print(f"Error fetching repositories: {e}")
    return []

def generate_projects_markdown(repos):
    """Generate markdown for projects"""
    markdown = "## 🚀 **Featured Projects**\n\n<div align=\"center\">\n\n"
    
    for i, repo in enumerate(repos, 1):
        stars_badge = f"[![Stars](https://img.shields.io/github/stars/{repo['name']}?style=flat-square&logo=github&label=Stars&color=00BFFF)]({repo['url']})"
        topics_str = " • ".join(repo['topics'][:3]) if repo['topics'] else repo['language']
        
        markdown += f"""### {i}. **{repo['name'].replace('-', ' ').title()}**
**[Repository]({repo['url']})** | **[Open Repository]({repo['url']}/blob/main/README.md)**

> {repo['description']}

**Tech Stack:** {topics_str}

{stars_badge}

---

"""
    
    markdown += "</div>\n\n"
    return markdown

def update_readme_with_real_data(username):
    """Update README with real GitHub data"""
    
    print(f"🔄 Fetching real data for {username}...")
    
    # Fetch data
    user_stats = fetch_github_user_stats(username)
    repos = fetch_top_repositories(username, 6)
    
    if not user_stats or not repos:
        print("❌ Failed to fetch GitHub data")
        return False
    
    # Read current README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update profile metrics
    content = content.replace(
        'REPOSITORIES-30+',
        f'REPOSITORIES-{user_stats["public_repos"]}+'
    )
    
    # Generate and insert projects section
    projects_markdown = generate_projects_markdown(repos)
    
    # Find and replace projects section
    import re
    pattern = r'(## 🚀 \*\*Featured Projects\*\*.*?)(---|\Z)'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(
            pattern,
            projects_markdown + '\n<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00BFFF,100:0D1117&height=2"/>\n\n---',
            content,
            flags=re.DOTALL
        )
    else:
        new_content = content
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated README with real GitHub data:")
    print(f"   Repositories: {user_stats['public_repos']}")
    print(f"   Top Projects: {len(repos)}")
    print(f"   Followers: {user_stats['followers']}")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("🔄 Updating Profile with Real GitHub Data...")
    print("=" * 60)
    
    if update_readme_with_real_data('Abhishek-18bit'):
        print("✅ Success! README updated with real data")
    else:
        print("❌ Failed to update README")
    
    print("=" * 60)
