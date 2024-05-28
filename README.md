# OpenInPdfChatBot


1. Build image

```
docker build -t openinpdfchatbot .

```


2. Run With volumes

```
docker run -v pdf_files:/app/pdf_files -it openinpdfchatbot

```