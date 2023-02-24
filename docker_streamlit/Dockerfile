FROM python:3.10.6

# Pull the base docker image of python with tag 3.9.13

RUN pip install --upgrade pip


WORKDIR /app
# Change the working dir inside the container - cd /app

COPY Home.py req.txt ./
# Copy main.py as source cod and req.txt as dependency

RUN pip install -r req.txt
# Install the dependency

RUN pip install streamlit --upgrade

ADD pages /app/pages/

ADD pages/Goes18.py /app/pages/
ADD pages/Mapping.py /app/pages/
ADD pages/Nexrad.py /app/pages/

### Container Env same as local at this point

EXPOSE 8000

CMD ["streamlit", "run", "Home.py", "--server.port", "8000"]