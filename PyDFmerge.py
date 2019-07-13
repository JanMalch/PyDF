import glob
import os
import sys

from PyPDF2 import PdfFileMerger
from datetime import datetime
from colorama import init, Fore, Style


def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses


def merge_files(file_list, file_name):
    merger = PdfFileMerger()

    for pdf in file_list:
        merger.append(open(pdf, 'rb'))

    with open(file_name, 'wb') as fout:
        merger.write(fout)
        path = os.path.abspath(fout.name)
    return path


def resolve_dir(base_dir):
    pathname = os.path.join(base_dir, '**', '*.pdf')
    return glob.glob(pathname, recursive=True)


def resolve_inputs(inputs):
    files, dirs = partition(lambda i: os.path.isfile(i), inputs)
    for folder in dirs:
        resolved = resolve_dir(folder)
        files.extend(resolved)
    return files


def get_result_file_name(first_input):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if os.path.isfile(first_input):
        prefix = os.path.dirname(os.path.realpath(first_input))
    else:  # isdir
        prefix = first_input
    default_file_name = os.path.join(prefix, '__PyDFmerge_' + timestamp + '.pdf')

    print("Enter resulting file name or path to confirm merge. Leave blank for default:")
    print("\t" + Fore.LIGHTBLUE_EX + default_file_name + Fore.GREEN)
    file_name = input("$ ")
    print(Style.RESET_ALL)
    return file_name or default_file_name


def name_and_merge(files):
    files.sort()
    count = len(files)
    if count == 0:
        input("No files found. Press any key to exit ...")
        sys.exit(1)

    print("Merging " + str(count) + " files in order:")
    print(Fore.LIGHTBLUE_EX + "\t" + "\n\t".join(files) + "\n" + Style.RESET_ALL)

    file_name = get_result_file_name(files[0])
    print("Writing to " + os.path.abspath(file_name))
    result = merge_files(files, file_name)
    os.system('start "" "' + result + '"')


def collect_input():
    print("Enter file names to merge. Enter a blank line to end the list." + Fore.GREEN)
    result = []
    file_name = input("$ ").strip()
    while file_name:
        if os.path.isfile(file_name):
            result.append(file_name)
        else:
            print(Fore.RED + "No such file." + Fore.GREEN)
        file_name = input("$ ").strip()
    print(Style.RESET_ALL)
    return result


if __name__ == '__main__':
    init()

    if len(sys.argv) == 1:
        files = collect_input()
    else:
        files = resolve_inputs(sys.argv[1:])

    name_and_merge(files)
