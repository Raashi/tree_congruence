from sys import argv

from main import main as project_main


def main():
    if len(argv) < 3:
        begin = end = int(argv[1])
    else:
        begin, end = int(argv[1]), int(argv[2])

    for i in range(begin, end + 1):
        opts = [None, '-f', f'trees\\{i}.txt', '-i', '-fn', f'trees\\{i}_diagram.png', '-it', '-tfn',
                f'trees\\{i}_tree.png']
        project_main(opts)


if __name__ == '__main__':
    main()
