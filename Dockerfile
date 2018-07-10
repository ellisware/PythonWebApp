FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install matplotlib
RUN pip install msgpack
RUN pip install halogen

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 1
# ENV STATIC_INDEX 0

COPY ./app /app
