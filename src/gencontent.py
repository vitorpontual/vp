from  block_markdown import markdown_to_html_node
import os

from post import group_posts_by_year, load_posts

def generate_page(from_path, template_path, dest_path, basepath, title=None):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r', encoding="utf-8") as f:
        md_content = f.read()

    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()
    
    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()

    if title is None:
       title = extract_title(md_content)
       if not title:
           title = "VP Developer Blog"

    print(title)


    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath) 

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f'Page generated successfully at {dest_path}')

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:]
    return None 

"""def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
                generate_page(from_path, dest_path, template_path, basepath)

        else:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(from_path, template_path, dest_path,basepath)"""

def generate_all_posts_html(posts, basepath="/"):
    """Gera HTML para todos os posts com preview simples"""
    html = ""
    for post in posts:
        # Preview simples: apenas título, data e primeiras palavras
        preview_text = post.generate_simple_preview()
        
        html += f'''
        <article class="post-item">
            <h2 class="post-title">
                <a href="{basepath}{post.path}">{post.title}</a>
            </h2>
            <div class="post-meta">
                <span class="post-date">
                   {post.get_formatted_date()}
                </span>
                <span class="reading-time">
                  {post.reading_time} min de leitura
                </span>
            </div>
            <p class="post-excerpt">
                {preview_text}
            </p>
            <a href="{basepath}{post.path}" class="read-more">
                Leia mais →
            </a>
        </article>
        '''
    return html


            
def generate_index_page(posts, template_path, dest_path, basepath):
    """Gera a página inicial com preview simples"""
    
    # Gera HTML para todos os posts
    all_posts_html = generate_all_posts_html(posts, basepath)
    
    # Conteúdo HTML simples
    content = f'''
    <section class="container">
        <img class="home-img" src="/images/book.jpg" alt="Livro">
        <p>Bem-vindo ao meu blog! Compartilhando conhecimento sobre programação e tecnologia.</p>
    </section>
    
    <section class="posts">
        <div class="posts-list">
            {all_posts_html}
        </div>
    </section>
    '''
    
    # Lê o template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Substitui placeholders
    final_html = template.replace("{{ Title }}", "VP Developer - Início")
    final_html = final_html.replace("{{ Content }}", content)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Escreve o arquivo HTML
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Generated index page with {len(posts)} posts at {dest_path}")



def generate_archive_page(posts, template_path, dest_path, basepath):
    """Gera a página de arquivo com links para cada ano"""
    
    # Agrupa posts por ano
    grouped_posts = group_posts_by_year(posts)
    
    # Gera HTML com links para cada ano
    archive_html = '<div class="archive-container">\n'
    
    for year, year_posts in grouped_posts.items():
        post_count = len(year_posts)
        
        archive_html += f'''
        <div>
        <a href="{basepath}blog/{year}/" class="year-card">
            <div class="year-card-content">
                <span class="year-number">{year}</span>
                <span class="year-post-count">
                   {post_count} [post{"s" if post_count != 1 else ""}]
                </span>
            
            </div>
        </a>
        </div>
        '''
    

    
    # Lê o template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Substitui placeholders
    final_html = template.replace("{{ Title }}", "Archive")
    final_html = final_html.replace("{{ Content }}", archive_html)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Escreve o arquivo HTML
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Generated archive page with {len(grouped_posts)} years at {dest_path}")

def generate_year_page_content(posts, year, basepath):
    """Gera o conteúdo HTML para a página de um ano específico"""
    
    posts_html = ""
    
    for post in posts:
        # Gera preview simples
        preview_text = post.generate_simple_preview(max_words=50)
        
        posts_html += f'''
        <article class="year-post-item">
            <div class="year-post-header">
                <h2 class="year-post-title">
                    <a href="{basepath}{post.path}">{post.title}</a>
                </h2>
                <div class="post-meta">
                    <span class="year-post-date">
                        {post.get_formatted_date()}
                    </span>
                    <span class="year-reading-time">
                        {post.reading_time} min de leitura
                    </span>
                </div>
            </div>
            <p class="year-post-excerpt">
                {preview_text}
            </p>
            <a href="{basepath}{post.path}" class="year-read-more">
                Leia mais 
            </a>
        </article>
        '''
    
    content = f'''
    <section class="year-hero">
        <h1>Arquivo: {year}</h1>
        <p>{len(posts)} post{"s" if len(posts) != 1 else ""} publicados em {year}</p>
        <a href="{basepath}archive.html" class="back-to-archive">
             Voltar para o arquivo completo
        </a>
    </section>
    
    <div class="year-posts-list">
        {posts_html}
    </div>
    
    <div class="year-footer">
        <a href="{basepath}" class="back-to-home">
             Voltar para o início
        </a>
    </div>
    '''
    
    return content

def generate_year_pages(posts, template_path, dest_dir_path, basepath):
    """Gera páginas para cada ano com os posts daquele ano"""
    
    # Agrupa posts por ano
    grouped_posts = group_posts_by_year(posts)
    
    for year, year_posts in grouped_posts.items():
        # Caminho da página do ano
        year_path = os.path.join(dest_dir_path, "blog", str(year), "index.html")
        
        # Gera o conteúdo da página do ano
        year_html = generate_year_page_content(year_posts, year, basepath)
        
        # Lê o template
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Substitui placeholders
        final_html = template.replace("{{ Title }}", f"Arquivo - {year}")
        final_html = final_html.replace("{{ Content }}", year_html)
        final_html = final_html.replace('href="/', f'href="{basepath}')
        final_html = final_html.replace('src="/', f'src="{basepath}')
        
        # Garante que o diretório existe
        os.makedirs(os.path.dirname(year_path), exist_ok=True)
        
        # Escreve o arquivo HTML
        with open(year_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"Generated year page for {year} at {year_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Processa recursivamente todos os arquivos .md e gera páginas"""
    
    print(f"\n===== Starting page generation =====")
    print(f"Content directory: {dir_path_content}")
    print(f"Content exists: {os.path.exists(dir_path_content)}")
    
    if not os.path.exists(dir_path_content):
        print(f"ERROR: Content directory not found!")
        return
    
    # Primeiro, lista TODOS os arquivos .md encontrados
    print(f"\n--- Scanning for all .md files ---")
    all_md_files = []
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dir_path_content)
                all_md_files.append(rel_path)
                print(f"Found: {rel_path}")
    
    if not all_md_files:
        print("ERROR: No .md files found!")
        return
    
    # Carrega posts (apenas da pasta blog, se existir)
    posts = []
    blog_path = os.path.join(dir_path_content, "blog")
    if os.path.exists(blog_path):
        posts = load_posts(dir_path_content, "blog")
        print(f"\nLoaded {len(posts)} blog posts")
    else:
        print(f"\nNo blog directory found at {blog_path}")
    
    # Gera página inicial (index)
    generate_index_page(posts, template_path, os.path.join(dest_dir_path, 'index.html'), basepath)
    
    # Gera página de arquivo (archive)
    print(f"\n--- Generating archive page ---")
    generate_archive_page(posts, template_path, os.path.join(dest_dir_path, 'archive.html'), basepath)

    generate_year_pages(posts, template_path, dest_dir_path, basepath)
    
    # Gera TODAS as páginas
    print(f"\n--- Generating all pages ---")
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_path.replace('.md', '.html'))
                
                print(f"\nProcessing: {rel_path}")
                print(f"  From: {from_path}")
                print(f"  To: {dest_path}")
                
                # Garante que o diretório de destino existe
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Gera a página
                generate_page(from_path,template_path,dest_path, basepath)
    
    print(f"\n===== Generation complete =====")
