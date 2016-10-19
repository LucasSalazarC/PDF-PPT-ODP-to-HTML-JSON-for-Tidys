
# Comentario porque sí...
from subprocess import call
from os import makedirs, path
from shutil import move

def pdf_to_html_json(presentation_fullpath, dest_dir=None):
    
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
    
    # Command to generate html using pdf2htmlex dockerfile
    command =   'docker run -ti --rm -v ' + directory + \
                ':/pdf bwits/pdf2htmlex pdf2htmlEX --embed cfijo ' + \
                 '--dest-dir ' + filename + ' --zoom 1.3 ' + pdf_filename
                
    call(command.split(' '))



    # Read html document and get the Ids of every page
    found_flag = 0
    page = []

    html = open(temp_dir + html_filename, 'r')

    for line in html.readlines():
        if line.startswith('<div id="pf'):
            found_flag = 1
            page.append(line.split('"')[1])
        elif found_flag == 1:
            break
            
    html.close()



    # NEED TO FIX THIS
    # Need a way to get the url of the html file stored in the server
    html_url = 'https://cg.tidys.io/ltec/presentation.html'

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





