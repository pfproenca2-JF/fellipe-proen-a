import os
import re
from github import Github

token = os.getenv('GITHUB_TOKEN')
g = Github(token)
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# 1. Contador
if not os.path.exists("count.txt"):
    with open("count.txt", "w") as f: f.write("0")

with open("count.txt", "r+") as f:
    count = int(f.read().strip()) + 1
    f.seek(0)
    f.write(str(count))
    f.truncate()

# 2. Mural
issues = repo.get_issues(state='open')
comments_list = []
for issue in issues:
    if "Mensagem para o Mural" in issue.title:
        comments_list.append(f"<li><b>{issue.user.login}:</b> {issue.body}</li>")

comments_html = "\n".join(comments_list[:5])

# 3. Atualização do README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Atualiza contador
content = re.sub(r'Visitante%20n%C2%BA-\d+-blue', f'Visitante%20n%C2%BA-{count}-blue', content)

# Limpa o mural antigo e coloca o novo (evita duplicatas infinitas)
marker_start = ""
marker_end = ""

if comments_html:
    new_mural = f"{marker_start}\n<ul>\n{comments_html}\n</ul>\n{marker_end}"
else:
    new_mural = f"{marker_start}\n*Ainda não há comentários. Seja o primeiro!*\n{marker_end}"

# Essa regex substitui TUDO entre os marcadores pelo novo bloco
content = re.sub(f"{marker_start}.*?{marker_end}", new_mural, content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
