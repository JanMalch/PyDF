import os

from PyPDF2 import PdfFileMerger, PdfFileReader

# todo: wip

def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    print(info)
    print(number_of_pages)

    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title


class Selection:
    def __init__(self, pdf_id, start, end):
        self.pdf_id = pdf_id
        self.start = start
        self.end = end

    def __str__(self):
        return "Selection{pdf_id=" + str(self.pdf_id) + ", start=" + str(self.start) + ", end=" + self.end + "}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, input_string):
        pdf_id, range = input_string.split()
        pdf_id = int(pdf_id.lstrip('#'))
        range = range.replace('*..', '0..').split('..')
        if len(range) == 1:
            start, end = range[0], range[0]
        else:
            start, end = range
        return cls(pdf_id, int(start), end)


def parse_selection(input):
    return list(map(lambda x: Selection.from_string(x.strip()), input.split(',')))


def print_pdf_info(id, path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()

    print("#" + str(id) + " : " + path + " (" + str(number_of_pages) + " pages)")


def get_pages_from_pdf(path, start, end):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        if end == "*":
            parsed_end = pdf.getNumPages() - 1
        else:
            parsed_end = int(end)
        return map(lambda p: pdf.getPage(p), range(start, parsed_end))


def create_pdf_from_selections(selections):
    merger = PdfFileMerger()
    with open('test.pdf', 'wb') as fout:
        print(selections)
        for s in selections:
            merger.append(pdfById[s.pdf_id], pages=(s.start, int(s.end) - s.start))
        merger.write(fout)
        return os.path.abspath(fout.name)


pdfById = ['ab.pdf', 'xy.pdf'] # temp


if __name__ == '__main__':
    print_pdf_info(0, 'ab.pdf')
    print_pdf_info(1, 'xy.pdf')
    print('#0 *..2, #1 2, #1 1..3')
    selections = parse_selection('#0 *..2, #1 2, #0 1..3')
    path = create_pdf_from_selections(selections)
    print(path)
