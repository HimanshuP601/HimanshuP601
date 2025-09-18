import os

username = "HimanshuP601"
num_articles = 5  # latest 5 articles

# Generate markdown for latest 5 articles
markdown_snippet = ""
for i in range(num_articles):
    url = f"https://github-readme-medium-recent-article.vercel.app/medium/@{username}/{i}"
    markdown_snippet += f'''
<a target="_blank" href="{url}">
  <img src="{url}" alt="Medium Article {i+1}">
</a>
'''

# Read existing README
with open("README.md", "r") as f:
    content = f.read()

# Replace content between markers
start_marker = "<!-- MEDIUM-START -->"
end_marker = "<!-- MEDIUM-END -->"
if start_marker in content and end_marker in content:
    new_content = content.split(start_marker)[0] + start_marker + "\n" + markdown_snippet + "\n" + end_marker + content.split(end_marker)[1]

    # Write updated README
    with open("README.md", "w") as f:
        f.write(new_content)
    print("README.md updated successfully!")
else:
    print("Markers not found in README.md")
