import argparse
import os
import time

def getArgParser():
    parser = argparse.ArgumentParser(
        prog='blog',
        description='Blog Helper',
        add_help=True,
    )
    subparsers = parser.add_subparsers(title='commands', required=True)

    postParser = subparsers.add_parser('post',
        help='Create a new post',
        description='Create a new post',
    )
    postParser.add_argument('postSlug',
        metavar='<slug>',
        help='The slug of the post',
    )
    postParser.add_argument('postTitle',
        nargs='?',
        metavar='<title>',
        default='',
        help='The title of the post',
    )
    postParser.add_argument('-c', '--categories',
        nargs='*',
        dest='postCategories',
        metavar='<category>',
        default=[],
        help='The categories of the post',
    )
    postParser.add_argument('--draft',
        dest='postDraft',
        action='store_true',
        help='Mark the post as draft',
    )

    return parser

def main():
    parser = getArgParser()
    args = parser.parse_args()

    postFilePath = os.path.abspath(os.path.join(
        './docs/blog/posts',
        args.postCategories[0] if len(args.postCategories) > 0 else '',
        args.postSlug + '.md'
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
        fp.write(f'draft: {str(args.postDraft).lower()}\n')
        fp.write(f'authors:\n')
        fp.write(f'  - stalomeow\n')

        if len(args.postCategories) > 0:
            fp.write(f'categories:\n')
            for cat in args.postCategories:
                fp.write(f'  - {cat}\n')

        fp.write(f'---\n')
        fp.write(f'\n')
        fp.write(f'# {args.postTitle}\n')
        fp.write(f'\n')
        fp.write(f'<!-- more -->\n')

    os.system(f'"{postFilePath}"')

if __name__ == '__main__':
    main()