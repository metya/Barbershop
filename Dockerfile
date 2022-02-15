FROM gpuci/miniconda-cuda:11.5-devel-ubuntu20.04

# Install some basic utilities
RUN apt update && apt install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    cmake \
    build-essential \
    libopencv-dev \
    python3-dev \
    && apt autoclean && apt autoremove \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Create a working directory
RUN mkdir /app
WORKDIR /app

ADD environment .

RUN conda env create -f environment.yml
RUN conda clean --all -f -y
RUN conda clean --all -y


COPY . .

SHELL ["conda", "run", "-n", "Barbershop", "/bin/bash", "-c"]
RUN conda env list
RUN pip install dlib --no-cache

ENTRYPOINT [ "conda", "run",  "--no-capture-output", "-n", "Barbershop", "streamlit", "run", "play.py"]