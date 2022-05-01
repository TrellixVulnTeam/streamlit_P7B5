FROM python:3

WORKDIR /app

RUN pip install -U pip

COPY requirements.txt ./requirements.txt
RUN pip install -r app/requirements.txt

# remember to expose the port your app'll be exposed on.
EXPOSE 8080
# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . /app


# run it!
# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
CMD streamlit run --server.port:8080 --server.enableCORS false app.py