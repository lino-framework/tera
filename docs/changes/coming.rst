.. _tera.coming: 

================
Kommende Version
================

Allgemein:

- Einkaufsrechnungen und Kontoauszüge werden direkt in Lino erfasst.
- Verkaufsrechnungen werden noch mit TIM erstellt und ausgedruckt und
  dann aus TIM nach Lino importiert.

- Dienstleistungen (Termine und Anwesenheiten) werden aus TIM nach
  Lino importiert.  Ich kann auf Knopfdruck über Nacht neue Versionen
  aufspielen und alle Daten aus TIM nach Lino importieren.  Wir haben
  uns mündlich auf ein Entwicklerpasswort geeinigt, mit dem DD, LS, GV
  und HS sich während der Testphase einloggen können.  Alle anderen
  Benutzer wurden zwar erstellt, aber können sich nicht anmelden.

TODO:

- Lebensgruppen haben keine Teilnehmer

- Fallbeispiele von falsch importieren  
  
- "Arbeiten als"  zeigt auch den aktuellen User an.

- Übersetzung "Life groups"
- Professional situation : Liste übersetzen. "Homemaker" ersetzen
  durch "Housewife"?
- Problem Import Akte Melinda : Mitglieder in Familie sind doppelt. Es
  gibt nur eine Familientherapie, keine Einzeltherapie.
- DLS->IdUser wird scheinbar nicht importiert. Therapeut ist nicht
  immer der aus der Akte.

TALK  
  
- Preisliste :
  - course_line
  - entry_type
  - client_tariff
  - price
  - new_price?
    
- Gekoppelte Termine KITZ : wie regeln wir das?
- Termine mit zwei Therapeuten: einer der beiden ist nur "Assistent"
  und wird als Teilnehmer mit Rolle "Assistent" erfasst.
- Abrechnung an Krankenkassen
- Klären, wie die Securex-Rechnungen verbucht werden sollen.

- Die Kalenderfunktionen soll so gut werden, dass OpenExchange nicht
  mehr nötig ist.
  
- Fakturierung testen: in Lino Rechnungen machen lassen und schauen,
  ob sie mit der Wirklichkeit übereinstimmen.

- "endet um" kann bis auf weiteres leer sein
- Abonnements (eine Rechnung für alle Termine einer Therapie)
- Tagesplaner

- Terminplanung : Wochen-Master (Stundenplan), Monatsplaner (Wo sind
  Lücken? Ausnahmen regeln), Wochenansicht mit diversen
  Filtermöglichkeiten, Terminblätter drucken zum
  Verteilen. Zugewiesene Termine werden nicht angezeigt im Dashboard.

- Themen sind pro Familie und pro Klient, Notizen nur pro Klient.

- MTI Navigator can be irritating. Possibility to hide certain links &
  conversions. e.g. Person -> Houshold, Person -> Partner should be
  hidden for normal users.

