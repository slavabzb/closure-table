from argparse import ArgumentParser


def apply_migrates(args):
    print('migrate')


def make_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    migrate = subparsers.add_parser('migrate')
    migrate.set_defaults(func=apply_migrates)

    return parser


if __name__ == '__main__':
    parser = make_parser()

    args = parser.parse_args()

    if vars(args):
        args.func(args)
    else:
        parser.print_help()
