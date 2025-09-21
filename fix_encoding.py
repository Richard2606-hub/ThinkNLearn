def convert_to_utf8(file_path):
    # Try to detect encoding and convert to UTF-8
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Try different encodings
    encodings = ['utf-16', 'utf-16le', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            decoded = content.decode(encoding)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(decoded)
            print(f"Successfully converted {file_path} from {encoding} to UTF-8")
            return True
        except UnicodeDecodeError:
            continue
    
    print(f"Could not determine encoding for {file_path}")
    return False

# Convert .env file
convert_to_utf8('.env')