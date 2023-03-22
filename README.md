# Onono! The Puzzle Game

Semestrální práce implementuje známou *puzzle* hru [Nonogram](https://en.wikipedia.org/wiki/Nonogram), spočívající v obarvování bílé mřížky na základě zadaných instrukcí. Hra je implementována za pomocí knihovny `pygame`, která se stará o veškeré vykreslování GUI. 

Jedním z hlavních rozšíření této hry je možnost nahrát libovolný obrázek formátu PNG a nechat jej převést na samotnou hádanku. To umožní ve hře rychlé a jednoduché vytváření hádanek a velkou míru znovuhratelnosti.

Bližší informace o práci jako takové, jejím vývoji a možném rozšíření se nachází tzv. *reportu* v souboru `ruzicsi1.pdf`.

## Závislosti a instalace

Závislosti jsou popsány v souboru `requirements.txt`. Jediné velké externí balíčky, o které se práce opírá, jsou `pygame` (pro celé vykreslování GUI), `numpy` (pro práci s herními savy a víceméně veškeré operace s poli) a `PIL` (tj. *Python Imaging Library*; pro zpracování vstupního obrázku). Pro testování jsou dále využity balíčky `pytest`, `pylint` a `pyautogui`.

Proces instalace a spuštění:
- Ujistěte se, že se nacházíte v adresáří `semestral/`.
- Nainstalujte veškeré závislosti pomocí příkazu `pip install -r requirements.txt`.
- Spusťte hru pomocí zadání příkazu `python onono` do příkazové řádky.
- Hru můžete ukončit tlačítkem v menu, zavřením okna nebo klávesovou zkratkou Ctrl+C v terminálu.

## Testování

Testovací soubory jsou obsaženy v adresáří `tests`. Některé z nich pracují i s vlastními herními savy (mezní případy nesprávných vstupů), takové jsou v adresáři `saves\tests`, resp. `saves\images\tests`. V souboru `test_lint` se nachází automatická kontrola linterem `pylint`, všechny moduly by měly (s vyjímkou uvedených odůvodněných varování) procházet na plné skóre, což znamená že zdrojový kód semestrální práce je v souladu s PEP 8.

Testy je možné spustit pomocí příkazu `pytest`, spuštěného v domovském adresáří.
