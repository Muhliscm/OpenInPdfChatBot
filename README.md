# OpenInPdfChatBot

1. Clone directory
```
git clone https://github.com/Muhliscm/OpenInPdfChatBot.git

```
2. Change dir
```
cd OpenInPdfChatBot

```

3. Build image

```
docker build -t openinpdfchatbot .

```


4. Run With volumes

```
docker run -v pdf_files:/app/pdf_files -it openinpdfchatbot

```