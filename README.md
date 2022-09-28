# Nonogram

Semestrální práce implementuje známou *puzzle* hru [Nonogram](https://en.wikipedia.org/wiki/Nonogram), spočívající v obarvování bílé mřížky na základě zadaných instrukcí. Hra bude implementována za pomocí knihovny `pyglet` (**WIP**), která se bude starat o vykreslování GUI. Hra bude mít uložené jednotlivé hádanky v podobě textového souboru, kde bude zapsaná velikost a čísla u daných řádků/sloupců. Po načtení do paměti bude hádanka (zadaná čísla i hrací plocha) reprezentována pomocí několika `numpy array` (**WIP**).

Během řešení hádanky bude hráč mít ve hře zapnutou časomíru (volitelná feature), která si uloží jeho výsledný čas potřebný k vyřešení hádanky. Díky tomu bude možné ke každé hádance vytvořit tabulku nejrychlejších řešitelů (pro podpoření soutěživosti se sebou samým/s jiným lokálním hráčem), případně čas přepočítat na skóre a to střádat na "profilu hráče". 

## Řešitelnost hádanky

Problém řešení Nonogramu již byl matematicky popsán jako NP-úplný, není znám žádný algoritmus který by jej řešil v polynomiálním čase. V semestrální práci jsem se původně snažil problému algoritmického řešení Nonogramu vyhnout (tj. přenechat na uživateli), bohužel to však není tak úplně možné. Hra musí kontrolovat uživatelovy tahy a posoudit, zda neprovádí neplatné tahy (ideálně co nejdříve). Základní verze programu (zn. Hard Mode) nechá hráče hádanku zcela vyplnit bez asistence, a až na konci ověří správnost. Tento problém je algoritmicky jednoduchý, obdobně jako např. u hry Sudoku, postačí pouhá iterace přes řádky a sloupce. Rozšířená verze (zn. Assisted Mode) pak bude každý hráčův tah ověřovat, a upozorní jej na případnou chybu již během hraní.

Jako jedno z možných řešení totoho problému se jeví ukládání hádanek v podobě vyplněné tabulky namísto zadaných čísel (resp. paralelně). Tím by zdánlivě odpadly starosti s výpočetně složitějším ověřováním hráčských tahů, protože by se každý tah pouze porovnával s kompletním řešením. Toto je však špatný nápad, protože některé hlavolamy mohou být zadané nejednoznačně (tedy mít více než jedno korektní řešení). Tato cesta ověřování tahů by znamenala, že by hra neumožnila provést zcela korektní řešení, což je pochopitelně nežádoucí. Problém ověřování, zda je hádanka jednoznačná či nikoliv, je obdobně výpočetně náročný jako samotné řešení hádanky, proto nebude v semestrální práci obsažen.

## Možná rozšíření

- algoritmus pro řešení hádanek (viz Řešitelnost hádanky)
- konverze obrázku standardního formátu na hádanku (fakticky černobílou čtvercovou matici)
- iterace hry s více barvami (možno v kombinaci s konverzí obrázků)
- online sdílená tabulka nejrychlejších časů

## Závislosti a instalace

Závislosti **budou** blíže popsány v souboru `requirements.txt`.

Proces instalace a spuštění:

**TODO**

## Testování

**TODO**

Nemám čas na testy, dělám ProgTest.