
from subprocess import call
from os import makedirs, path, walk
from shutil import move, copyfile

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
        command = 'convert ' + directory + pdf_filename + ' ' + temp_dir + filename + '.png'
        call(command.split(' '))
        
        html = open(temp_dir + html_filename, 'w')
        
        # Count number of png images, which is the number of pages in the pdf
        png_counter = 0
        for root, dirs, files in walk(temp_dir):
            for file in files:    
                if file.endswith('.png'):
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
            html.write('            <img src="' + filename + '-' + str(i) + '.png" />\n')
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


    html_url = url + html_filename

    # Create .json file with same name as pdf file
    json_file = open(temp_dir + json_filename, 'w')

    # Write .json file
    json_file.write('{\n')
    json_file.write('  "name": ' + '"' + pdf_filename[0:-4] + '",\n')
    json_file.write('  "slides": [\n')

    for item in page:
        json_file.write('    {\n')
        json_file.write('      "question": null,\n')
        json_file.write('      "url": "' + html_url + '#' + item + '"\n')
        json_file.write('    },\n')
        
    json_file.write('  ]\n')
    json_file.write('}\n')

    json_file.close()
    
    
    
    # Move directory containing HTML and JSON to dest_dir
    if dest_dir is not None:
        move(temp_dir, dest_dir)
    
    
    return





