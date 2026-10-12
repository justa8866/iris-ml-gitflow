# Zadanie 18 — Zaawansowane Git: Cherry-pick i Stash

Wykonano w repozytorium `iris-ml-gitflow`. Data ukończenia: 11.10.2026.

## 1. Cherry-pick: przeniesienie jednego commita z brancha A na B

- Branch A: `feature-cherry-source`.
- Branch B: `feature-cherry-target`.
- Commit źródłowy: `7357e66` — `docs: add advanced Git operations exercise`.
- Commit na branchu B: `4fd7baf` — ta sama zmiana z nowym identyfikatorem.

Przebieg już wykonanej operacji:

```powershell
git switch feature-cherry-source
git log -1 --oneline
git switch feature-cherry-target
git cherry-pick 7357e66
git log -1 --oneline
```

Commit źródłowy dodał plik `docs/advanced_git_operations.md`. Cherry-pick
zastosował tę zmianę na branchu B. Przy dokończeniu zadania potwierdzono
obecność obu commitów na właściwych branchach oraz identyczną zawartość:

```powershell
git show --no-patch 7357e66
git show --no-patch 4fd7baf
git diff 7357e66 4fd7baf
```

Ostatnie polecenie nie zwróciło różnic. Cherry-pick przenosi zmianę z wybranego
commita; nie scala całej gałęzi. W tym ćwiczeniu powstał nowy commit `4fd7baf`.

## 2. Stash: zmiana brancha bez commitowania i odzyskanie pracy

Na `feature-cherry-target` rozpoczęto edycję tego dokumentu: dopisano hash
commita źródłowego i sekcję o stash. Zmiany zapisano tymczasowo bez commita:

```powershell
git stash push -m "docs: record stash recovery"
```

W chwili wznowienia zadania katalog roboczy był czysty, a `git stash list`
pokazywało zapis:

```text
stash@{0}: On feature-cherry-target: docs: record stash recovery
```

Sprawdzono zapisane zmiany, przełączono branch, wrócono i odzyskano pracę:

```powershell
git stash show -p 'stash@{0}'
git switch feature-cherry-source
git status --short
git switch feature-cherry-target
git stash pop
git diff -- docs/advanced_git_operations.md
git stash list
```

Wynik:

- Przełączenie na branch A i powrót na B zakończyły się powodzeniem.
- `git stash pop` przywróciło edycję dokumentu bez konfliktów.
- `git diff` pokazało odzyskany hash `7357e66` oraz sekcję o stash.
- Git potwierdził usunięcie wykorzystanego zapisu: `Dropped refs/stash@{0}`
  (hash zapisu: `f9d8189bb63cfde93c25a174f529c50bdac10a17`).
- Końcowe `git stash list` było puste.

Stash przechowuje niedokończoną pracę poza historią brancha, pozwalając zmienić
gałąź. `git stash pop` przywraca zmiany, a po udanym zastosowaniu usuwa zapis
ze stosu. Odzyskane zmiany pozostają niezatwierdzone, dopóki nie zrobimy commita.

## Rezultat

Oba wymagania zadania zostały wykonane. Dokumentację uzupełniono po odzyskaniu
zmian i zatwierdzono osobnym commitem na `feature-cherry-target`:

```powershell
git add docs/advanced_git_operations.md
git commit -m "docs: complete cherry-pick and stash exercise"
```
