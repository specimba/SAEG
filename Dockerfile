FROM ubuntu:22.04@sha256:4f838adc7181d9039ac795a7d0aba05a9bd9ecd480d294483169c5def983b64d

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm

# RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash-static \
    busybox-static \
    ca-certificates \
    curl \
    gcc-multilib \
    git \
    lib32stdc++6 \
    libstdc++6 \
    python3 \
    python3-dev \
    python3-pip \
    ruby-full \
    xz-utils && \
    curl -fsSL -o /tmp/radare2.deb \
    https://github.com/radareorg/radare2/releases/download/6.1.4/radare2_6.1.4_amd64.deb && \
    apt-get install -y --no-install-recommends /tmp/radare2.deb && \
    rm -rf /tmp/radare2.deb /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
# RUN python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN python3 -m pip install --no-cache-dir --upgrade \
    pip==26.1.1 \
    setuptools==82.0.1 \
    wheel==0.47.0 && \
    python3 -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

RUN gem install one_gadget -v 1.9.0 --no-document
RUN ln -sf /usr/bin/bash-static /bin/sh && \
    ln -sf /usr/bin/bash-static /bin/bash && \
    ln -sf /usr/bin/busybox /bin/cat && \
    /bin/sh -c true && \
    /bin/bash -lc true && \
    /bin/cat /dev/null

RUN mkdir /aeg
COPY aeg_module /aeg/aeg_module
COPY ./assets/ /aeg/assets
COPY ./saeg.py /aeg/
COPY ./testset.py /aeg/
COPY ./test_extra_dataset.py /aeg/
