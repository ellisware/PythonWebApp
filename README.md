This python web application has a rudimentary HTML5/CSS boilerplate to assist in building a web application.  To demonstrate the python Flask back end, a matlibplot is loaded as an image.  Importantly the python generated image is loaded using a lazy loader reducing the demand on the processor by allowing only visible images to be called, and also this allows the use of a loading graphic for slow processes so the user understands the delay.

Build the container from the docker terminal (directory with dockerfile) being certain to not miss the period at the end of the call:

# docker build -t fullstack .


Run the container from the docker terminal:

# docker run -p 4000:80 fullstack


This will run the container in the foreground (-p) so any errors can be observed in the Docker terminal.  The default docker IP address makes the site available at http://192.168.99.100:4000 
