from bs4 import BeautifulSoup

with open("Prologue.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

lines = [p.get_text(strip=True) for p in soup.find_all("p")]

with open("Prologue cleaned.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(lines))