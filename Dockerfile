# Start with the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y \
    # C++ development tools
    build-essential \
    g++ \
    cmake \
    make \
    ninja-build \
    git \
    # Python development tools
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    # Zsh and utilities for Prezto
    zsh \
    curl \
    wget \
    vim \
    unzip \
    zip \
    sudo \
    # Clean up APT when done
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up Zsh and Prezto
RUN chsh -s /usr/bin/zsh \
    && git clone --recursive https://github.com/sorin-ionescu/prezto.git /root/.zprezto \
    && zsh -c 'setopt EXTENDED_GLOB' \
    && zsh -c 'for rcfile in /root/.zprezto/runcoms/^README.md(.N); do ln -s "$rcfile" "/root/.${rcfile:t}"; done'

# Create and activate the virtual environment
WORKDIR /root
RUN python3 -m venv venv

# Copy the requirements file
COPY requirements.txt /root/llmcc/

# Set the working directory
WORKDIR /root/llmcc

# Install dependencies from requirements.txt using the virtual environment's pip
RUN /root/venv/bin/pip install --upgrade pip \
    && /root/venv/bin/pip install -r requirements.txt


RUN echo "zstyle ':prezto:module:prompt' theme 'sorin'" >> /root/.zpreztorc


# Start Zsh with Prezto
CMD [ "zsh" ]