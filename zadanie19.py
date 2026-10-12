"""Zadanie 19: GitHub Projects dla justa8866/iris-ml-gitflow (Python + gh)."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "justa8866/iris-ml-gitflow"
OWNER = "justa8866"
TITLE = "Zadanie 19 - Iris ML Kanban"
HERE = Path(__file__).resolve().parent
STATE = HERE / "zadanie19_state.json"
JOURNAL = HERE / "zadanie19_history.jsonl"
STATUSES = ["Backlog", "To Do", "In Progress", "Review", "Done"]
STAGES = {
    "data": (
        "Data collection - dane Iris",
        [
            "Sprawdzić src/data.py: load_iris_frame().",
            "Potwierdzić 150 rekordów, 4 cechy i 3 gatunki.",
            "Sprawdzić kompletność danych i testy tests/test_data.py.",
            "Powiązać Issue z Pull Requestem dotyczącym ładowania danych.",
        ],
    ),
    "eda": (
        "EDA - eksploracyjna analiza Iris",
        [
            "Przejrzeć notebooks/01_iris_eda.ipynb oraz src/eda.py.",
            "Sprawdzić liczebności klas i statystyki cech według gatunku.",
            "Sprawdzić wykresy oraz tests/test_eda.py.",
            "Powiązać Issue z Pull Requestem dotyczącym EDA.",
        ],
    ),
    "preprocessing": (
        "Preprocessing - podział danych i skalowanie",
        [
            "Sprawdzić src/model.py: train_test_split(test_size=0.2, "
            "stratify=target, random_state=42).",
            "Potwierdzić StandardScaler wewnątrz Pipeline, "
            "dopasowany tylko na zbiorze treningowym.",
            "Sprawdzić brak przecieku danych i testy modelu.",
            "Powiązać Issue z Pull Requestem dotyczącym preprocessingu.",
        ],
    ),
    "modeling": (
        "Modeling - baseline Logistic Regression",
        [
            "Sprawdzić build_baseline_pipeline() i train_baseline() w src/model.py.",
            "Uruchomić python -m src.train.",
            "Potwierdzić zapis models/iris_logistic_regression.joblib "
            "i testy tests/test_model.py.",
            "Powiązać Issue z Pull Requestem dotyczącym treningu modelu.",
        ],
    ),
    "evaluation": (
        "Evaluation - ocena modelu Iris",
        [
            "Sprawdzić evaluate_model() w src/model.py.",
            "Zanotować accuracy oraz balanced_accuracy na odłożonym zbiorze testowym.",
            "Uruchomić python -m pytest -q i sprawdzić GitHub Actions.",
            "Powiązać Issue z Pull Requestem dotyczącym oceny modelu.",
        ],
    ),
    "deployment": (
        "Deployment - przygotowanie uruchomienia modelu",
        [
            "Wybrać sposób udostępnienia predykcji: "
            "CLI, API lub aplikacja demonstracyjna.",
            "Dodać ładowanie zapisanego modelu i walidację czterech cech wejściowych.",
            "Udokumentować instalację, uruchomienie i przykład predykcji.",
            "Sprawdzić odtwarzalność oraz udokumentować faktyczne wdrożenie.",
            "Powiązać Issue z Pull Requestem dotyczącym deploymentu.",
        ],
    ),
}


def gh(*args, payload=None, raw=False):
    command = ["gh", *map(str, args)]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(
        command,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    if raw:
        return result.stdout.strip()
    return json.loads(result.stdout) if result.stdout.strip() else None


def graphql(query, **variables):
    result = gh("api", "graphql", payload={"query": query, "variables": variables})
    if result.get("errors"):
        raise RuntimeError(json.dumps(result["errors"], ensure_ascii=False))
    return result["data"]


def save(state):
    temp = STATE.with_suffix(".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(STATE)


def log(event):
    from datetime import datetime, timezone

    event["time"] = datetime.now(timezone.utc).isoformat()
    with JOURNAL.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")


def load():
    if not STATE.exists():
        raise RuntimeError("Najpierw uruchom: python zadanie19.py setup")
    return json.loads(STATE.read_text(encoding="utf-8"))


def fields(state):
    data = gh(
        "project",
        "field-list",
        state["number"],
        "--owner",
        OWNER,
        "--limit",
        "100",
        "--format",
        "json",
    )
    return next(field for field in data["fields"] if field["name"] == "Status")


def move(state, stage, status):
    issue = state["issues"][stage]
    field = fields(state)
    option = next(opt for opt in field["options"] if opt["name"] == status)
    gh(
        "project",
        "item-edit",
        "--id",
        issue["item_id"],
        "--project-id",
        state["id"],
        "--field-id",
        field["id"],
        "--single-select-option-id",
        option["id"],
        raw=True,
    )
    old = issue.get("status")
    issue["status"] = status
    save(state)
    log({"action": "move", "stage": stage, "from": old, "to": status})
    print(f"{stage}: {old or '(brak statusu)'} -> {status}")


def board(state):
    """Create a saved board with Status columns via the official REST API."""
    data = graphql(
        "query($id:ID!){node(id:$id){... on ProjectV2{"
        "views(first:100){nodes{id name layout number}}}}}",
        id=state["id"],
    )
    boards = [
        v for v in data["node"]["views"]["nodes"] if v["layout"] == "BOARD_LAYOUT"
    ]
    if boards:
        state["board_url"] = state["url"] + "/views/" + str(boards[0]["number"])
        save(state)
        print("Widok Board już istnieje:", boards[0]["name"])
        print(state["board_url"])
        return
    rest_fields = gh(
        "api",
        f"users/{OWNER}/projectsV2/{state['number']}/fields",
        "-H",
        "X-GitHub-Api-Version: 2026-03-10",
    )
    status_id = next(f["id"] for f in rest_fields if f["name"] == "Status")
    result = gh(
        "api",
        f"users/{OWNER}/projectsV2/{state['number']}/views",
        "--method",
        "POST",
        "-H",
        "X-GitHub-Api-Version: 2026-03-10",
        payload={
            "name": "Kanban ML",
            "layout": "board",
            "filter": "",
            "vertical_group_by": [status_id],
        },
    )
    state["board_url"] = result.get("value", result)["html_url"]
    save(state)
    print("Utworzono widok Kanban:", state["board_url"])


def setup():
    gh("auth", "status", raw=True)
    login = gh("api", "user")["login"]
    if login != OWNER:
        raise RuntimeError(
            f"Zalogowano jako {login}; potrzebne konto {OWNER}. Użyj gh auth switch."
        )
    gh("api", f"repos/{REPO}")
    if STATE.exists():
        state = load()
    else:
        # Reuse an identically named project after an interrupted first run.
        projects = gh(
            "project", "list", "--owner", OWNER, "--limit", "100", "--format", "json"
        )["projects"]
        matches = [p for p in projects if p["title"] == TITLE]
        if len(matches) > 1:
            raise RuntimeError(
                "Więcej niż jeden projekt o tej nazwie; "
                "wybierz go ręcznie przed kontynuacją."
            )
        project = (
            matches[0]
            if matches
            else gh(
                "project",
                "create",
                "--owner",
                OWNER,
                "--title",
                TITLE,
                "--format",
                "json",
            )
        )
        state = {
            "id": project["id"],
            "number": project["number"],
            "url": project["url"],
            "issues": {},
        }
        save(state)
    gh("project", "link", state["number"], "--owner", OWNER, "--repo", REPO, raw=True)
    field = fields(state)
    if [opt["name"] for opt in field["options"]] != STATUSES:
        # The API replaces options and does not accept existing option IDs.
        # Never replace them on a populated project: that could reset statuses.
        items = gh(
            "project",
            "item-list",
            state["number"],
            "--owner",
            OWNER,
            "--limit",
            "1",
            "--format",
            "json",
        )
        if items["items"]:
            raise RuntimeError(
                "Projekt zawiera karty. Ustaw ręcznie opcje Status: "
                + ", ".join(STATUSES)
                + "; następnie ponów setup."
            )
        colors = ["GRAY", "BLUE", "YELLOW", "PURPLE", "GREEN"]
        options = []
        for name, color in zip(STATUSES, colors):
            option = {"name": name, "color": color, "description": name}
            options.append(option)
        graphql(
            "mutation($input: UpdateProjectV2FieldInput!) { "
            "updateProjectV2Field(input:$input) { clientMutationId } }",
            input={"fieldId": field["id"], "singleSelectOptions": options},
        )
    print(
        "W przeglądarce ustaw View > Layout > Board, "
        "kolumny według Status i zapisz widok."
    )
    all_issues = gh(
        "issue",
        "list",
        "--repo",
        REPO,
        "--state",
        "all",
        "--limit",
        "1000",
        "--json",
        "number,title,url",
    )
    for stage, (title, checks) in STAGES.items():
        if stage not in state["issues"]:
            full_title = "[Z19] " + title
            matches = [i for i in all_issues if i["title"] == full_title]
            if len(matches) > 1:
                raise RuntimeError(f"Niejednoznaczne Issue: {full_title}")
            if matches:
                issue = matches[0]
            else:
                body = (
                    f"## Etap projektu ML: {stage}\n\n"
                    "Issue utworzone do zadania 19. "
                    "Stan kodu należy zweryfikować przed oznaczeniem Done.\n\n"
                    "## Kryteria akceptacji\n\n"
                    + "\n".join("- [ ] " + check for check in checks)
                    + "\n\n## Workflow\n\n"
                    "Backlog → To Do → In Progress → Review → Done.\n"
                    "Done dopiero po zakończeniu prac, testach i zatwierdzeniu.\n"
                )
                issue = gh(
                    "api",
                    f"repos/{REPO}/issues",
                    "--method",
                    "POST",
                    payload={"title": full_title, "body": body},
                )
                issue["url"] = issue["html_url"]
            state["issues"][stage] = {"number": issue["number"], "url": issue["url"]}
            save(state)
        issue = state["issues"][stage]
        if not issue.get("item_id"):
            item = gh(
                "project",
                "item-add",
                state["number"],
                "--owner",
                OWNER,
                "--url",
                issue["url"],
                "--format",
                "json",
            )
            issue["item_id"] = item["id"]
            save(state)
        if not issue.get("status"):
            move(state, stage, "Backlog")
    print("\nUtworzono/skonfigurowano projekt i 6 Issues:", state["url"])
    print("W Board sprawdź Group by: Status i widoczność pustych kolumn.")
    report(state)


def link(state, stage, pr_number):
    issue = state["issues"][stage]
    pr = gh("api", f"repos/{REPO}/pulls/{pr_number}")
    if pr["state"] != "open":
        if not pr.get("merged_at"):
            raise RuntimeError(
                "Ten PR zamknięto bez scalenia. Wybierz otwarty lub scalony PR."
            )
        current = gh("api", f"repos/{REPO}/issues/{issue['number']}")
        body = current.get("body") or ""
        reference = f"Realizacja historyczna: {pr['html_url']}"
        if reference not in body:
            gh(
                "api",
                f"repos/{REPO}/issues/{issue['number']}",
                "--method",
                "PATCH",
                payload={"body": body + "\n\n" + reference + "\n"},
            )
        issue["pr"] = pr["html_url"]
        save(state)
        log(
            {
                "action": "link-history",
                "stage": stage,
                "issue": issue["url"],
                "pr": issue["pr"],
            }
        )
        print("Dodano odnośnik do scalonego PR:", issue["pr"])
        print(
            "To odnośnik historyczny; "
            "sprawdź powiązanie Development w Issue na GitHubie."
        )
        return
    marker = f"<!-- zadanie19:{stage} -->"
    body = pr.get("body") or ""
    if marker not in body:
        # The full URL is unambiguous. Existing PR descriptions remain intact.
        body += f"\n\n{marker}\nCloses {issue['url']}\n"
        gh(
            "api",
            f"repos/{REPO}/pulls/{pr_number}",
            "--method",
            "PATCH",
            payload={"body": body},
        )
    issue["pr"] = pr["html_url"]
    save(state)
    log({"action": "link", "stage": stage, "issue": issue["url"], "pr": issue["pr"]})
    print("Powiązano:", issue["url"], "->", issue["pr"])
    default_branch = gh("api", f"repos/{REPO}")["default_branch"]
    if pr["base"]["ref"] != default_branch:
        print(
            "Ten PR trafia do",
            pr["base"]["ref"],
            "— powiąż go również ręcznie przez Development w Issue.",
        )
    report(state)


def report(state):
    lines = [
        "# Zadanie 19 - GitHub Projects dla Iris ML",
        "",
        f"Projekt: {state['url']}",
        f"Repozytorium: https://github.com/{REPO}",
        "",
        "Kolumny: Backlog, To Do, In Progress, Review, Done.",
        "",
        "| Etap | Issue | Ostatni status ustawiony skryptem | PR |",
        "|---|---|---|---|",
    ]
    for stage, issue in state["issues"].items():
        lines.append(
            f"| {stage} | {issue['url']} | {issue.get('status', '')} | "
            f"{issue.get('pr', 'DO POWIĄZANIA')} |"
        )
    lines += [
        "",
        "Zmiany wykonane w przeglądarce mogą różnić się od lokalnego raportu.",
        "Historia operacji skryptu: zadanie19_history.jsonl.",
        "Do oddania dołącz zrzut faktycznej tablicy, "
        "link do projektu i powiązanych PR.",
    ]
    (HERE / "zadanie19_raport.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup")
    sub.add_parser("report")
    sub.add_parser("board")
    p = sub.add_parser("move")
    p.add_argument("stage", choices=STAGES)
    p.add_argument("status", choices=STATUSES)
    p = sub.add_parser("link")
    p.add_argument("stage", choices=STAGES)
    p.add_argument("pr", type=int)
    args = parser.parse_args()
    if not shutil.which("gh"):
        raise RuntimeError(
            "Brak GitHub CLI. Zainstaluj: winget install --id GitHub.cli --exact. "
            "Otwórz ponownie terminal."
        )
    if args.command == "setup":
        setup()
    else:
        state = load()
        if args.command == "move":
            move(state, args.stage, args.status)
        elif args.command == "link":
            link(state, args.stage, args.pr)
        elif args.command == "board":
            board(state)
        report(state)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, StopIteration, OSError) as error:
        print(
            f"Błąd: {error}\nStan zapisany obok skryptu. "
            "Po poprawieniu przyczyny ponów polecenie.",
            file=sys.stderr,
        )
        sys.exit(1)
