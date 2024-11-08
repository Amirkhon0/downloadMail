import sys
import os
import re
import requests

def getDirectLinkFromMailCloudUrl(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        page_content = response.text

        re_pattern = r'dispatcher.*?weblink_get.*?url":"(.*?)"'
        match = re.search(re_pattern, page_content)

        if match:
            url = match.group(1).replace('\\', '')
            parts = link.split('/')[-2:]
            return f'{url}/{parts[0]}/{parts[1]}'
    except Exception as e:
        print(f"Ошибка: {e}")
    return None

def getFromMailCloudUrl(link, to, file):
    url = getDirectLinkFromMailCloudUrl(link)
    if not url:
        print("Не удалось получить прямую ссылку.")
        return

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        os.makedirs(to, exist_ok=True)
        file_path = os.path.join(to, file)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Файл успешно сохранён: {file_path}")
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: download.exe <ссылка> <путь>")
    else:
        link = sys.argv[1]
        to = sys.argv[2]
        file = sys.argv[3]
        getFromMailCloudUrl(link, to, file)
