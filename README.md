# PDF-PPT-ODP-to-HTML-JSON-for-Tidys

Converts a PDF file to HTML. If the file is a .ppt, .pptx or .odp, it converts to PDF first and then to HTML.
Also creates a JSON file (for the Tidys application).

Default behavior is converting the pdf to SVG images and then putting them into an HTML document.

When calling the function, the absolute path of the file must be passed as argument. The CSS file must be in
the same directory as the script.

Requires:
  *  Libreoffice installed
  *  pdf2htmlEX docker image installed. See: https://github.com/coolwanglu/pdf2htmlEX
  *  pdf2svg installed
