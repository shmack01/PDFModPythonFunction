import logging
import sys
import locale
import tempfile
import os
import subprocess
import ntpath
import errno
import azure.functions as func

# pylint: disable=unsubscriptable-object
def main(myblob: func.InputStream, smblob: func.Out[func.InputStream], context: func.Context) -> None:
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    #context.function_directory
    name = ntpath.basename(myblob.name)
    temp = tempfile.gettempdir()
    filename = os.path.join(temp, name)
    outfilename = os.path.join(temp, "out" + name)

    logging.info(f"Temp File {filename}")
    logging.info(f"Temp Out File {outfilename}")
  
    
    with open(filename, 'wb') as tmpfile:
        tmpfile.write(myblob.read())

    #apt-get -y install ghostscript
    try:
        subprocess.call(['gs'])
    except OSError as e:
        if e.errno == errno.ENOENT:
            #Handle Process not found
            #REMOVE THIS COMMAND WHEN USING DOCKER FILE/CONTAINER
            #DOCKERFILE WILL INSTALL GHOSTSCRIPT
            logging.info("Installing Ghostscript")
            command = subprocess.run(["apt-get", "-y", "install", "ghostscript"], check=True)
            logging.debug(f"The exit code for installing Ghostscript: {command.returncode}")

            #Command was executed and the return code was not successful(0) 
            if command.returncode != 0:
                logging.error("Unable to install Ghostscript. Exiting function app...")
                return
        else:
            logging.error("Error with installing Ghostscript. Exiting function app...")
            return 
    
    
    try:
        logging.info("Begin compressing PDF...")
        #initial_size = os.path.getsize(filename)
        subprocess.call(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                        '-dPDFSETTINGS=/ebook',
                        '-dNOPAUSE', '-dQUIET', '-dBATCH',
                        '-sOutputFile='+ outfilename,
                         filename]
        )
    except OSError as e:
        logging.error(f"Error code when executing Ghostscript program: {e.errno}")
        return

    logging.info("Compression Completed")

    logging.info(f"Temp file Location {outfilename}")
    logging.info("***-----------Testing writing out to Blob-------------***")
    with open(outfilename, 'rb') as outfile:
        logging.info("Writing out to Blob")
        smblob.set(outfile.read())
        logging.info(f"Successful in Compression with file: {outfilename}")

    