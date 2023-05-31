# CHESSBOT

CHESSBOT - interaktywny program, który umożliwia użytkownikom rozgrywanie partii szachowych na komputerze. Program będzie wykorzystywał bibliotekę szachową pythona (python-chess) do generowania planszy i przeprowadzania ruchów.



## Funkcje CHESSBOT:

1. Generowanie planszy szachowej
2. Zarządzanie ruchami graczy na planszy
3. Określenie poprawności ruchów zgodnie z zasadami gry szachowej
4. Określanie końca gry (szach-mat, pat, remis)
5. Zapisywanie i wczytywanie stanu gry
6. Tryb gry z komputerem (dostępne różne poziomy trudności)
7. Tryb gry z innym graczem (online)

## Harmoniogram prac:

1. 2023-04-04
    1. Generowanie planszy szachowej
    2. Implementacja przeprowadzania ruchów graczy
    3. Określenie poprawności ruchów zgodnie z zasadami gry
    4. Określanie końca gry
2. 2023-04-18
    1. Zapisywanie i wczytywanie stanu gry
    2. Implementacja trybu gry z komputerem
3. 2023-05-16
    1. Autoryzacja i autentykacja
    2. Realizacja części backendu
4. 2023-05-30
    1. Realizacja backend - c.d
    2. hisoria gier, statystyki, rankingi
 
## Technologie, których planujemy użyć:

1. Biblioteka chess - obsługa gier szachowych
2. PyGame
3. Flask - serwer + zapytania HTTP / TCP

## Feedback po prezentowaniu, plan prac przed oddaniem projektu(od najwazniejszych/najłatwiejszych do najtrudniejszych):
- [ ] oznaczenie, czyj jest ruch:
  (przypominajka: ```simulation.board.turn() -> True | False```, True to białe)
- [x] brak możliwości klikania w puste pola/ pola z figurami przeciwnika
- [ ] narysowane możliwe ruchy po kliknięciu figury
- [ ] przycisk cofający do menu wyboru trybu (bez zapisywania itp., pomysł aby nie tzeba było wychodzić x, co sprawia ze trzeba znów sie logować)
- [ ] okno GM's (może być zastąpiona przyciskiem "wczytaj ostatnią grę z komputerem")
- [ ] numeracja wierszy, kolumn na planszy
- [ ] GUI promocji piona
- [ ] zapisywanie, wczytywanie stanu gry (pomysł: zapisywanie może być aktywowane klawiszem s, informacja "Nacisnij s aby zapisac może być w tytule okna dla oszczędności czasu i okien")
- [ ] tryb gry z innym graczem
