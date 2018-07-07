Build the container from the docker terminal (directory with dockerfile) being certain to not miss the period at the end of the call:

# docker build -t fullstack .


Run the container from the docker terminal:

# docker run -p 4000:80 fullstack


This will run the container in the foreground (-p) so any errors can be observed in the Docker terminal.  The default docker IP address makes the site available at http://192.168.99.100:4000 
