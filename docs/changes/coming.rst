.. _tera.coming: 

================
Kommende Version
================

Besprechungsbeginn 2018-10-09.
Release vorgesehen für 2018-11-05.

Tagesordnung:

- Das, was wir am 2018-10-09 besprochen haben ist fast alles gemacht.
  Ich habe nicht jedes Detail hier dokumentiert, weil wir noch in der
  iterativen Entwicklungsphase sind.

- Dienstleistungen (Termine und Anwesenheiten) werden regelmäßig aus
  TIM nach Lino importiert.  In Lino sind sie bisher nur zum Spielen.
  Alle Änderungen in Lino gehen beim nächsten Import verloren.

- Statt "Therapie" sagt Lino jetzt "Akte", um beim etablierten
  Wortschatz bleiben. "Akten" steht jetzt an erster Stelle im Menü.

- Wir hatten ein Fallbeispiel "Kylie B hat ET in Lino, was nicht
  stimmt" gesehen. Das kommt, weil in TIM für Kylie ein PAR mit IdPrt
  P steht, weil sie ja als Kind in einer Lebensgruppe mitmacht. Aber
  woher soll Lino wissen, dass Kylie keine Einzeltherapie hat sondern
  nur als Kind einer anderen Therapie benutzt wird? Okay,
  normalerweise haben Personen, die in einer LG oder TG mitmachen,
  nicht auch noch eine Einzeltherapie... aber da gibt es bestimmt
  Ausnahmen. En attendant haben Fälle wie Kylie in Lino zwei
  Therapien.

- Therapien mit zwei Therapeuten : die haben zur Zeit noch alle
  Termine doppelt nach dem Import, weil in TIM jeder Therapeut seine
  DLS eingibt. Dubletten kann ich wahrscheinlich automatisch
  rausklamüsern, aber bin noch nicht sicher, ob das schwer ist. Zu
  klären, ob sich die Arbeit überhaupt lohnt.
  
- Wir haben gesagt, dass bei Akten mit zwei Therapeuten der
  Cotherapeut mit den Patienten in der Liste der Teilnehmer kommt.
  Ich bin noch nicht sicher, ob euch das gefällt.

Falls Zeit bleibt:  

- Momentan habt ihr nur eine Telefonnummer, GSM-Nr und E-Mail-Adresse
  pro Partner. In Lino könnte man auch mehrere "Kontaktdaten" pro
  Partner haben. Daniel und ich haben irgendwann im Juni mal
  "beschlossen", dass eine reicht. Nachteil von mehreren ist, dass die
  Bearbeitung dann anders funktioniert als aus TIM gewohnt. Man kann
  auch später von single-contact nach multi-contact wechseln, falls
  sich rausstellt, dass es Sinn macht.

- Could not import zahler 1025, 8, 15, 5, 22, 24

- Es gibt in TIM Akten mit ungültigem Tarif 0, 3, 33

Aussicht:

- Einkaufsrechnungen und Kontoauszüge werden direkt in Lino erfasst.
- Verkaufsrechnungen werden noch mit TIM erstellt und ausgedruckt und
  dann aus TIM nach Lino importiert.
- Buchhaltung 2018 wird parallel auch beim Steuerberater erfasst. Die
  Daten in Lino sind da, um zu überprüfen.

DONE:


TODO:

- Termine mit zwei Therapeuten: einer der beiden ist nur "Assistent"
  und wird als Teilnehmer mit Rolle "Cotherapeut" erfasst.  Für aus
  TIM importiere Termine stehen zwei Kalendereinträge in Lino. Diese
  könnten bei Bedarf automatisch gelöscht werden.
  
- "Arbeiten als"  zeigt auch den aktuellen User an.

- Professional situation : Liste übersetzen. "Homemaker" ersetzen
  durch "Housewife"?
  
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

