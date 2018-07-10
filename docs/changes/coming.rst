.. _tera.coming: 

================
Kommende Version
================

Allgemein:

- Nächster Meilenstein ist, dass auch die DLS und DLP aus TIM (Termine
  und Anwesenheiten) nach Lino importiert werden und die
  Kalenderfunktionen erweitert werden.  En passant kann dann auch die
  Fakturierung getestet werden: in Lino Rechnungen machen lassen und
  schauen, ob sie mit der Wirklichkeit übereinstimmen.

- Wir beginnen bald mit der aktiven Testphase: Ich kann auf Knopfdruck
  über Nacht neue Versionen aufspielen und alle Daten aus TIM nach
  Lino importieren. Wir haben uns mündlich auf ein Entwicklerpasswort
  geeinigt, mit dem DD, LS, GV und HS sich während der Testphase
  einloggen können.  Alle anderen Benutzer werden zwar erstellt, aber
  können sich nicht anmelden.

- Buchhaltung wird von Vera übernommen : Alle Einkaufsrechnungen und
  Kontoauszüge werden schon in Lino erfasst.  Verkaufsrechnungen
  werden in 2018 noch mit den beiden TIMs erstellt und ausgedruckt,
  aber daraufhin die jeweiligen Beträge manuell in Lino erfasst in
  einem eigenen Journal (ähnlich wie OD), pro Serie von Rechnungen
  wird dort ein einziges Dokument erstellt.

TODO (Luc):

- Teilnehmer der Gruppentherapien scheinen überall zu fehlen.

- Kalendereintragsart ist leer.

- DLA aus TIM importieren nach cal.EventType (Kalendereintragsart).
  "Kalendereintragsart" ersetzen durch "Dienstleistungsart".

- client_state un tariff : nicht pro Client sondern pro Course
  
- Site.languages : auch EN und NL

- Alter : bei Kleinkindern auf z.B. "18 Monate"

- Professional situation : Liste übersetzen. "Homemaker" ersetzen
  durch "Housewife"?

- Doppelte Therapeuten in Auswahlfeld "Benutzer".
- Kein Standardpasswort für die anderen Benutzer.
  
- Terminplanung : Wochen-Master (Stundenplan), Monatsplaner (Wo sind
  Lücken? Ausnahmen regeln), Wochenansicht mit diversen
  Filtermöglichkeiten, Terminblätter drucken zum
  Verteilen. Zugewiesene Termine werden nicht angezeigt im Dashboard.

- cal.EntriesByCourse : Übersichtlicher gestalten.  Jahr anzeigen im
  Datum.  Im KITZ können mehrere Termine pro Tag stattfinden, an
  mehreren Tage pro Woche.  Im SPZ dagegen kommen manche nur 3x pro
  Jahr...

- Therapeutische Gruppen : Kolonnenlayout

- Termin erstellen von Therapie aus : geht nicht

- Idee (zu besprechen): Von einem neuen Klienten aus könnte man eine
  Aktion starten, die eine Notiz fürs Erstgespräch erstellt, wobei
  Lino dann falls nötig automatisch eine Aktivität erstellt.

- Notizen und Themen sind sehr vertraulich (nur für Therapeuten),
  Termine werden auch vom Sekretariat gesehen.
    
  Notizen und Themen müssen importiert werden aus TIM. Themen sind pro
  Familie und pro Klient, Notizen nur pro Klient.

- MTI Navigator can be irritating. Possibility to hide certain links &
  conversions. e.g. Person -> Houshold, Person -> Partner should be
  hidden for normal users.

- Übersetzung ClientStates : Statt "Zustand" eines Patienten "Stand
  der Beratung".

TODO (Vera)

- Partner, die seit Ende 2017 in TIM erstellt wurden, müssen auch in
  Lino erstellt werden.

DONE (to verify):

- No de GSM, Date naissance, Geschlecht n'ont pas été importés
- birth_date wird jetzt importiert
- Therapie E130280 : nicht Harry sondern Daniel müsste Therapeut
  sein. Falsch importiert. Lino nahm prioritär den T1 statt des T2.
  
- Rechnungsempfänger und Krankenkasse importieren : pro Patient, nicht
  pro Einschreibung.
  
- Akten E180246 und E180247 fehlen in Lino.

- Notizen sind nur bis November 2017 importiert worden

- Status der importierten Anwesenheiten war immer leer.  Status
  "Verpasst" heißt "abwesend" in Lino.


DONE and verified:

- Kindergruppe 2016 hat keine Therapie in Lino. Kindergruppe 2018
  fehlt komplett.  "Psychodrama Do 2018" hat Anwesenheiten pro
  Teilnehmer in TIM korrekt.

- Fakturationsadresse sichtbar machen in Ansicht Patient und Haushalt.
- Import Fakturationsadresse (Zahler) aus TIM scheint nicht zu funktionieren.
- Klientenkontaktarten : Liste füllen und auch Daten importieren aus
  TIM (z.B. Krankenkasse)

- nationality ist leer. Es fehlen viele Länder.
  
- Übersetzung Enrolment = "Teilnahme" (nicht "Einschreibung")
- NotesByPatient raus. Auch "Health situation" und zwei weitere
  Memofelder.
- Modul humanlinks raus, phones rein.
- "Alte Daten löschen" in TIM

  

Außerdem besprochen:

- Es wird eine Serie "virtueller Personen" geben, z.B. "Kaleido" : das
  bedeutet "irgendein Mitarbeiter von Kaleido, der als Vertreter
  fungiert". Wer das jeweils genau ist, wird nicht in Lino notiert.
  
- Raum einer Therapie (eines Termins)? Bleibt.
- Brauchen wir eine weitere Tabelle von "Anfragen" bzw. "Projekten"?
  Vorerst nicht.
  
- Notiz Erstgespräch (Create a note from patient without therapy) :
  Meine Idee ("Von einem neuen Klienten aus könnte man eine Aktion
  starten, die eine Notiz fürs Erstgespräch erstellt, wobei Lino dann
  falls nötig automatisch eine Aktivität erstellt") ist nicht
  nötig.  Stattdessen kommt NotesByPatient komplett raus. Notizen sieht
  man nur über die jeweilige Therapie.
  
- Pro Therapie gibt es einen verantwortlichen Therapeuten. Die
  "Disziplinen" im KITZ werden als unabhängige Therapien erfasst.  Das
  Erstgespräch bzw. die Testphase gilt ebenfalls als eine eigene
  Therapie.  Der Therapeut dieser Therapie ist zunächst auch
  Primärbegleiter.
