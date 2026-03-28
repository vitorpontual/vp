import os 

def copy_files(src_path, dest_path):
    with open(src_path, "rb", encoding="utf-8") as f:
        content = f.read()
        with open(dest_path, "wb", encoding="utf-8") as dest_f: 
            dest_f.write(content)
        print(f"Copy: {src_path} -> {dest_path}")

def copy_static(src_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    items = os.listdir(src_path)

    for item in items:
        from_path = os.path.join(src_path, item)
        to_path = os.path.join(dest_path, item)

        if os.path.isfile(from_path):
            copy_files(from_path, to_path)
        elif os.path.isdir(from_path):
            if not os.path.exists(dest_path):
                os.mkdir(to_path)
            copy_static(from_path, to_path)

