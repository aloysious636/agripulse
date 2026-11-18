# 24. User Manual

## 24.1 Getting started

**Opening AgriPulse.** Double-click *AgriPulse.exe*. The window opens on the **Dashboard**. Everything works without internet.

**First-time set-up (5 minutes)**

1. **Settings ▸ Farm & formats** — enter your farm name, location, your name and phone. Check the date format, currency (KES by default) and whether you want weights shown in kg or lb.
2. **Settings ▸ Species parameters** — look at the numbers for the species you keep (gestation, heat cycle, weaning age, target growth). Ask your extension officer or veterinarian whether they suit your breed; change them if not. *These numbers drive every expected date and alert.*
3. **Settings ▸ Breeds** and **Production categories** — add breeds or categories you use that are missing.
4. **Animals ▸ Register animal** — add your first animal.

**The screen.** The green menu on the left opens the thirteen modules. The amber number next to *Notifications* is the count of unread alerts. Every list has a search/filter bar, an **Add** button, and **Edit** buttons on each row. Destructive actions always ask for confirmation. Messages appear at the top right; red messages mean nothing was saved and tell you why.

**Entering data.** Fields marked with a red * are required. Dates use the date picker. Enter weights in **kg** and milk in **litres** (display units can be changed in Settings but entry stays metric so records stay consistent).

## 24.2 Dashboard

Shows live figures from your records: registered animals (and by species, breed, sex and production category), breeding females, pregnant animals, animals due for service, overdue activities, net balance this month, expected births (next 60 days), upcoming activities (next 14 days by default), production over the last 30 days, income and expenditure for six months, services per month, recent health records and recent transactions. When there are no animals yet it shows a welcome message and zero counts — no sample or made-up figures are ever displayed. Click a figure to open the related list.

## 24.3 Animals

**Register an animal.** *Animals ▸ Register animal.* Required: ear tag / ID number (must be unique, upper/lower case are treated alike), species and sex. Recommended: breed, date of birth, production category, birth weight, current weight, dam, sire, acquisition details and a photograph. Tick **Used for breeding** for females you breed (this makes them eligible for "due for service" and heat predictions). If you enter a *purchase price*, an "Animal purchases" expense is added to Finance. A *current weight* is saved as a dated weight record.

The system rejects: duplicate tags; future birth dates; a breed from another species; a dam that is not female, a sire that is not male, parents of another species, parents born after their offspring, and circular family trees; photographs that are not real images or are larger than 5 MB.

**Find animals.** The filter bar searches tag, name, notes and source, and filters by species, breed, sex, status, category, group, breeding stock and *Missing information*. **Show** switches between active animals, sold/dead/exited, archived and everything. **Export CSV** downloads the filtered list.

**Animal profile.** Click a tag. Tabs: **Overview** (details, parents, offspring, reproductive status, growth snapshot, withdrawal warnings, upcoming events, linked records), **Breeding**, **Health**, **Management**, **Feeding**, **Production**, **Growth**, and **History** (a dated timeline of everything). Each tab has buttons to add records for this animal and Edit buttons that return you to the profile.

**Archive, sell, record death.**

* **Archive** hides an animal from active lists but keeps every record (use for animals you no longer manage). *Restore from archive* reverses it.
* **Sold / died / culled** opens *Record exit*: choose the reason and date. *Sold/Culled* with a price creates an "Animal sales" income; *Deceased* creates a mortality record; *Slaughtered* creates a slaughter record (enter live and carcass weights; dressing % is calculated). **Reactivate** reverses an exit.
* **Delete** (on the Edit page) is allowed only for an animal with no linked records, no offspring and no manual transactions. Otherwise you are told to archive it. This protects your history.

**Herds and flocks.** *Animals ▸ Herds / flocks ▸ New group* creates a group (for example "Layer flock A", 200 birds). Groups can be used for feeding, production, health, vaccination and mortality records. A group with data cannot be deleted; mark it inactive.

## 24.4 Breeding

Tabs: **Overview**, **Services**, **Heat records**, **Pregnancy exams**, **Births**.

* **Record heat** — animal, date observed, intensity, signs.
* **Record service** — animal (females only), service date, method (natural / AI), sire (registered male or an external bull/semen name), cost, outcome status. While you choose the animal and date the form previews the *expected delivery date*, the *expected next heat if not pregnant* and the *suggested pregnancy-check date* for that species. The expected delivery can be overridden. A service cost becomes a "Breeding" expense. An animal with a confirmed pregnancy cannot be served again until the outcome is recorded.
* **Record pregnancy examination** — pick the service, date, method and result. *Pregnant* → the service becomes **Pregnant**; *Not pregnant* → **Open**; *Inconclusive* → stays **Pending**.
* **Record birth** — dam, date, outcome, number born alive and dead, average birth weight. The birth is linked to the dam's open service automatically and the service becomes **Delivered** (an *Abortion* outcome makes it **Aborted**). The number of offspring must be plausible for the species (for example at most 3 for cattle). On the **Births** tab, **Register offspring** opens the animal form with dam, sire, species, date of birth and birth weight already filled in.

The **Overview** shows confirmed pregnant animals, due-for-service animals, pregnancy checks needed, expected deliveries with days remaining (red when overdue), expected heats in the next 21 days, the herd conception rate, and a table of reproductive performance per female: services, conceptions, conception rate, services per conception, births, average litter size, average birth interval and age at first service.

*Why is an animal "due for service"?* She is a mature female marked as breeding stock, not pregnant, the species' post-partum waiting period and heat-cycle length have passed since her last birth and last service. Animals with unknown age and no birth history are never listed because the system cannot tell.

## 24.5 Health

Tabs: **Health cases**, **Treatments**, **Vaccination & deworming**, **Due & overdue**, **Mortality**. Records can be for an individual animal or a group.

* **Health case** — date, disease/problem, symptoms, diagnosis, whether a veterinarian examined the animal, the veterinarian, recovery status and date, veterinary notes. Marking a case *Died* marks the animal as deceased.
* **Treatment** — medication, **dosage exactly as prescribed or printed on the label** (AgriPulse never suggests doses), route, duration, who administered it, **milk and meat withdrawal days**, cost. The *withdrawal end dates* are calculated and shown on the animal's profile, in the calendar and as an alert; a cost becomes a "Medication" expense.
* **Vaccination / deworming** — product, target, dose, batch, **next due date** (the calendar and alerts use it; if you leave it blank and a species interval exists in Settings, it is suggested). Recording a new dose of the same product replaces the old due date.
* **Due & overdue** lists scheduled vaccinations and deworming for the next 60 days and anything overdue.
* **Mortality** — deaths of animals or groups (a group's head count is reduced automatically).

## 24.6 Management (routine activities)

Tabs: **Upcoming**, **Overdue (n)**, **Completed**, **Cancelled**, **All**. **Schedule activity** needs an animal, a group *or a whole species*, the activity, date and priority (Low, Medium, High, Critical). Activities offered include castration, disbudding, dehorning, teeth clipping, iron supplementation, beak trimming, identification, weaning, hoof trimming, vaccination, deworming, dipping/tick control, body condition scoring, pregnancy examination, dry-off, shearing, weighing and other. **The system refuses activities that do not apply to the species** (for example disbudding a pig); *Other* is always allowed.

Row buttons: **Complete** (date and notes; if the task repeats, the next one is scheduled automatically), **Reschedule** (new date and reason, kept in the notes), **Cancel**. Overdue activities are shaded red and appear in alerts and the dashboard.

## 24.7 Nutrition and feeding

Tabs: **Feed inventory**, **Stock movements**, **Feeding records**, **Feeding schedules**, **Rations**, **Consumption & efficiency**.

1. **Add feed** — name, category, reorder level, cost per kg and (if you know them) dry matter %, crude protein % of dry matter and energy (ME). Opening stock creates the first stock movement.
2. **Stock movements** — record purchases (with cost per kg; tick *Record purchase as a Feed expense* to add it to Finance), adjustments and wastage. Stock can never go below zero.
3. **Record feeding** — animal or group, feed, quantity as fed. **Stock is deducted automatically**; if there is not enough you are told and nothing is saved. Editing or deleting a record gives the quantity back. For groups, per-animal quantity is calculated from the head count.
4. **Feeding schedules** — planned amount per feeding and feedings per day; the inventory estimates *days of stock* from active schedules.
5. **Rations** — create a ration, add ingredients (kg per animal per day) and read the analysis: as-fed kg, dry matter, crude protein % of DM, energy density, cost per day. Enter an animal's live weight to compare the ration's dry matter with the *estimated dry matter intake* (live weight × species DMI %). A warning lists feeds whose nutrient values are missing.
6. **Consumption & efficiency** — feed used per feed and cost for the period, and **feed conversion ratio** (kg feed per kg gain) for individually fed animals with at least two weighings.

## 24.8 Production

Tabs: **Summary**, **Daily records**, **Lactations**, **Meat & carcass**.

* **Milk** — enter morning and/or evening litres; the day's total is calculated. Only females can have milk records.
* **Eggs** — eggs collected, birds in the flock that day (taken from the group's head count if blank) and broken eggs; **production %** = eggs ÷ birds. Eggs cannot exceed the number of birds.
* **Other products** (wool/fibre, others) — quantity and unit.
* One record per animal/group, product and date (the system tells you to edit the existing one).
* **Lactations** — start (calving/kidding) and dry-off dates; days in milk, total, average and peak are calculated from that animal's milk records. An animal can have only one open lactation.
* **Meat & carcass** — slaughter date, live weight, carcass weight, grade; dressing % is calculated and the animal is marked slaughtered.
* **Summary** — choose 7, 30, 90 or 365 days: totals, averages, peak day, top milk producers, daily charts, average hen-day %, feed per dozen eggs.

## 24.9 Growth and weight monitoring

**Record weight** (animal, date, kg, method, optional body condition score 1–5). One weight per animal per day; dates before birth are refused. The animal's *current weight* is always the latest weighing. **Performance & comparison** lists each animal's previous and current weight, last gain, last ADG and overall ADG (grams/day) with a verdict against the species target: *On/above target*, *Slightly below target*, *Poor growth*, *Weight loss*. Tick animals and press **Compare selected** to draw their weights on one chart. **Poor performers only** filters the list. The poor-growth threshold (default 70 % of target) is in *Settings ▸ Alerts & assumptions*.

## 24.10 Calendar

Choose **Month**, **Week** or **Day**, move with the arrows and **Today**. Colours show the event type: heat, service, pregnancy check, expected delivery, birth, vaccination, deworming, weaning, management task and withdrawal end. Tick types to show only those, or **Hide completed**. Overdue items have a red outline; completed items are faded. Click any event to open the related record. Expected heat dates are *projections* (see section 17.2).

## 24.11 Notifications

Alerts have five levels: **Critical**, **High priority**, **Overdue**, **Upcoming**, **Informational**. Open **Notifications** to read them, click the title to open the related record, then **Read** or **Resolve**. *Resolve* hides an alert you have dealt with; if the situation changes it can come back. Alerts also resolve themselves automatically when the cause ends (for example a recorded birth ends the delivery alert) and are never duplicated. **Re-check now** forces a refresh; **Mark all read** clears the unread counter. Which alerts are produced and how many days ahead they warn is set in *Settings ▸ Alerts & assumptions*.

## 24.12 Finance

Tabs: **Transactions**, **Summary & charts**. **Add transaction**: type (Income/Expense), category (income: Milk, Eggs, Animal sales, Other livestock income; expense: Feed, Veterinary, Medication, Breeding, Labour, Animal purchases, Other expense), date, amount, enterprise, description, optional animal/group and counterparty. Transactions marked **Automatic** were created from another record (a feed purchase, treatment, vaccination, service fee, animal purchase or sale); change them by editing that record. Filter by date, type, category and enterprise. The summary shows total income, expenditure and net balance, monthly figures, expenditure by category and income by category and enterprise. **Export CSV** downloads the filtered transactions.

## 24.13 Reports and exports

*Reports* offers 13 reports: Animal inventory, Animal registration, Breeding, Reproductive performance, Health, Vaccination & deworming, Feeding, Production, Growth, Management activities, Financial, Upcoming tasks, Overdue activities. Choose one, set the filters (dates, species, animal where relevant) and press **Apply**. Use **Print**, **CSV** (opens in Excel) or **PDF** (A4, landscape when wide, farm name and date in the header, page numbers, header row repeated on every page).

## 24.14 Settings

* **Farm & formats** — farm and farmer details, date format, currency code and symbol, weight and volume display units.
* **Species parameters** — gestation/incubation, heat cycle, re-breeding wait, pregnancy-check day, minimum breeding age, weaning age, vaccination/deworming default intervals, dry matter intake %, target daily gain. *Add species* for any other animal (choose "Other" for *Behaves like*). Species in use cannot be deleted; mark them *not in use*.
* **Breeds** and **Production categories** — add, edit, delete (when unused).
* **Alerts & assumptions** — how many days ahead to warn, which alerts to produce, the heat-projection window, the poor-growth threshold and the dashboard window.
* **Backup & restore** — see next section.

## 24.15 Backup and restore

* **Create backup now** saves the database and all photographs in one `.zip` in the backup folder. Choose the folder (for example a USB drive such as `E:\AgriPulseBackups`) and how many backups to keep. With **Create a backup automatically when AgriPulse closes** ticked, every exit creates a backup.
* **Download**, **Restore** or **Delete** any listed backup, or **Restore from file** to use a backup copied from another computer.
* A restore **replaces all current data**. Before replacing anything AgriPulse validates the file and saves a *safety backup* of your current data (named `…beforerestore…`). If the file is invalid, nothing changes.

**Good practice:** keep the automatic backup on, and copy the backup folder to a USB drive every week.

## 24.16 Quick answers

| Question | Answer |
|---|---|
| I mistyped an ear tag | Edit the animal; the new tag must still be unique. |
| An animal was sold | Animal profile ▸ **Sold / died / culled** ▸ Sold ▸ enter price. |
| A cow lost a calf | Record a **birth** with outcome *Abortion* or *Stillbirth*, or record a pregnancy exam *Not pregnant*. |
| Why is the expected delivery different from my calendar? | The date uses the species gestation length in Settings (cattle 283 days); change the species value or override the date on the service. |
| Why is there no expected heat for my rabbit/hen? | These species have no regular cycle in the parameters, so no prediction is made. |
| I cannot delete an animal | It has records; **Archive** it instead. |
| A feeding record says not enough stock | Record the feed purchase first (Nutrition ▸ Stock movements). |
| Can AgriPulse tell me the dose? | No. It records exactly what your veterinarian or the label says. |
