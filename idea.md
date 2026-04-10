## OBSŁUGA ZGLOSZENIA HELPDESK

1) Podjęcie zgłoszenia
2) Odnotowanie problemu
3) Wprowadzenie opisu problemu do Agenta
4) Uruchomienie Agenta

---------------
### CO ROBI AGENT: (poprzez wmi)
1) Zbiera dane o wydajności stacji
2) RAM, CPU, DYSK
3) Zbiera logi dt. usług systemowych (np. ZBHost)
4) Sprawdza adres IP stacji (czy komputer znajduje się w dobrym VLAN)
5) Aktywna karta sieciowa (np. czy w KSI czy VPN)
6) Najbardziej obciążające procesy
7) Stan baterii
---
5) Zwrócenie payload (format json, podsumowanie analizy)
6) Generowanie odpowiedzi LLM
7) Zwrócenie gotowych rozwiązań
---------------

## ZALETY:
1) Rozwijanie standardów pracy HelpDesk
2) Szybsza i kompleksowa reakcja na problemy użytkowników
3) Kompleksowa analiza pracy komputerów w sieci


## WADY:
1) Halucynacja modeli

## ROLA PRACOWNIKA IT (INFORMATYKA)
1) Weryfikacja generowanych raportów
2) Implementacja rozwiązań proponowanych przez system
3) Reagowanie na zmiany


---
### CO ROBI AGENT: (poprzez wmi) - AGENT MOŻE PEŁNIĆ ROLĘ CHECKLISTY - PAYLOAD JEST RAPORTEM O STANIE KOMPUTERA
1) Zbiera dane o wydajności stacji
2) RAM, CPU, DYSK
3) Zbiera logi dt. usług systemowych (np. ZBHost)
4) Sprawdza adres IP stacji (czy komputer znajduje się w dobrym VLAN)
5) Aktywna karta sieciowa (np. czy w KSI czy VPN)
6) Najbardziej obciążające procesy
7) Stan baterii
---
8) Jak sprawdzić, czy problem na innej stacji? : to zależy, ponieważ trzeba, by mieć dostęp do logów aplikacji, do tego zdalny -> najprościej na tym etapie sprawdzać, czy payload na innej stacji jest podobny -> FUNKCJA COMPARE

#### FUNKCJA COMPARE
1) Wygeneruj payload - stacja A
2) Wygeneruj payload - stacja B
...
3) Wygeneruj payload - stacja N (max 3)
4) Zamień na embedding -> reprezentacja wektorowa
5) Zastosuj cosine similarity - podobieństwo cosinusowe
6) Jeżeli wynosi > 0.8 - podobny problem występuje na innych stacjach
