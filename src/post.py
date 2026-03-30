import os
import re
from datetime import datetime

class Post:
    def __init__(self, title, date, content, slug, path):
        self.title = title
        self.date = date
        self.content = content
        self.slug = slug
        self.path = path
        self.reading_time = self.calculate_reading_time()
        self.preview = self.generate_preview()
    
    def calculate_reading_time(self):
        """Calcula o tempo estimado de leitura (200 palavras por minuto)"""
        words = len(self.content.split())
        minutes = max(1, round(words / 200))
        return minutes
    def generate_simple_preview(self, max_words=50):
        """Gera um preview simples com apenas texto puro"""
        
        content = self.content
        
        # Remove o título e data
        lines = content.split('\n')
        text_lines = []
        in_code_block = False
        
        for line in lines:
            # Pula título
            if line.startswith('# '):
                continue
            # Pula data
            if line.startswith('date: '):
                continue
            # Pula code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            
            # Adiciona texto puro
            if line.strip():
                # Remove markdown básico
                line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
                line = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', line)
                line = re.sub(r'[*_`]', '', line)
                text_lines.append(line.strip())
        
        # Junta tudo
        text = ' '.join(text_lines)
        
        # Limita por palavras
        words = text.split()
        if len(words) > max_words:
            preview = ' '.join(words[:max_words]) + '...'
        else:
            preview = text
        
        return preview
    
    def generate_preview(self, length=800, lines=12):
        """Gera um preview do conteúdo com número específico de linhas"""
        
        content = self.content
        
        # Remove título e data
        lines_content = content.split('\n')
        filtered_lines = []
        in_code_block = False
        code_block_lines = 0
        max_code_lines = 4  # Mostra até 4 linhas de código no preview
        
        for line in lines_content:
            # Pula título
            if line.startswith('# '):
                continue
            # Pula data
            if line.startswith('date: '):
                continue
            
            # Detecta início/fim de code block
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lines = 0
                    filtered_lines.append('```')
                else:
                    in_code_block = False
                    filtered_lines.append('```')
                continue
            
            # Se está dentro de um code block
            if in_code_block:
                if code_block_lines < max_code_lines:
                    filtered_lines.append(line)
                    code_block_lines += 1
                elif code_block_lines == max_code_lines:
                    filtered_lines.append('...')
                    code_block_lines += 1
                continue
            
            # Linhas normais (não código)
            line = line.strip()
            if line:
                # Remove markdown básico
                line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
                line = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', line)
                line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
                line = re.sub(r'\*([^*]+)\*', r'\1', line)
                filtered_lines.append(line)
            
            # Limita número de linhas
            if len(filtered_lines) >= lines:
                break
        
        # Junta as linhas
        text = '\n'.join(filtered_lines)
        
        # Limita por caracteres
        if len(text) > length:
            text = text[:length].rsplit(' ', 1)[0] + '...'
    
        return text 
    
    def get_formatted_date(self):
        """Retorna a data formatada (ex: 15 de Janeiro, 2024)"""
        # Mapeamento de meses para português
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        return f"{self.date.day} de {meses[self.date.month]}, {self.date.year}"
    
    def get_year(self):
        """Retorna o ano do post"""
        return self.date.year  # CORRIGIDO: year, não years

def extract_title_and_date(content):
    """Extrai título e data do conteúdo markdown"""
    lines = content.split('\n')
    title = ""
    date = None
    
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
        elif line.startswith('date: '):
            try:
                date_str = line[6:].strip()
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                pass
    
    # Se não encontrou título, usa "Untitled"
    if not title:
        title = "Untitled"
    
    # Se não encontrou data, usa a data atual
    if not date:
        date = datetime.now()
    
    return title, date

def load_posts(content_dir, blog_dir="blog"):
    """Carrega apenas os posts do diretório blog"""
    print(f"\n[DEBUG] ===== load_posts =====")
    print(f"[DEBUG] content_dir: {content_dir}")
    print(f"[DEBUG] blog_dir: {blog_dir}")
    
    # Caminho completo para o blog
    blog_path = os.path.join(content_dir, blog_dir)
    print(f"[DEBUG] blog_path: {blog_path}")
    print(f"[DEBUG] blog_path exists: {os.path.exists(blog_path)}")
    
    if not os.path.exists(blog_path):
        print(f"[DEBUG] Blog directory not found, returning empty list")
        return []
    
    # Lista todos os arquivos .md na pasta blog
    print(f"[DEBUG] Walking through: {blog_path}")
    posts = []
    
    for root, dirs, files in os.walk(blog_path):
        print(f"[DEBUG] In directory: {root}")
        print(f"[DEBUG] Files found: {files}")
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"[DEBUG] Found MD file: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    title, date = extract_title_and_date(content)
                    slug = title.lower().replace(' ', '-').replace('?', '').replace('!', '').replace(',', '')
                    
                    rel_path = os.path.relpath(file_path, blog_path)
                    path = os.path.join(blog_dir, rel_path.replace('.md', '.html'))
                    
                    print(f"[DEBUG] Adding post: {title} -> {path}")
                    posts.append(Post(title, date, content, slug, path))
                    
                except Exception as e:
                    print(f"[ERROR] Error loading {file_path}: {e}")
    
    print(f"[DEBUG] Total posts loaded: {len(posts)}")
    return posts

def group_posts_by_year(posts):
    """Agrupa posts por ano"""
    grouped = {}
    for post in posts:
        year = post.get_year()  # Agora funciona corretamente
        if year not in grouped:
            grouped[year] = []
        grouped[year].append(post)
    
    # Ordena anos decrescentes
    return dict(sorted(grouped.items(), reverse=True))
