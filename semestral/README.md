# Onono! The Puzzle Game

Semestrální práce implementuje známou *puzzle* hru [Nonogram](https://en.wikipedia.org/wiki/Nonogram), spočívající v obarvování bílé mřížky na základě zadaných instrukcí. Hra bude implementována za pomocí knihovny `pygame`, která se bude starat o vykreslování GUI. Hra bude mít uložené jednotlivé hádanky v podobě textového souboru, kde budou zapsané údaje o vyplnění jednotlivých políček. Po načtení do paměti bude hádanka (zadaná čísla i hrací plocha) reprezentována pomocí několika `numpy array`. Jedna matice bude ukládat načtená data, představující korektní řešení, do druhé se bude ukládat průběžný stav hry. Nápovědy pro jednotlivé řádky/sloupce se však budou ukládat jako `list`, vzhledem k jejich rozdílné délce.

Během řešení hádanky bude hráč mít ve hře zapnutou časomíru (volitelná feature), která si uloží jeho výsledný čas potřebný k vyřešení hádanky. Díky tomu bude možné ke každé hádance vytvořit **tabulku nejrychlejších řešitelů** (pro podpoření soutěživosti se sebou samým/s jiným lokálním hráčem), případně čas přepočítat na skóre a to střádat na "profilu hráče".

Zároveň bude ve hře implementována **konverze obrázku** standardního (a snadno zpracovatelného) formátu na hádanku (fakticky černobílou čtvercovou matici). To umožní ve hře rychlé a jednoduché vytváření hádanek a velkou míru znovuhratelnosti.

## Řešitelnost hádanky

Problém řešení Nonogramu již byl matematicky popsán jako NP-úplný, není znám žádný algoritmus který by jej řešil v polynomiálním čase. V semestrální práci jsem se původně snažil problému algoritmického řešení Nonogramu vyhnout (tj. přenechat na uživateli), bohužel to však není tak úplně možné. Hra musí kontrolovat uživatelovy tahy a posoudit, zda neprovádí neplatné tahy (ideálně co nejdříve). Základní verze programu (zn. Hard Mode) nechá hráče hádanku zcela vyplnit bez asistence, a až na konci ověří správnost. Tento problém je algoritmicky jednoduchý, obdobně jako např. u hry Sudoku, postačí pouhá iterace přes řádky a sloupce. Rozšířená verze (zn. Assisted Mode) pak bude každý hráčův tah ověřovat, a upozorní jej na případnou chybu již během hraní.

Jako jedno z možných řešení totoho problému se jeví ukládání hádanek v podobě vyplněné tabulky namísto zadaných čísel, a následné porovnávání uživatelského řešení s referencí. Tím by zdánlivě odpadly starosti s výpočetně složitějším ověřováním hráčských tahů, je však špatný nápad se spoléhat pouze na tento způsob. Některé hlavolamy totiž mohou být zadané nejednoznačně (tedy mít více než jedno korektní řešení). Tato cesta ověřování tahů by znamenala, že by hra neumožnila provést zcela korektní řešení, což je pochopitelně nežádoucí. Problém ověřování, zda je hádanka jednoznačná či nikoliv, je obdobně výpočetně náročný jako samotné řešení hádanky, proto nebude v semestrální práci obsažen.

Samotná implementace hry řeší tento problém na dvou úrovních. Korektní řešení je ukládáno jako matice "správných tipů" (načtená ze souboru/náhodně generovaná). Z té se následně generují řádky/sloupce nápověd, které se ve hře zobrazují jako čísla na kraji hrací plochy. Po každé změně hrací plochy se provede následující:

- vytvoří se kopie tipů uživatele, která má místo prázdných polí "křížky" (tedy tipy, že toto pole nemá být vybarveno)
- dojde k porovnání totožnosti s referenčním řešením
  - pokud se matice shodují, dále se nic nekontroluje a hra je ukončena
- dojde k porovnání shody s jednotlivými vektory nápověd
  - pokud se neshodují obě matice, ale shodují se všechny nápovědy, hra je také považována za ukončenou

Poslední krok (porovnání shody s nápovědami) se také dá využít pro určitou formu nápovědy hráči. Pokud se řešení v jednom řádku/sloupci s nápovědou shoduje, vykreslená čísla zněmí barvu. Tím uživatel dostane najevo, že tento řádek má "splněný", a může se soustředit na zbytek hrací plochy.

## Možná rozšíření

- algoritmus pro řešení hádanek (viz Řešitelnost hádanky)
- iterace hry s více barvami (v kombinaci s konverzí obrázků)
- online sdílená tabulka nejrychlejších časů

## Závislosti a instalace

Závislosti jsou popsány v souboru `requirements.txt`. Jediné velké balíčky, o které se práce opírá, jsou pygame (pro celé vykreslování GUI) a numpy (pro práci s herními savy a víceméně veškeré operace s poli).

Proces instalace a spuštění:
- Nainstalujte veškeré závislosti pomocí příkazu `pip install -r requirements.txt`.
- Ujistěte se, že se nacházíte v adresáří `semestral/`.
- Spusťte hru pomocí zadání příkazu `python onono` do příkazové řádky.
- Hru můžete ukončit zavřením okna nebo klávesovou zkratkou Ctrl+C v terminálu.

## Testování

Testovací soubory jsou obsaženy v adresáří `tests`. Některé z nich pracují i s vlastními herními savy (mezní případy nesprávných vstupů), takové jsou v adresáři `saves\tests`. Testy je možné spustit pomocí příkazu `pytest`, spuštěného v domovském adresáří.

## TODO
- možnost uložit náhodně generovaný puzzle
- generování puzzle z obrázku - implementace v menu
- nastavení obtížnosti (generování puzzle/načítání obrázku)
- "puzzle menu" - obtížnost, tabulka (potřeba adekvátně upravit savegame, "wrapper")
- "Assisted mode" - solver???
