This is the PDF reader example for "Embedding Meta-Information into
Visualizations"
It is composed of three parts:

    1. A Flask-based backend that receives a PDF file, searches its pages for
    images, and attempts to extract a watermark from each image. It responds
    with a JSON containing information about the images that had a watermark
    successfully extracted from them and the data associated with them

    2. A simple database that contains a table of key -> data for the server
    above to search through. The server only knows that an image has a valid
    watermark if there is an existing result in the database

    3. A PDF reader using a modified pdf.js, which first sends the PDF file to
    the server above before receiving a JSON response. In this response, there
    should be information about where the image is in the PDF, because pdf.js
    does not have any other way of locating images
