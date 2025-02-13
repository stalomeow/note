import os

BASE_PATH = os.path.join(os.path.dirname(__file__), '../docs/obsidian-vault/attachments')
COMPRESSION_CACHE_FILEPATH = os.path.join(BASE_PATH, '.compressed')

def load_compression_cache():
    cache = set()
    try:
        with open(COMPRESSION_CACHE_FILEPATH, 'r') as fp:
            cache.update(map(str.strip, fp.readlines()))
    except FileNotFoundError:
        pass
    return cache

def save_compression_cache(cache):
    with open(COMPRESSION_CACHE_FILEPATH, 'w') as fp:
        fp.write('\n'.join(sorted(cache)))

def print_result(total_size_original, total_size_compressed):
    if total_size_original == 0 or total_size_compressed == 0:
        print('No images found')
        return

    def format_size(size):
        if size < 1024:
            return f'{size} B'
        elif size < 1024 * 1024:
            return f'{size / 1024:.2f} KB'
        elif size < 1024 * 1024 * 1024:
            return f'{size / 1024 / 1024:.2f} MB'
        else:
            return f'{size / 1024 / 1024 / 1024:.2f} GB'

    print(f'Original size: {format_size(total_size_original)}')
    print(f'Compressed size: {format_size(total_size_compressed)}')
    print(f'Saved: {(1 - total_size_compressed / total_size_original) * 100:.2f}%')

def main():
    # https://tinypng.com/developers/reference/python
    import tinify

    # API key is stored in environment variable
    tinify.key = os.environ.get('TINYPNG_API_KEY')
    print(f'API key: {tinify.key}')

    total_size_original = 0
    total_size_compressed = 0
    cache = load_compression_cache()
    files = set()

    for filename in os.listdir(BASE_PATH):
        filepath = os.path.join(BASE_PATH, filename)

        if os.path.isdir(filepath):
            continue

        if os.path.splitext(filename)[1] not in ('.png', '.jpg', '.jpeg'):
            continue

        files.add(filename)

        if filename not in cache:
            print(f'Compressing {filename}')

            total_size_original += os.path.getsize(filepath)
            tinify.from_file(filepath).to_file(filepath)
            total_size_compressed += os.path.getsize(filepath)

    cache = files # 这样可以把旧的被删除的文件从缓存中去掉
    save_compression_cache(cache)
    print_result(total_size_original, total_size_compressed)

if __name__ == '__main__':
    main()
