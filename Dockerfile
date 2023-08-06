FROM python:3.10

ARG PYTORCH_VERSION=2.0.1
ARG TORCHVISION_VERSION==0.15.2
ARG TORCH_CPU_URL=https://download.pytorch.org/whl/cpu/torch_stable.html

RUN \
    python -m pip install --no-cache-dir \
    torch==${PYTORCH_VERSION}+cpu \
    torchvision==${TORCHVISION_VERSION}+cpu -f ${TORCH_CPU_URL}

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c 'from transformers import CLIPProcessor, CLIPModel; CLIPModel.from_pretrained("openai/clip-vit-base-patch32"); CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")'

COPY ["hw.py", "."]

CMD ["uvicorn", "hw:app", "--host", "0.0.0.0", "--port", "80"]