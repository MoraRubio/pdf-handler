import os
from pikepdf import Pdf

def get_filename(path):
    return path.split('/')[-1].split('.')[0]

def split(path, destination=os.getcwd()):

    """
    Split PDF file into single pages.

    Inputs:
    path: path to original PDF file
    destination: path to destination folder

    Outputs:
    Saves each page of the original file as a new PDF file in the destination folder.
    """
    
    filename = get_filename(path)
    with Pdf.open(path) as src:
        for n, page in enumerate(src.pages):
            dst = Pdf.new()
            dst.pages.append(page)
            dst.save(f'{destination}/{filename}_page_{n+1:02d}.pdf')

#split('C:/Users/alejo/Downloads/conda-cheatsheet.pdf')

def merge(paths, destination=os.getcwd()):

    """
    Merge multiple PDF files into a single one.

    Inputs:
    paths: List of paths to original PDF files
    destination: path to destination folder

    Outputs:
    Saves a new PDF file in the destination folder.
    """

    pdf = Pdf.new()
    version = pdf.pdf_version
    for file in paths:
        with Pdf.open(file) as src:
            version = max(version, src.pdf_version)
            pdf.pages.extend(src.pages)
    pdf.remove_unreferenced_resources()
    pdf.save(f'{destination}/merged.pdf', min_version=version)

#merge(['conda-cheatsheet_page_01.pdf', 'conda-cheatsheet_page_02.pdf'])

def reorganize(path, order, destination=os.getcwd()):

    """
    Reorganize the order of the pages in a PDF file.

    Inputs:
    path: path to original PDF file
    order: list of ordered page numbers to include in the file
    destination: path to destination folder

    Outputs:
    Saves a new PDF file in the destination folder.
    """

    filename = get_filename(path)
    dst = Pdf.new()
    with Pdf.open(path) as src:
        for n_page in order:
            dst.pages.append(src.pages[n_page-1])
    dst.save(f'{destination}/{filename}_organized.pdf')

#reorganize('merged.pdf', [2,1])