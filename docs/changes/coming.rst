.. _tera.coming: 

================
Kommende Version
================

Allgemein:

- Vera übernimmt die Buchhaltung : Alle Einkaufsrechnungen und
  Kontoauszüge werden schon in Lino erfasst.  Verkaufsrechnungen
  werden in 2018 noch mit den beiden TIMs erstellt und ausgedruckt,
  aber daraufhin die jeweiligen Beträge manuell in Lino erfasst,
  evtl. in einem eigenen Journal (ähnlich wie OD), pro Serie von
  Rechnungen wird dort ein einziges Dokument erstellt.

- Auch die DLS und DLP aus TIM (Termine und Anwesenheiten) werden
  jetzt nach Lino importiert.  Ich kann auf Knopfdruck über Nacht neue
  Versionen aufspielen und alle Daten aus TIM nach Lino
  importieren. Wir haben uns mündlich auf ein Entwicklerpasswort
  geeinigt, mit dem DD, LS, GV und HS sich während der Testphase
  einloggen können.  Alle anderen Benutzer werden zwar erstellt, aber
  können sich nicht anmelden.

TODO:

- Lebensgruppen haben keine Teilnehmer?
- Problem Import Akte Melinda : Mitglieder in Familie sind doppelt. Es
  gibt nur eine Familientherapie, keine Einzeltherapie.
- Überfällige Termine : nicht schon die von heute, erst ab gestern.
- dashboard aktivieren
- users.UserDetail hat keine Reiter (Dashboard, event_type, ...)
- DLS->IdUser wird scheinbar nicht importiert. Therepeut ist nicht
  immer der aus der Akte.
- Wenn DLP->Status leer ist, dann soll in Lino Anwesend stehen.
- Terminzustand "Unentschuldigt ausgefallen" fehlt
- Anwesenheiten der Teilnehmer werden nur in therapeutischen Gruppen
  erfasst, bei Einzeltherapien und Lebensgruppen gelten immer alle als
  anwesend (werden ansonsten gelöscht).
- Gekoppelte Termine KITZ : wie regeln wir das?
- Termine mit zwei Therapeuten: einer der beiden ist nur "Assistent"
  und wird als Teilnehmer mit Rolle "Assistent" erfasst.
- Preisliste :
  - course_line
  - entry_type
  - client_tariff
  - price
  - new_price?
- "Arbeiten als"  zeigt auch den aktuellen User an.

- Übersetzung "Life groups"
- Professional situation : Liste übersetzen. "Homemaker" ersetzen
  durch "Housewife"?
 
TALK:

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

