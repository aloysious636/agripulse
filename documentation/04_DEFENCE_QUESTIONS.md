# Appendix A — Project Defence: 25 Questions and Answers

**A. Purpose and design choices**

**1. What problem does AgriPulse solve, and who is it for?**
Livestock farmers record events on paper, so vaccinations, pregnancy checks and weaning are missed, reproductive dates are worked out by hand, and costs are never linked to production. AgriPulse records each fact once and then calculates dates and indicators, raises alerts and produces reports. It is for smallholder and commercial farmers, farm managers, extension officers and animal science students.

**2. Why a desktop application instead of a web or mobile app?**
The requirement was offline-first operation on a farm computer. A desktop program needs no internet, no hosting cost and no subscription, and the data stays on the farm. A mobile or cloud version is listed as future work (with optional encrypted backup when internet is available).

**3. Why Flask, SQLite, Waitress and pywebview?**
Flask is small, well understood and lets the logic stay in Python, which an Animal Science student can read. SQLite is a reliable single-file relational database that needs no installation, ideal for one farm and easy to back up. Waitress is a production-grade pure-Python server that works on Windows. pywebview shows the local pages in a native window, so the user never opens a browser or starts a server. PyInstaller packages it all into a Windows program. React, Node, Django, FastAPI and cloud databases were excluded by the brief, and not needed.

**4. How is the code organised and why?**
Layers: routes (one blueprint per module) → services (business rules that touch the database) → calculations (pure formulas) → models (ORM). The application-factory pattern builds an isolated app per data folder, which is also what makes automated testing possible. Forms are declared once as lists of `Field` objects and a generic CRUD engine supplies validated create/edit/delete routes, so there is little duplicated code and no file over about 560 lines.

**5. Why separate the calculation engine from the database?**
Formulas then take plain inputs (dates, numbers, species parameters) and return a result. They can be unit-tested with exact values, read and checked by a non-programmer, and reused by the screens, alerts, calendar and reports so every part of the program gives the same answer.

**B. Database and data integrity**

**6. Describe the database design.**
27 tables and 46 foreign keys in SQLite, accessed through SQLAlchemy. Groups: reference data (species, breeds, categories, groups, settings), core (animals, weights, notifications), breeding (heat, service, pregnancy, birth), health and management (cases, treatments, vaccination/deworming, mortality, tasks), nutrition (feeds, stock movements, feeding records, schedules, rations, ingredients), production and finance. The ERD in section 13 is generated from the live schema so it cannot disagree with the software.

**7. How do you keep the data consistent?**
Foreign keys are enforced on every connection; unique constraints (tag, species, one weight per animal per day, one notification per key); every save is one transaction with rollback on error; server-side validation of types, ranges, dates and cross-field rules; and safe deletion — an animal with linked records, a parent with offspring, a feed with history or a species in use cannot be deleted, only archived or made inactive.

**8. How do animal tags stay unique, and why case-insensitive?**
The `tag_number` column has a UNIQUE constraint with `NOCASE` collation, and the form also checks it so the user sees a friendly message. "ab-12" and "AB-12" would otherwise look the same to a farmer but be different to the computer.

**9. Why do some records link to an animal *or* a group?**
Dairy and breeding stock are managed individually, but laying hens and broilers are managed as flocks. Records such as production, feeding, health and mortality therefore have nullable `animal_id` and `group_id`, and the forms require exactly one, so every record is linked to an identifiable animal or group as the brief requires.

**10. How do you evolve the database for existing users without losing data?**
`create_all()` adds missing tables; numbered migration steps recorded in `farm_settings.schema_version` handle later changes (ALTER TABLE etc.), applied once in order. A restore from an older backup is upgraded the same way, while a backup from a newer version is refused.

**C. Biology and calculations**

**11. How do you calculate the expected delivery date, and how is it species-specific?**
Expected delivery = service date + the gestation length stored for that species (cattle 283, goats 150, sheep 147, pigs 114, rabbits 31, chicken incubation 21 days by default). It is not applied across species; each species row holds its own parameters, editable in Settings. A manual override is allowed. Because the date is computed from the current species parameter rather than stored, changing the parameter recalculates dates. Calendar arithmetic handles leap years (tests confirm 1 Jan 2026 + 114 days = 25 April 2026 for pigs, and a 29 February birthday).

**12. How is the next heat predicted and what are the limits?**
Next heat = last heat observation or service + the species cycle length (cattle/goats 21 days, sheep 17, pigs 21). If that date has passed it is rolled forward by whole cycles. No prediction is made if the species has no regular cycle (rabbit, poultry), if the animal is already in an active pregnancy, or if the last observation is older than a configurable window (default 90 days). It is an estimate, labelled as a projection, because real cycles vary.

**13. Define conception rate and services per conception as the software does.**
Conception rate = (services that ended Pregnant, Delivered or Aborted) ÷ (those + services that ended Open) × 100. Services still *Pending* are excluded because their result is unknown. Services per conception = services with a known outcome ÷ conceptions. Example (tested): 2 conceptions and 1 open service give 66.7 % and 1.5.

**14. How do you measure growth and decide an animal is performing poorly?**
Average daily gain = (later weight − earlier weight) ÷ days between the weighings, using only recorded weights and dates; the birth weight is the first point of the series. Same-day or reversed dates return no value instead of a misleading number. The ADG is compared with the species' target (for example 700 g/day for cattle): at or above target is *On/above target*; at least 70 % of target (configurable) is *Slightly below*; below that is *Poor growth*; a negative ADG is *Weight loss*.

**15. How are the egg production percentage and feed conversion calculated?**
Hen-day production % = eggs collected ÷ birds in the flock that day × 100; the system rejects more eggs than birds. Feed conversion ratio = kg of feed ÷ kg of live-weight gain over the period, shown only when the gain is positive and there are at least two weighings. Dry matter intake is estimated as live weight × a species percentage and is clearly labelled a planning estimate.

**16. Where do the default biological values come from, and are they reliable?**
They are standard textbook planning values (for example cattle gestation about 283 days, sow 114 days, 21-day cattle cycle). They are generic, not breed- or region-specific, so they are shown in Settings and are editable; the documentation recommends review by an extension officer or veterinarian. Vaccination and deworming intervals are deliberately left blank because correct schedules depend on disease risk and region.

**17. Why does AgriPulse never give drug doses?**
Wrong doses harm animals and food safety. The brief forbids inventing veterinary advice, so the dosage field stores exactly what the veterinarian or label states, and the system only calculates *withdrawal end dates* from the days the user enters.

**D. Alerts, calendar and reports**

**18. How do notifications avoid duplicates and stale alerts?**
Each alert has a stable key (rule + record id). Evaluating the rules produces candidate alerts; an existing key is updated in place, a new key is created, and a stored alert whose condition no longer holds is auto-resolved. If a user resolves an alert while the condition persists it stays hidden; when the condition ends the stored row is removed so it can appear again later. Tests run the refresh repeatedly and confirm no duplicates.

**19. How is the calendar built, and does it store anything?**
Nothing extra is stored. Events are computed from the real records (services, heat, pregnancy checks, expected deliveries, vaccinations, deworming, weaning, tasks, withdrawal ends) each time, so the calendar always agrees with the data and cannot be out of date. Each event links to the record it came from.

**20. How are reports and exports produced?**
Each of the 13 reports is a function that returns one structure (title, columns, rows, summary). The same structure drives the screen preview, the CSV export and the PDF (made with ReportLab: A4, landscape if wide, farm header, repeated table header, page numbers). CSV is written with a byte-order mark so Excel reads accents correctly, and cells that begin with `=`, `+`, `-` or `@` are neutralised to prevent spreadsheet formula injection.

**E. Security, reliability and deployment**

**21. What security measures did you implement for a local program?**
The server listens on 127.0.0.1 only; every POST form carries a CSRF token (a test checks every form); a Content-Security-Policy forbids inline scripts and external resources; uploaded photos are verified by file signature and size and saved under random names; backup file names are whitelisted and zip entries are filtered against path traversal; SQL goes through the ORM; the secret key is generated per installation. There are no user accounts — access control relies on the Windows user account — which is stated as a limitation.

**22. How do backup and restore work and how do you know they are safe?**
Backup uses SQLite's online backup API for a consistent snapshot, zips it with a manifest and the photographs, and prunes old backups. Restore first validates the archive (is a zip, has the AgriPulse manifest, safe names, SQLite `integrity_check`, expected tables, schema not newer), then saves a safety backup of current data, replaces the database atomically and upgrades the schema. Tests cover normal restore, corrupt/foreign/malicious files (current data stays untouched), pruning and custom folders.

**23. How does the program start and stop as a desktop application?**
`desktop.py` takes a single-instance lock, creates the app, starts Waitress on a free local port, waits for the health check, opens the pywebview window, and when the window closes runs the optional automatic backup and stops the server. I found and fixed a shutdown race (an intermittent socket error) by making one thread own the server loop and closing sockets itself.

**F. Testing, honesty and future work**

**24. How did you test the system and what did you find?**
169 automated tests: calculation unit tests, workflow tests through the real HTTP routes (success and failure paths), security and offline tests, backup/restore, the real server and launcher flow, plus jsdom tests of the real JavaScript. PyInstaller built the spec and a frozen test executable served every page and PDF. Testing found real defects (listed in section 19) such as a template crash on filtered lists, an ambiguous database join, an alert-escalation bug, a shutdown race and a live preview that was missing from the form — all corrected.

**25. What are the limitations, and what would you do next?**
Honest limits: I could not run the Windows window or build the `.exe` in my environment, so a Windows verification checklist is provided; single user with no login; one farm per database; money stored as rounded floats; display units change only the display; growth is per individual animal; default biological values are generic; alerts are evaluated on use rather than by a background service. Next steps: optional user accounts, spreadsheet import, flock average weights, a Swahili interface, idle desktop notifications or SMS, pedigree and inbreeding tools, least-cost ration formulation, and a signed installer with updates.
