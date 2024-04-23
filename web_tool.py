from duckduckgo_search import DDGS
import requests
from unstructured.partition.html import partition_html
import random
import regex

ddgs = DDGS()

with open("http_proxies.txt", "r") as file:
    data = file.readlines()

http_proxies = []
for proxy in data:
    if proxy.split(":")[0] == "http":
        http_proxies.append(proxy[:-1])  # Till -1 to remove \n

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


class WebTool:
    def __init__(self) -> None:
        pass

    def get_urls(self, text):
        search_results = ddgs.text(text, max_results=2)
        links = [i["href"] for i in search_results]
        print(links, "\n\n")
        return links

    def get_content(self, url):

        content = ""

        proxy = {"http": random.choice(http_proxies)}
        html_reponse = requests.get(
            url=url, headers=header, proxies=proxy
        ).content.decode()
        html_text_elements = partition_html(text=html_reponse)

        for i in html_text_elements:
            if "unstructured.documents.html.HTMLTitle" in str(type(i)):
                clean = regex.sub("\n", lambda x: "", i.text)
                content = content + "\n\n" + clean

            elif "unstructured.documents.html.HTMLNarrativeText" in str(type(i)):
                clean = regex.sub("\n", lambda x: "", i.text)
                content = content + "\n" + clean

            elif "unstructured.documents.html.HTMLListItem" in str(type(i)):
                clean = regex.sub("\n", lambda x: "", i.text)
                content = content + clean + "|"

        return content

    def fetch_content(self, text):
        content = ""
        urls = self.get_urls(text)
        for e, url in enumerate(urls):
            content += f"Source {e+1}\n\n"
            content += self.get_content(url)
            content += "\n\n\n"

        return content.strip()


# print(WebTool().fetch_content(text="russia vs NATO"))
