import logging
import traceback

from sim import directory, argparsers, actions


def main():
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparsers.create_args_parser()
    script_args = arg_parser.parse_args()
    logging.log(level=logging.DEBUG, msg=str(script_args))

    dir_error = directory.is_valid(script_args.root)
    if dir_error is not None:
        logging.log(level=logging.ERROR, msg=dir_error.msg)
        exit(dir_error.code)

    try:
        actions.select(script_args).go().print_results()

    except AttributeError as e:
        print(e)
        traceback.print_exc()
        arg_parser.print_usage()


if __name__ == "__main__":
    main()
