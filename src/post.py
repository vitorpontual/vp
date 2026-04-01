import os
import re
from datetime import datetime

class Post:
    def __init__(self, title, date, content, slug, path, tags=None, published_date=None):
        self.title = title
        # Garante que date é um objeto datetime
        if isinstance(date, str):
            try:
                self.date = datetime.strptime(date, "%Y-%m-%d")
            except:
                self.date = datetime.now()
        else:
            self.date = date
            
        self.content = content
        self.slug = slug
        self.path = path
        self.tags = tags if tags else []
        
        # Data de publicação (usa a mesma data se não especificada)
        if published_date:
            if isinstance(published_date, str):
                try:
                    self.published_date = datetime.strptime(published_date, "%Y-%m-%d")
                except:
                    self.published_date = self.date
            else:
                self.published_date = published_date
        else:
            self.published_date = self.date
        
        self.reading_time = self.calculate_reading_time()
        self.preview = self.generate_preview()
    
    def get_formatted_date(self):
        """Retorna a data formatada (fixa)"""
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        # Usa published_date em vez de date para consistência
        return f"{self.published_date.day} de {meses[self.published_date.month]}, {self.published_date.year}"
    
    def get_formatted_date_short(self):
        """Retorna a data no formato curto (DD/MM/YYYY)"""
        return self.published_date.strftime("%d/%m/%Y")
    
    def get_year(self):
        """Retorna o ano do post"""
        return self.published_date.year
    
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
    
 

def extract_title_and_date(content):
    """Extrai título, data e tags do conteúdo markdown"""
    lines = content.split('\n')
    title = ""
    date = None
    tags = []
    published_date = None
    
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
        elif line.startswith('date: '):
            try:
                date_str = line[6:].strip()
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                pass
        elif line.startswith('published: '):
            try:
                published_str = line[10:].strip()
                published_date = datetime.strptime(published_str, "%Y-%m-%d")
            except:
                pass
        elif line.startswith('tags: '):
            tags_str = line[6:].strip()
            tags = [tag.strip().lower() for tag in tags_str.split(',')]
    
    # Se não encontrou título, usa "Untitled"
    if not title:
        title = "Untitled"
    
    # Se não encontrou data, usa None (será tratado depois)
    if not date:
        date = None
    
    # Se não encontrou data de publicação, usa a data de criação
    if not published_date:
        published_date = date
    
    return title, date, published_date, tags

def load_posts(content_dir, blog_dir="blog"):
    """Carrega apenas os posts do diretório blog"""
    posts = []
    blog_path = os.path.join(content_dir, blog_dir)
    
    if not os.path.exists(blog_path):
        print(f"[WARNING] Blog directory not found: {blog_path}")
        return posts
    
    for root, dirs, files in os.walk(blog_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extrai título, data e tags
                    title, date, published_date, tags = extract_title_and_date(content)
                    
                    # Se não tem data, usa a data de modificação do arquivo
                    if not date:
                        # Pega a data de modificação do arquivo
                        stat = os.stat(file_path)
                        date = datetime.fromtimestamp(stat.st_mtime)
                    
                    if not published_date:
                        published_date = date
                    
                    # Cria slug
                    slug = title.lower().replace(' ', '-').replace('?', '').replace('!', '').replace(',', '')
                    
                    # Caminho relativo
                    rel_path = os.path.relpath(file_path, blog_path)
                    path = os.path.join(blog_dir, rel_path.replace('.md', '.html'))
                    
                    # Cria o post
                    posts.append(Post(title, date, content, slug, path, tags, published_date))
                    
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
    
    # Ordena por data de publicação (mais recente primeiro)
    posts.sort(key=lambda x: x.published_date, reverse=True)
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
