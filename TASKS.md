# Planned Improvements

## Deduplikacja treści QA/Quiz

1. Skonsolidowanie zduplikowanych pytań poprzez dodanie MapPageTaxonomy do powiązania pojedynczej strony QA lub Quiz z
   wieloma wpisami Taxonomy, zamiast wpis QA/Quiz per Taxonomy z jednym dowiazaniem MapPageTaxonomy.
2. Ponieważ wyświetlenie Quiz-u tylko z poprawną odpowiedzią może zastąpić QA. Należy usunięcie QA mających
   odpowiadający im Quiz po nazwie sprawdzając przy tym czy poprawna odpowiedź Quizu jest taka sama jak treść w QA.

## TIPTAP/ProseMirror

### Migracja page content

Należy materiały `Page.Content` w formacie HTML przerobić na dokument ProseMirror/TipTap.

### Własne elementy

- `quiz-block` (param: id) - po stronie aplikacji frontendowej w miejsce bloku zostanie pobrany i wyrenderowany quiz po
  wskazanym ID
- `page-link` (param: id, type: id_type) - po stronie aplikacji frontendowej w miejsce tekstu zostanie stworzony
  hyperlink do strony, po kliknięciu pojawia się popup ze stroną (np. postać, data)

### Migracja 'Zapamiętaj'

Zastąpienie statycznych sekcji „Zapamiętaj” zawierających listy pojęć, postaci i dat odwołaniami `page-link` do
istniejących wpisów z naszej bazy.

### Migracja Quiz

Migracja w niektórych materiałach quizów P/F w formie tabeli do interaktywnych Quizów. Zastąpienie statycznych tabel z
pytaniami typu „Prawda/Fałsz” w materiałach do nauki oraz wybranych lekcjach interaktywnymi komponentami Quiz
`quiz-block`, aby zwiększyć interaktywność treści.

## Users

### System kont użytkowników

Dodanie możliwości logowania do platformy oraz rejestracji użytkowników (zbieranie adresów e-mail) w celu personalizacji
doświadczenia i zapisywania postępów.

### Zapisywanie ulubionych i postępu czytania

Umożliwienie oznaczania materiałów jako ulubione („serduszka”) oraz automatyczne zapisywanie listy ostatnio czytanych
materiałów/sekcji materiału, aby użytkownik mógł łatwo wrócić do nauki.

### Zapisywanie postępów w quizach

Zapisywanie odpowiedzi udzielonych w quizach, aby umożliwić kontynuowanie rozpoczętych testów oraz prezentowanie
statystyk, takich jak procent poprawnych odpowiedzi dla poszczególnych rozdziałów.