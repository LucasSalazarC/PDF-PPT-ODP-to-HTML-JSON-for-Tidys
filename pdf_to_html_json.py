
from subprocess import call
from os import makedirs, path, walk, listdir, rename
from shutil import move, copyfile, rmtree
import json

def pdf_to_html_json(presentation_fullpath, dest_dir=None, conv_to_img=1, url='https://lucas.tidys.io/'):

    # Get directory, filename, extension
    name_length = len(presentation_fullpath.split('/')[-1])
    directory = presentation_fullpath[0:-1*name_length]     # includes '/'
    filename = presentation_fullpath.split('/')[-1].split('.')[0]
    extension = presentation_fullpath.split('.')[-1]


    try:
        # Check if file exists
        if not path.isfile(presentation_fullpath):
            raise Exception("Error: File doesn't exist")

        # If file is a ppt, convert to pdf
        elif extension in ['ppt', 'pptx', 'odp']:
            command =   'libreoffice --headless --invisible --convert-to pdf ' + \
                        presentation_fullpath + ' --outdir ' + directory
            call(command.split(' '))

        # If not a ppt or pdf, return
        elif extension != 'pdf':
            raise Exception("Error: Invalid file type")

    except Exception as e:
        print(e.args[0])
        return


    # Get filenames
    pdf_filename = filename + '.pdf'
    html_filename = filename + '.html'
    json_filename = filename + '.json'

    # Create output directory
    temp_dir = directory + filename + '/'
    if not path.exists(temp_dir):
        makedirs(temp_dir)

    # Copy style.css
    copyfile('style.css', temp_dir + 'style.css')


    # Convert pdf to image and write html manually
    if conv_to_img:
        # Using pdftoppm (generates jpeg)
        command = 'pdftoppm -jpeg ' + directory + pdf_filename + ' ' + temp_dir + filename
        call(command.split(' '))

        # Rename jpeg files to match svg files
        for root, dirs, files in walk(temp_dir):
            for file in files:
                name_array = file.split("-")
                if name_array[-1].startswith("0"):
                    name_array[-1] = name_array[-1][1:]
                    rename(temp_dir + file, temp_dir + '-'.join(name_array))

        # Using pdf2svg
        command = 'pdf2svg ' + directory + pdf_filename + ' ' + temp_dir + filename + '-%d.svg all'
        call(command.split(' '))

        html = open(temp_dir + html_filename, 'w')

        # Count number of png images, which is the number of pages in the pdf
        png_counter = 0
        for root, dirs, files in walk(temp_dir):
            for file in files:
                if file.endswith('.svg'):
                    png_counter += 1

        # Write html
        html.write('<!DOCTYPE html>\n')
        html.write('<html>\n')
        html.write('<head>\n')
        html.write('    <meta charset="utf-8">\n')
        html.write('    <meta name="generator" content="pandoc">\n')
        html.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">\n')
        html.write('    <title></title>\n')
        html.write('    <style type="text/css">code{white-space: pre;}</style>\n')
        html.write('    <link rel="stylesheet" href="style.css">\n')
        html.write('    <!--[if lt IE 9]>\n')
        html.write('    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv-printshiv.min.js"></script>\n')
        html.write('    <![endif]--><link rel="stylesheet" href="https://use.fontawesome.com/4b0be90c69.css" media="all">\n')
        html.write('</head>\n')
        html.write('<body>\n')

        for i in range(png_counter):
            html.write('    <section id="pf' + format(i + 1,'0x') + '" class="level1 vflex">')
            html.write('        <figure>\n')
            html.write('            <img src="' + filename + '-' + str(i + 1) + '.svg" />\n')
            html.write('        </figure>\n')
            html.write('    </section>\n')

        html.write('</body>\n')
        html.write('</html>\n')

        html.close()


    else:
        # Command to generate html using pdf2htmlex dockerfile
        command =   'docker run -ti --rm -v ' + directory + \
                    ':/pdf bwits/pdf2htmlex pdf2htmlEX --embed cfijo ' + \
                     '--dest-dir ' + filename + ' --zoom 1.3 ' + pdf_filename

        call(command.split(' '))



    # Read html document and get the Ids of every page
    page = []

    html = open(temp_dir + html_filename, 'r')

    for line in html.readlines():
        if line.startswith('<div id="pf') or '<section id="pf' in line:
            page.append(line.split('"')[1])

    html.close()


    html_url = url + filename + '/' + html_filename

    # Create json file as dictionary, then dump into file
    json_dict = {}
    json_dict["name"] = filename
    json_dict["slides"] = []

    for item in page:
        temp = {"question": 'null'}
        temp["url"] = html_url + '#' + item
        json_dict["slides"].append(temp)
        del temp

    with open(temp_dir + json_filename, 'w') as fp:
        json.dump(json_dict, fp)




    # Move directory containing HTML and JSON to dest_dir
    if dest_dir is not None:
        if path.exists(dest_dir):
            rmtree(dest_dir, ignore_errors=True)
        move(temp_dir, dest_dir)


    return
