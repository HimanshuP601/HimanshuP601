import requests

username = "HimanshuP601"
max_articles = 5  # number of articles to show if >= 5
markdown_snippet = ""

available_articles = []

# Check which articles exist
for i in range(20):  # check up to 20 latest articles
    url = f"https://github-readme-medium-recent-article.vercel.app/medium/@{username}/{i}"
    response = requests.get(url)
    if response.status_code == 200:
        available_articles.append(url)
    else:
        break  # stop at first non-existent article

# Determine how many to show
if len(available_articles) >= max_articles:
    articles_to_show = available_articles[:max_articles]
else:
    articles_to_show = available_articles  # show whatever exists

# Generate markdown
for url in articles_to_show:
    markdown_snippet += f'''
<a target="_blank" href="{url}">
  <img src="{url}" alt="Medium Article">
</a>
'''

# Update README
with open("README.md", "r") as f:
    content = f.read()

start_marker = "<!-- MEDIUM-START -->"
end_marker = "<!-- MEDIUM-END -->"

if start_marker in content and end_marker in content:
    new_content = content.split(start_marker)[0] + start_marker + "\n" + markdown_snippet + "\n" + end_marker + content.split(end_marker)[1]
    with open("README.md", "w") as f:
        f.write(new_content)
    print(f"README.md updated successfully! Showing {len(articles_to_show)} article(s).")
else:
    print("Markers not found in README.md")
