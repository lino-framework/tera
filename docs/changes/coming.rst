.. _tera.coming: 

================
Kommende Version
================

BEsprechungsbeginn 2018-10-09.
Release vorgesehen für 2018-11-05.

Kontext:

- Einkaufsrechnungen und Kontoauszüge werden direkt in Lino erfasst.
- Verkaufsrechnungen werden noch mit TIM erstellt und ausgedruckt und
  dann aus TIM nach Lino importiert.
- Buchhaltung 2018 wird parallel auch beim Steuerberater erfasst. Die
  Daten in Lino sind da, um zu überprüfen.

- Dienstleistungen (Termine und Anwesenheiten) werden aus TIM nach
  Lino importiert.  Ich spiele häufig neue Versionen auf und
  importiere dabei alle Daten aus TIM nach Lino.  Wir haben uns
  mündlich auf ein Entwicklerpasswort geeinigt, mit dem die Tester
  sich während der Testphase einloggen können.  Alle anderen Benutzer
  wurden zwar erstellt, aber können sich nicht anmelden.

DONE:

- Reihenfolge im Menü : "Therapien" steht jetzt an erster Stelle und
  erinnert schon so an die Akten aus TIM.  Ich möchte nachfragen, ob
  ihr wirklich das Wort "Akte" beibehalten wollt.  Therapie fände ich
  korrekter, weil es spezifischer ist.  Man könnte z.B. auch eine
  Patientenakte haben, die wäre was anderes als eine Therapie.

TODO:

- Lebensgruppen haben keine Teilnehmer

- Termine mit zwei Therapeuten: einer der beiden ist nur "Assistent"
  und wird als Teilnehmer mit Rolle "Cotherapeut" erfasst.  Für aus
  TIM importiere Termine stehen zwei Kalendereinträge in Lino. Diese
  könnten bei Bedarf automatisch gelöscht werden.
  
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
  
- Gekoppelte Termine : für bestimmte Therapien gilt, dass wenn ein
  Patient mehrer Termine hintereinander am gleichen Tag hat, diese für
  die Rechnung als ein einziger betrachtet werden.  Dieses Konzept
  wird überflüssig, falls wir monatliche Abo-Fakturierung einführen.
  
- Abrechnung an Krankenkassen
- Klären, wie die Securex-Rechnungen verbucht werden sollen.

- Die Kalenderfunktionen soll entweder (1) so gut werden, dass
  OpenExchange nicht mehr nötig ist oder (2) mit Kopano synchronisiert
  sein.
  
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

