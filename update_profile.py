import os
import re
from github import Github

# Conexão
token = os.getenv('GITHUB_TOKEN')
g = Github(token)
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# 1. Contador (Sempre +1 por execução)
if not os.path.exists("count.txt"):
    with open("count.txt", "w") as f: f.write("0")

with open("count.txt", "r+") as f:
    val = f.read().strip()
    count = int(val) + 1 if val.isdigit() else 1
    f.seek(0)
    f.write(str(count))
    f.truncate()

# 2. Mural de Recados
issues = repo.get_issues(state='open')
msgs = [f"<li><b>{i.user.login}:</b> {i.body}</li>" for i in issues if "Mensagem para o Mural" in i.title]
mural_content = "<ul>" + "\n".join(msgs[:5]) + "</ul>" if msgs else "*Ainda não há comentários. Seja o primeiro!*"

# 3. A Cirurgia no README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Atualiza o Badge do Contador
readme = re.sub(r'Visitante%20n%C2%BA-\d+-blue', f'Visitante%20n%C2%BA-{count}-blue', readme)

# LOCALIZA E SUBSTITUI TUDO ENTRE AS TAGS (A mágica está aqui)
start_tag = ""
end_tag = ""

# Se as tags existirem, a regex abaixo vai limpar TUDO entre elas e colocar o conteúdo novo
pattern = f"{re.escape(start_tag)}.*?{re.escape(end_tag)}"
replacement = f"{start_tag}\n{mural_content}\n{end_tag}"

if re.search(pattern, readme, re.DOTALL):
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
else:
    # Caso as tags tenham sido corrompidas, ele apenas anexa ao fim para não perder o arquivo
    new_readme = readme + f"\n\n{replacement}"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)
    
