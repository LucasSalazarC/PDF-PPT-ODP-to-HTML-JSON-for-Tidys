# PDF-PPT-ODP-to-HTML-JSON-for-Tidys

Converts a PDF file to HTML. If the file is a .ppt, .pptx or .odp, it converts to PDF first and then to HTML.
Also creates a JSON file (for the Tidys application).

Default behavior is converting the pdf to PNG images putting them into an HTML document.

When calling the function, the absolute path of the file must be passed as argument.

Requires:
  *  Libreoffice installed
  *  ImageMagick installed
  *  pdf2htmlEX docker image installed. See: https://github.com/coolwanglu/pdf2htmlEX
