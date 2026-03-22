# Lumos Agent

Agent diagnostyczny systemu Windows zbierający informacje o stanie komputera.
Jego zadaniem jest analiza podstawowych parametrów wydajnościowych oraz dostarczanie danych do systemów monitoringu lub narzędzi AI (np. SolveDesk).

Agent może być używany jako część większego systemu diagnostycznego lub jako samodzielne narzędzie do sprawdzania wydajności stacji roboczej.

---

# Funkcjonalności

Agent umożliwia odczyt podstawowych parametrów systemu:

### 1. Użycie pamięci RAM

* całkowita ilość pamięci RAM
* procentowe użycie pamięci

### 2. Użycie procesora

* aktualne użycie CPU w procentach

### 3. Zajętość dysku

* całkowita pojemność dysku
* procent zajętej przestrzeni

### 4. Najbardziej obciążające procesy

* lista procesów
* PID procesu
* nazwa procesu
* użycie CPU

Agent zwraca **5 najbardziej obciążających procesów**.

---

# Architektura

Agent składa się z serwisu diagnostycznego:

```
DiagnoseService
```

Odpowiada on za komunikację z systemem operacyjnym poprzez bibliotekę **psutil**.

Dostępne metody:

| Metoda               | Opis                                            |
| -------------------- | ----------------------------------------------- |
| `check_ram_usage()`  | Zwraca informacje o użyciu RAM                  |
| `check_cpu_usage()`  | Zwraca aktualne użycie CPU                      |
| `check_disk_space()` | Zwraca informacje o wykorzystaniu dysku         |
| `top_processes()`    | Zwraca listę najbardziej obciążających procesów |

---

![workflow](image-1.png)

# Wymagania

## Python

Python 3.9+

## Biblioteki Python

```
psutil
```

Instalacja:

```
pip install psutil
```

---

## Lokalny model LLM

Agent może współpracować z lokalnym modelem językowym uruchamianym przez **Ollama**.

W projekcie wykorzystywany jest model:

* **qwen2.5:3b**

### Instalacja Ollama

Pobierz i zainstaluj Ollama:

https://ollama.com

### Pobranie modelu

```
ollama pull qwen2.5:3b
```

### Uruchomienie serwera Ollama

```
ollama serve
```

Domyślnie API Ollama działa pod adresem:

```
http://localhost:11434
```

Agent wykorzystuje to API do komunikacji z modelem LLM w celu planowania operacji diagnostycznych oraz interpretacji wyników systemowych.


---

# Uruchomienie

Przykładowe użycie:

```python
python -m venv venv
venv\Scripts\activate

python main.py
```

Przykładowy wynik:

Badanie
```json
{"type": "plan", "content": ["check_cpu_usage", "check_ram_usage", "check_disk_space", "top_processes"]}
{"type": "observation", "content": {"tool": "check_cpu_usage", "result": {"cpu_usage_percent": 48.8}}}
{"type": "observation", "content": {"tool": "check_ram_usage", "result": [{"AvgTotalGB": 15.72000000000002, "AvgUsedGB": 13.672333333333336, "AvgFreeGB": 2.047666666666667, "AvgUsedPercent": 86.97166666666665}]}}
{"type": "observation", "content": {"tool": "check_disk_space", "result": {"disk_total_gb": 237.76, "disk_used_percent": 96.5}}}
{"type": "observation", "content": {"tool": "top_processes", "result": [{"Id": 1724, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 1004.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:39:59.6067664"}, {"Id": 1441, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 957.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:39:24.7200238"}, {"Id": 25, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 949.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:36:44.3885368"}, {"Id": 309, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 949.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:37:16.0901868"}, {"Id": 592, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 949.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:37:46.9104436"}, {"Id": 875, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 949.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:38:18.6411362"}, {"Id": 1158, "MachineGuid": "<PC_NAME>", "ProcessId": 10028, "ProcessName": "devenv", "MemoryUsageMB": 949.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-21T15:43:04.1456354+01:00", "LastScan": "2026-03-22 10:38:51.3447019"}, {"Id": 9066, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 902.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:57:26.4448836"}, {"Id": 9349, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 902.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:58:00.5804277"}, {"Id": 8783, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 881.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:54:37.6199807"}, {"Id": 8503, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 862.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:53:59.862154"}, {"Id": 8224, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 816.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:53:22.4794512"}, {"Id": 7945, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 801.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:52:46.1050987"}, {"Id": 7387, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 796.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:51:34.3226447"}, {"Id": 7666, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 796.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:52:12.3339674"}, {"Id": 12970, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 787.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:06:19.8066768"}, {"Id": 13203, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 784.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:06:57.4461033"}, {"Id": 7108, "MachineGuid": "<PC_NAME>", "ProcessId": 20896, "ProcessName": "devenv", "MemoryUsageMB": 783.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T10:50:06.3571166+01:00", "LastScan": "2026-03-22 10:51:01.2468834"}, {"Id": 13463, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 691.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:07:33.7871848"}, {"Id": 10886, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 664.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:01:34.3499958"}, {"Id": 11147, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 644.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:02:08.9194291"}, {"Id": 11409, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 644.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:02:42.988393"}, {"Id": 12711, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 602.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:05:41.6877386"}, {"Id": 11645, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 565.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:03:16.2944533"}, {"Id": 12452, "MachineGuid": "<PC_NAME>", "ProcessId": 11880, "ProcessName": "Code", "MemoryUsageMB": 527.0, "CpuUsagePercent": 0.0, "StartTime": "2026-03-22T11:01:03.8549193+01:00", "LastScan": "2026-03-22 11:05:04.8311821"}]}}
```

Diagnoza
```json
{"type": "summary", "content": "Podsumowanie wydajno\u015bci komputera na podstawie obserwowanych wynik\u00f3w diagnostycznych powinno pom\u00f3c informatykom w postaci wskazania, kt\u00f3re mog\u0105 by\u0107 zwi\u0105zane z problemem. Oto niekt\u00f3re podej\u015bcia do analizy:\n\n### 1. **Wysoki warto\u015bci CPU (Czas wykonania procesor\u00f3w)**:\n   - Poni\u017csza lista pokazuje, \u017ce wi\u0119kszo\u015b\u0107 proces\u00f3w dzia\u0142a na niskich wydajno\u015bciach CPU (~0-2%), ale kilka proces\u00f3w ma wy\u017cej napi\u0119cia CPU, co mo\u017ce by\u0107 zwi\u0105zane z du\u017c\u0105 obci\u0105\u017ceniem komputera.\n   \n   **Prawda:** Najpierw sprawd\u017a, kt\u00f3re procesy maj\u0105 wysokie warto\u015bci CPU. Mo\u017cliwe \u017ce one s\u0105 nadmiernie wykorzystywane przez aplikacje, kt\u00f3rych nie trzeba uruchamia\u0107.\n\n### 2. **Wysoki warto\u015bci RAM [...] konieczne zmniejszenie u\u017cycia plik\u00f3w.\n3. **Sprawd\u017a procesy**: Upewnij si\u0119, \u017ce nie s\u0105 nadmiernie wykorzystywane przez niekt\u00f3re aplikacje lub procesy.\n\n### Wniosek:\nWystarczy to og\u00f3lnie, aby pom\u00f3c w identyfikacji problemu. Warto upewni\u0107 si\u0119, \u017ce wszystkie te punkty s\u0105 odpowiednio zaktualizowane i sprawdzone. Dalsze kroki zale\u017c\u0105 od kontekstu konkretnego problemu i wynik\u00f3w obserwacji."}
```

---

# Przykładowe zastosowania

Agent może być używany w różnych scenariuszach:

1. **Diagnostyka wolno działającego komputera**
2. **Monitoring stacji roboczych**
3. **Automatyczna analiza problemów użytkownika**
4. **Integracja z systemami helpdesk**
5. **Źródło danych dla agentów AI**

---

![cmd test](image.png)

# Integracja z Lumos

Przykład integracji z projektem Lumos - usługą systemową Windows magazynującą informację o wydajności stacji.
ConnectionString odpowiada ścieżce bezwzględnej do pliku lokalnego .db.

```python

def fetch_memory_ram_scan(self):
        query = text("""SELECT 
            AVG(TotalGB)     AS AvgTotalGB,
            AVG(UsedGB)      AS AvgUsedGB,
            AVG(FreeGB)      AS AvgFreeGB,
            AVG(UsedPercent) AS AvgUsedPercent
        FROM MemoryRamScans""")

        with self.engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()

        return [dict(row._mapping) for row in rows]

```

```json

{"type": "observation", "content": {"tool": "check_ram_usage", "result": [{"AvgTotalGB": 15.720000000001031, "AvgUsedGB": 10.102186288332874, "AvgFreeGB": 5.6178137116672575, "AvgUsedPercent": 64.26475149806092}]}}

```

# Integracja z AI / SolveDesk

Agent może być wykorzystywany przez systemy AI do automatycznej diagnostyki problemów zgłaszanych przez użytkowników.

Przykład:

```
Użytkownik: "Komputer działa bardzo wolno"

AI Agent:
1. check_cpu_usage
2. check_ram_usage
3. top_processes
4. check_disk_space
```

Na podstawie wyników agent może wygenerować diagnozę, np.:

```
Wysokie użycie CPU przez proces Chrome (85%)
Rekomendacja: zamknąć nieużywane karty przeglądarki.
```

---

# Roadmap

Planowane rozszerzenia:

* monitorowanie temperatury CPU
* monitorowanie GPU
* sprawdzanie usług Windows
* monitorowanie sieci
* integracja z WMI

---

Dominik Hofman
