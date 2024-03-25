import os
import time

POSTS_PATH = r'./docs/blog/posts'

def getCategories():
    # 获取已有的分类，只遍历顶层目录
    existingCats = [d for d in next(os.walk(POSTS_PATH))[1]]

    print('categories:')
    for i in range(len(existingCats)):
        print(f'  {i}.{existingCats[i]}')
    newCats = input('select/new: ').split(',')

    for i in range(len(newCats)):
        if newCats[i].isdigit():
            newCats[i] = existingCats[int(newCats[i])]
    return newCats

def main():
    title = input('title: ')
    slug = input('slug: ')
    categories = getCategories()
    draft = input('draft? (y/n): ').lower() == 'y'

    postFilePath = os.path.abspath(os.path.join(
        POSTS_PATH,
        categories[0] if len(categories) > 0 else '',
        slug + '.md'
    ))
    if os.path.exists(postFilePath):
        print(f'创建失败\n文件 "{postFilePath}" 已存在')
        return

    postFileDir = os.path.dirname(postFilePath)

    if not os.path.exists(postFileDir):
        os.makedirs(postFileDir)

    with open(postFilePath, 'w+', encoding='utf-8') as fp:
        fp.write(f'---\n')
        fp.write(f'date: {time.strftime("%Y-%m-%dT%H:%M:%S")}\n')
        fp.write(f'draft: {str(draft).lower()}\n')
        fp.write(f'authors:\n')
        fp.write(f'  - stalomeow\n')

        if len(categories) > 0:
            fp.write(f'categories:\n')
            for cat in categories:
                fp.write(f'  - {cat}\n')

        fp.write(f'---\n')
        fp.write(f'\n')
        fp.write(f'# {title}\n')
        fp.write(f'\n')
        fp.write(f'<!-- more -->\n')

    os.system(f'"{postFilePath}"')

if __name__ == '__main__':
    main()