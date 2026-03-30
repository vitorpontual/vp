import os
import sys

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gencontent import generate_page
from src.block_markdown import markdown_to_html_node

def test_generation():
    """Testa a geração manual"""
    
    base = "/home/vpqg/Documents/myblog"
    
    # Arquivos para testar
    files = [
        ("content/index.md", "docs/index.html"),
        ("content/contact/index.md", "docs/contact/index.html"),
    ]
    
    template = os.path.join(base, "template.html")
    
    for md_file, html_file in files:
        from_path = os.path.join(base, md_file)
        dest_path = os.path.join(base, html_file)
        
        print(f"\n{'='*50}")
        print(f"Processing: {md_file}")
        print(f"File exists: {os.path.exists(from_path)}")
        
        if os.path.exists(from_path):
            # Lê o arquivo
            with open(from_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"Content length: {len(content)}")
                print(f"First 100 chars: {content[:100]}")
            
            # Gera a página
            generate_page(from_path, template, dest_path, "/")
        else:
            print(f"ERROR: File not found!")

if __name__ == "__main__":
    test_generation()
