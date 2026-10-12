# Zadanie 19 — GitHub Projects dla Iris ML

Tablica istnieje na GitHubie, a karty to Issues z repozytorium.
Skrypt `zadanie19.py` tworzy projekt `Zadanie 19 - Iris ML Kanban`,
łączy go z `justa8866/iris-ml-gitflow`, tworzy sześć Issues z kryteriami
akceptacji i dodaje je do Backlog. Nie wymaga zmian w `.github/workflows/test.yml`.
Nie uruchamiaj go jako workflow CI: wykonuj polecenia lokalnie na swoim koncie.

## 1. Przygotowanie terminala

### Jeśli używasz Bash / UCRT64 (jak w terminalu Justyny)

Po instalacji GitHub CLI możesz udostępnić go w bieżącym terminalu bez restartu:

```bash
export PATH="/c/Program Files/GitHub CLI:$PATH"
gh --version
cd ~/Desktop/lesson03_tasks/iris-ml-gitflow
gh auth login --hostname github.com --web
gh auth refresh --hostname github.com --scopes project
../.venv/Scripts/python.exe zadanie19.py setup
```

Wykonuj polecenia kolejno i poczekaj na zakończenie logowania, zanim
uruchomisz następne. W Bash ścieżki zapisuj z `/`, bez prefiksu promptu `$`.
Jeśli wklejenie doda do polecenia `[200~`, anuluj linię przez Ctrl+C
i wpisz polecenie ręcznie.

### Jeśli używasz PowerShell

```powershell
cd C:\Users\Justyna\Desktop\lesson03_tasks\iris-ml-gitflow
winget install --id GitHub.cli --exact
```

Po instalacji zamknij i otwórz terminal ponownie. Zaloguj się na `justa8866`:

```powershell
gh auth login --hostname github.com --web
gh auth refresh --hostname github.com --scopes project
gh auth status
```

Uprawnienie `project` jest wymagane do zapisu Projects. Autoryzację wykonaj
w przeglądarce; tokenów nie wklejaj do plików ani czatu.

## 2. Utworzenie projektu i sześciu Issues

W tym workspace interpreter jest w nadrzędnym `.venv`:

```powershell
..\.venv\Scripts\python.exe zadanie19.py setup
```

Jeżeli masz aktywne inne środowisko Pythona, możesz użyć `python zadanie19.py setup`.
Skrypt wypisze link do projektu. Ponowne `setup` wykorzystuje zapisany stan
i Issues o tych samych tytułach. Zachowaj plik `zadanie19_state.json`.
Na zapełnionym projekcie skrypt nie zastępuje opcji Status; poprosi o ich
ręczne ustawienie, aby nie zgubić istniejących statusów.

## 3. Ustawienie widoku Kanban na GitHubie

Skrypt obsługuje również utworzenie zapisanego widoku przez API:

```bash
../.venv/Scripts/python.exe zadanie19.py board
```

Projekt Justyny ma już zapisany widok
[Kanban ML](https://github.com/users/justa8866/projects/2/views/2).
Polecenie `board` wykorzystuje istniejący Board, jeśli taki widok już jest.
Sprawdź w przeglądarce widoczność wszystkich pięciu kolumn; poniżej wariant ręczny.

1. Otwórz link wypisany przez skrypt.
2. W menu widoku ustaw Layout → Board.
3. Ustaw kolumny według pola Status.
4. Sprawdź kolejność: Backlog, To Do, In Progress, Review, Done.
5. Włącz widoczność pustych kolumn, jeśli są ukryte, i zapisz widok (Save).
6. W repozytorium w zakładce Projects sprawdź, czy projekt jest powiązany.

## 4. Powiązanie z dotychczasową pracą

Lokalna historia Git zawiera następujące scalone PR. Przed przypisaniem
sprawdź na GitHubie zakładkę Files changed i zakres każdego PR.
Jeden PR może realizować kilka etapów.

| Etap / argument skryptu | Dowód w repozytorium | Kandydat PR |
|---|---|---|
| Data collection / `data` | `src/data.py`, wbudowany zbiór Iris | #3, wydanie zawierające loader |
| EDA / `eda` | `src/eda.py`, `notebooks/01_iris_eda.ipynb` | #1 |
| Preprocessing / `preprocessing` | split i StandardScaler w `src/model.py` | #2 |
| Modeling / `modeling` | LogisticRegression, `src/train.py` | #2 |
| Evaluation / `evaluation` | accuracy, balanced accuracy, `tests/test_model.py` | #2 |
| Deployment / `deployment` | wymaga sposobu udostępniania predykcji | przyszły PR |

Przykład odnośnika do już scalonego PR:

```powershell
..\.venv\Scripts\python.exe zadanie19.py link eda 1
```

Dla scalonego PR skrypt dodaje do Issue odnośnik historyczny, bez zmiany
opisu PR. Nie jest to automatycznie powiązanie Development. W Issue otwórz
Development → wybierz repozytorium i PR → Apply. Jeśli GitHub nie pozwala
wybrać historycznego PR, zachowaj odnośnik jako dokumentację i użyj
Development dla przyszłego otwartego PR realizującego dane zadanie.

Dla otwartego PR polecenie `link` dopisuje `Closes` z adresem Issue do opisu PR.
Jeśli PR trafia do `develop`, dodaj również ręczne powiązanie Development.
Automatyczne zamknięcie przez `Closes` działa przy PR do domyślnej gałęzi.

## 5. Przenoszenie kart zgodnie z postępem

Backlog = zaplanowane; To Do = wybrane do pracy; In Progress = praca trwa;
Review = zmiany czekają na sprawdzenie; Done = spełnione kryteria i sprawdzona praca.
Możesz przeciągać karty na tablicy albo używać polecenia:

```powershell
..\.venv\Scripts\python.exe zadanie19.py move deployment "To Do"
```

Gdy faktycznie zaczniesz deployment, przenieś go do In Progress; po otwarciu
PR do Review; po testach i scaleniu do Done. Do Done nie przenoś go tylko
dlatego, że istnieje skrypt treningowy — trening nie udostępnia predykcji.

Dla już ukończonych etapów sprawdź kryteria Issue i testy, zaznacz odpowiednie
checkboxy, powiąż PR, zamknij Issue jako completed i ustaw Done.
Polecenie `move` zmienia wyłącznie kolumnę, nie zamyka Issue.
Nie trzeba mieć kart w każdej kolumnie ani pozorować historycznych przejść.

## 6. Co oddać

- Link do projektu i zrzut widoku Board z pięcioma kolumnami oraz sześcioma Issues.
- Linki do Issues i realizujących je PR; deployment otrzyma PR po implementacji.
- Krótkie wyjaśnienie rzeczywistego stanu etapów i pokazanie przesunięcia karty
  podczas faktycznej pracy.

`python zadanie19.py report` zapisuje `zadanie19_raport.md` obok skryptu.
Raport zawiera ostatnie statusy ustawione skryptem; zmiany przez przeglądarkę
sprawdzaj bezpośrednio na tablicy. `zadanie19_history.jsonl` zapisuje operacje
skryptu, nie pełną historię GitHuba.

Dokumentacja: [GitHub CLI Projects](https://cli.github.com/manual/gh_project),
[widok Board](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view),
[powiązania Issue–PR](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).
