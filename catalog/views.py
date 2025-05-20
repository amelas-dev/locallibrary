from django.shortcuts import render
from django import forms


class UploadPDFForm(forms.Form):
    """Simple form for uploading a single PDF file."""
    pdf_file = forms.FileField(label="Select PDF")


def extract_text_from_pdf(file_obj):
    """Extract text from each page of the uploaded PDF.

    This function tries to use ``PyPDF2`` to read the file. If the
    dependency is missing or an error occurs while reading, an empty list
    is returned along with the error message.
    """
    pages = []
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception as exc:  # ImportError or other issues
        return [], str(exc)

    try:
        reader = PdfReader(file_obj)
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"page": i, "text": text})
        return pages, None
    except Exception as exc:  # pylint: disable=broad-except
        return [], str(exc)


def upload_pdf(request):
    """Handle PDF upload and display extracted text in a table."""
    table_data = []
    error = None

    if request.method == "POST":
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data["pdf_file"]
            table_data, error = extract_text_from_pdf(pdf_file)
    else:
        form = UploadPDFForm()

    context = {"form": form, "table_data": table_data, "error": error}
    return render(request, "catalog/upload.html", context)

