const AgriPulse = {
    speciesList: [],
    animalsList: [],
    calendarCursor: new Date(),
    currency: 'KES',

    vaccinationSchedules: {
        "Poultry": [
            { minDays: 1, ageLabel: "Day 1 (Hatch)", disease: "Marek's Disease", vaccine: "Marek's HVT Vaccine", route: "Subcutaneous (Neck) at Hatchery", boosterDays: 0, boosterLabel: "Once in lifetime" },
            { minDays: 7, ageLabel: "Day 7 (Week 1)", disease: "Newcastle Disease (1st Dose)", vaccine: "NCD Hitchner B1 / LaSota", route: "Eye drop or Drinking water", boosterDays: 14, boosterLabel: "Boost at Day 21, then every 3 months" },
            { minDays: 10, ageLabel: "Day 10 - 14 (Week 2)", disease: "Gumboro / IBD (1st Dose)", vaccine: "IBD Intermediate Strain", route: "Drinking water (chlorine-free)", boosterDays: 10, boosterLabel: "2nd dose at Day 20-24" },
            { minDays: 14, ageLabel: "Day 14 (Week 2)", disease: "Infectious Bronchitis", vaccine: "IB H120 Vaccine", route: "Eye drop or Drinking water", boosterDays: 84, boosterLabel: "Boost at Week 14" },
            { minDays: 21, ageLabel: "Day 21 (Week 3)", disease: "Newcastle Disease (2nd Dose)", vaccine: "NCD LaSota", route: "Drinking water", boosterDays: 90, boosterLabel: "Every 3 months thereafter" },
            { minDays: 24, ageLabel: "Day 20 - 24 (Week 3-4)", disease: "Gumboro / IBD (2nd Dose)", vaccine: "IBD Intermediate / Hot Strain", route: "Drinking water", boosterDays: 0, boosterLabel: "Complete after 2nd dose" },
            { minDays: 42, ageLabel: "Week 6 (Day 42)", disease: "Fowl Pox", vaccine: "Fowl Pox Live Vaccine", route: "Wing-web stab", boosterDays: 365, boosterLabel: "Annual booster for layers/breeders" },
            { minDays: 56, ageLabel: "Week 8 (Day 56)", disease: "Fowl Typhoid", vaccine: "Live Fowl Typhoid 9R", route: "Intramuscular (Thigh/Breast)", boosterDays: 180, boosterLabel: "Boost at Week 18 (Point of Lay)" },
            { minDays: 112, ageLabel: "Week 16 - 18 (Point of Lay)", disease: "Newcastle + IB + EDS", vaccine: "Inactivated Combined Layer Vaccine", route: "Intramuscular injection", boosterDays: 365, boosterLabel: "Protects throughout laying cycle" }
        ],
        "Cattle": [
            { minDays: 30, ageLabel: "1 Month & Older", disease: "East Coast Fever (ECF)", vaccine: "ITM Muguga Cocktail", route: "Subcutaneous (Below ear) + Oxytetracycline", boosterDays: 0, boosterLabel: "Once in a lifetime immunity" },
            { minDays: 90, ageLabel: "3 - 8 Months (Heifer Calves)", disease: "Brucellosis (Contagious Abortion)", vaccine: "Brucella S19 Vaccine", route: "Subcutaneous injection", boosterDays: 0, boosterLabel: "Single dose for female calves only" },
            { minDays: 120, ageLabel: "4 Months & Older", disease: "Foot and Mouth Disease (FMD)", vaccine: "Quadrivalent FMD Vaccine", route: "Subcutaneous injection", boosterDays: 180, boosterLabel: "Every 6 months" },
            { minDays: 120, ageLabel: "4 Months & Older", disease: "Lumpy Skin Disease (LSD)", vaccine: "LumpiVax / Neethling Strain", route: "Subcutaneous injection", boosterDays: 365, boosterLabel: "Every 12 months (Annually)" },
            { minDays: 180, ageLabel: "6 Months & Older", disease: "Anthrax & Blackquarter (Blanthax)", vaccine: "Combined Anthrax + BQ Vaccine", route: "Subcutaneous injection", boosterDays: 365, boosterLabel: "Every 12 months (Before rainy season)" },
            { minDays: 180, ageLabel: "6 Months & Older", disease: "Rift Valley Fever (RVF)", vaccine: "RVF Clone 13 / Smithburn", route: "Subcutaneous injection (Non-pregnant)", boosterDays: 365, boosterLabel: "Annually before heavy rains" }
        ],
        "Goats & Sheep": [
            { minDays: 14, ageLabel: "2 - 4 Weeks (Kids/Lambs)", disease: "Orf (Contagious Ecthyma)", vaccine: "Live Orf Scarification Vaccine", route: "Skin scarification (Inner thigh)", boosterDays: 365, boosterLabel: "Annual booster in endemic flocks" },
            { minDays: 42, ageLabel: "6 Weeks (Kids/Lambs)", disease: "Enterotoxemia (Pulpy Kidney) & Tetanus", vaccine: "Multivalent Clostridial (Covexin/Lambivac)", route: "Subcutaneous injection", boosterDays: 28, boosterLabel: "Boost 4 weeks later, then annually (or 1 mo pre-kidding)" },
            { minDays: 90, ageLabel: "3 Months & Older", disease: "Peste des Petits Ruminants (PPR)", vaccine: "Live Attenuated PPR Vaccine", route: "Subcutaneous injection", boosterDays: 1095, boosterLabel: "Every 3 years" },
            { minDays: 90, ageLabel: "3 Months & Older", disease: "Contagious Caprine Pleuropneumonia (CCPP)", vaccine: "Caprivax (Inactivated Mycoplasma)", route: "Subcutaneous (Goats)", boosterDays: 365, boosterLabel: "Every 6 to 12 months" },
            { minDays: 120, ageLabel: "4 Months & Older", disease: "Sheep & Goat Pox", vaccine: "Live Sheep/Goat Pox Vaccine", route: "Subcutaneous injection", boosterDays: 365, boosterLabel: "Every 12 months" },
            { minDays: 180, ageLabel: "6 Months & Older", disease: "Rift Valley Fever (RVF)", vaccine: "RVF Clone 13 Vaccine", route: "Subcutaneous injection", boosterDays: 365, boosterLabel: "Annually before heavy rains" }
        ],
        "Pigs": [
            { minDays: 3, ageLabel: "Day 3 (Piglets)", disease: "Piglet Anemia (Nutritional Prevention)", vaccine: "Iron Dextran 200mg Injection", route: "Intramuscular (Neck/Ham)", boosterDays: 11, boosterLabel: "Optional 2nd dose at Day 14" },
            { minDays: 21, ageLabel: "Week 3 - 4 (Weaning)", disease: "Mycoplasma Enzootic Pneumonia & Circovirus", vaccine: "PCV2 + Mycoplasma Vaccine", route: "Intramuscular injection", boosterDays: 180, boosterLabel: "Single or 2-dose weaner protocol" },
            { minDays: 56, ageLabel: "Week 8 (2 Months)", disease: "Swine Erysipelas", vaccine: "Erysipelas Bacterin / Live Vaccine", route: "Intramuscular / Subcutaneous", boosterDays: 180, boosterLabel: "Boost 3 weeks later, then every 6 months" },
            { minDays: 180, ageLabel: "6 Months (Gilts 2-4 wks pre-service)", disease: "Porcine Parvovirus + Leptospirosis", vaccine: "Parvo-Lepto-Ery (FarrowSure)", route: "Intramuscular injection", boosterDays: 150, boosterLabel: "Before every breeding cycle" }
        ],
        "Rabbits": [
            { minDays: 35, ageLabel: "5 - 6 Weeks (Weaners)", disease: "Rabbit Hemorrhagic Disease (RHDV1 & 2)", vaccine: "Filavac / Eravac Inactivated Vaccine", route: "Subcutaneous injection", boosterDays: 365, boosterLabel: "Every 12 months" },
            { minDays: 42, ageLabel: "6 Weeks & Older", disease: "Pasteurellosis (Snuffles)", vaccine: "Pasteurella multocida Bacterin", route: "Subcutaneous injection", boosterDays: 180, boosterLabel: "Every 6 months in breeding does/bucks" }
        ]
    },

    async init() {
        this.bindNavigation();
        this.setDefaultDates();
        await this.refreshAll();
    },

    bindNavigation() {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
                btn.classList.add('active');
                const view = btn.dataset.view;
                document.getElementById(`view-${view}`).classList.add('active');
                document.getElementById('view-title').textContent = btn.textContent.replace(/[0-9]/g, '').trim();
            });
        });
    },

    setDefaultDates() {
        const today = new Date().toISOString().split('T')[0];
        document.querySelectorAll('input[type="date"]').forEach(inp => {
            if (!inp.value && inp.name && !['actual_delivery_date', 'next_due_date', 'heat_date'].includes(inp.name)) {
                inp.value = today;
            }
        });
    },

    toast(msg, isError = false) {
        const c = document.getElementById('toast-container');
        const el = document.createElement('div');
        el.className = `toast ${isError ? 'error' : ''}`;
        el.textContent = msg;
        c.appendChild(el);
        setTimeout(() => el.remove(), 3500);
    },

    async api(url, options = {}) {
        const res = await fetch(url, options);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Operation failed');
        return data;
    },

    async refreshAll() {
        try {
            await this.loadSpeciesAndSettings();
            await Promise.all([
                this.loadDashboard(),
                this.loadAnimals(),
                this.loadBreeding(),
                this.loadHealth(),
                this.loadTasks(),
                this.loadNutrition(),
                this.loadProduction(),
                this.loadWeights(),
                this.loadCalendar(),
                this.loadNotifications(),
                this.loadFinance(),
                this.loadBackups()
            ]);
        } catch (err) {
            this.toast(err.message, true);
        }
    },

    async loadSpeciesAndSettings() {
        const [species, settings] = await Promise.all([
            this.api('/api/species'),
            this.api('/api/settings')
        ]);
        this.speciesList = species;
        this.currency = settings.currency || 'KES';
        document.getElementById('currency-badge').textContent = this.currency;
        document.getElementById('sidebar-farm-name').textContent = settings.farm_name || 'AgriPulse';

        document.getElementById('set-farm-name').value = settings.farm_name || '';
        document.getElementById('set-location').value = settings.location || '';
        document.getElementById('set-owner').value = settings.owner_name || '';
        document.getElementById('set-currency').value = this.currency;
        document.getElementById('set-lead-days').value = settings.lead_alert_days || 7;

        const spSelect = document.getElementById('animal-species-select');
        const filterSp = document.getElementById('filter-animal-species');
        spSelect.innerHTML = species.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        filterSp.innerHTML = '<option value="">All Species</option>' + species.map(s => `<option value="${s.id}">${s.name}</option>`).join('');

        const spBody = document.querySelector('#species-config-table tbody');
        spBody.innerHTML = species.map(s => `
            <tr>
                <td><strong>${s.name}</strong></td>
                <td><input type="number" id="sp-gest-${s.id}" value="${s.gestation_days}" style="width:70px"></td>
                <td><input type="number" id="sp-est-${s.id}" value="${s.estrous_cycle_days}" style="width:70px"></td>
                <td><input type="number" id="sp-preg-${s.id}" value="${s.pregnancy_check_days}" style="width:70px"></td>
                <td><input type="number" id="sp-wean-${s.id}" value="${s.weaning_days}" style="width:70px"></td>
                <td><input type="number" step="0.1" id="sp-dmi-${s.id}" value="${s.dmi_pct_body_weight}" style="width:70px"></td>
                <td>${s.default_production_system}</td>
                <td><button class="btn btn-sm btn-primary" onclick="AgriPulse.saveSpeciesParam(${s.id})">Update</button></td>
            </tr>
        `).join('');
    },

    async saveSpeciesParam(id) {
        try {
            await this.api(`/api/species/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    gestation_days: document.getElementById(`sp-gest-${id}`).value,
                    estrous_cycle_days: document.getElementById(`sp-est-${id}`).value,
                    pregnancy_check_days: document.getElementById(`sp-preg-${id}`).value,
                    weaning_days: document.getElementById(`sp-wean-${id}`).value,
                    dmi_pct_body_weight: document.getElementById(`sp-dmi-${id}`).value
                })
            });
            this.toast('Species biological parameters updated');
        } catch (e) { this.toast(e.message, true); }
    },

    async loadDashboard() {
        const d = await this.api('/api/dashboard');
        const k = d.kpis;
        document.getElementById('nav-alert-badge').textContent = k.active_alerts_count;

        const kpiItems = [
            ['Active Livestock', k.total_animals],
            ['Breeding Females', k.active_breeding_females],
            ['Pregnant Animals', k.pregnant_animals],
            ['Due for Service', k.due_for_service],
            ['Expected Births', k.expected_births],
            ['Upcoming Tasks', k.upcoming_tasks],
            ['Overdue Tasks', k.overdue_tasks],
            ['30d Milk (L)', k.milk_30d],
            ['30d Eggs', k.eggs_30d],
            [`Net Balance (${this.currency})`, k.net_balance.toLocaleString()]
        ];
        document.getElementById('dashboard-kpis').innerHTML = kpiItems.map(([label, val]) => `
            <div class="kpi-card"><span>${label}</span><strong>${val}</strong></div>
        `).join('');

        const alertBox = document.getElementById('dashboard-alerts-list');
        alertBox.innerHTML = d.top_alerts.length ? d.top_alerts.map(a => `
            <div class="alert-item ${a.severity.split(' ')[0]}">
                <div>
                    <strong>[${a.severity}] ${a.title}</strong>
                    <div style="font-size:12px; color:#475569;">${a.message}</div>
                </div>
                <span style="font-size:11px; font-weight:600;">${a.due_date}</span>
            </div>
        `).join('') : '<p style="color:#64748b;">No urgent alerts. All scheduled activities are on track.</p>';

        document.querySelector('#dash-health-table tbody').innerHTML = d.recent_health.map(h => `
            <tr><td>${h.event_date}</td><td><strong>${h.tag_number}</strong></td><td>${h.record_type}</td><td>${h.disease_or_condition}</td><td>${h.recovery_status}</td></tr>
        `).join('') || '<tr><td colspan="5">No health events recorded yet.</td></tr>';

        document.querySelector('#dash-finance-table tbody').innerHTML = d.recent_transactions.map(t => `
            <tr><td>${t.transaction_date}</td><td>${t.transaction_type}</td><td>${t.category}</td><td>${this.currency} ${t.amount.toLocaleString()}</td></tr>
        `).join('') || '<tr><td colspan="4">No transactions recorded yet.</td></tr>';

        this.drawBarChart('chart-species', d.distributions.by_species, '#059669');
        this.drawLineChart('chart-milk-trend', d.milk_trend.map(m => m.date), d.milk_trend.map(m => m.yield));
        this.drawBarChart('chart-expenses', d.distributions.expense_by_category, '#d97706');
    },

    async loadAnimals() {
        const search = document.getElementById('filter-animal-search').value;
        const sp = document.getElementById('filter-animal-species').value;
        const st = document.getElementById('filter-animal-status').value;

        const animals = await this.api(`/api/animals?search=${encodeURIComponent(search)}&species_id=${sp}&status=${st}`);
        this.animalsList = animals;

        const tbody = document.querySelector('#animals-table tbody');
        tbody.innerHTML = animals.map(a => `
            <tr>
                <td><strong>${a.tag_number}</strong></td>
                <td>${a.name || '-'}</td>
                <td>${a.species_name}</td>
                <td>${a.breed}</td>
                <td>${a.sex}</td>
                <td>${a.age_info.display}</td>
                <td>${a.current_weight ? a.current_weight + ' kg' : '-'}</td>
                <td>${a.production_category}</td>
                <td><span class="${a.status === 'Active' ? 'tag-emerald' : 'tag-amber'}">${a.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="AgriPulse.openAnimalProfile(${a.id})">Profile</button>
                    ${a.status === 'Active' ? `<button class="btn btn-sm btn-outline" onclick="AgriPulse.archiveAnimal(${a.id})">Archive</button>` : ''}
                </td>
            </tr>
        `).join('') || '<tr><td colspan="10">No livestock records match the current filters.</td></tr>';

        const allActive = await this.api('/api/animals?status=Active');
        const females = allActive.filter(a => a.sex === 'Female');
        document.getElementById('breeding-animal-select').innerHTML = females.map(a => `<option value="${a.id}">${a.tag_number} (${a.species_name})</option>`).join('');
        const allOptions = allActive.map(a => `<option value="${a.id}">${a.tag_number} - ${a.name || a.species_name}</option>`).join('');
        document.getElementById('health-animal-select').innerHTML = allOptions;
        document.getElementById('weight-animal-select').innerHTML = allOptions;
        document.getElementById('task-animal-select').innerHTML = '<option value="">-- Group Activity --</option>' + allOptions;
        document.getElementById('feeding-animal-select').innerHTML = '<option value="">-- Herd / Group Ration --</option>' + allOptions;
        document.getElementById('prod-animal-select').innerHTML = '<option value="">-- Flock / Group --</option>' + allOptions;

        const vaxChecker = document.getElementById('vax-animal-checker');
        if (vaxChecker) {
            vaxChecker.innerHTML = '<option value="">-- Check Specific Animal by Age --</option>' + allOptions;
        }
        this.renderVaccinationGuide();

        if (allActive.length > 0) {
            this.loadGrowthChart(allActive[0].id);
        }
    },

    async submitAnimal(e) {
        e.preventDefault();
        try {
            const fd = new FormData(e.target);
            await this.api('/api/animals', { method: 'POST', body: fd });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Animal registered successfully');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async archiveAnimal(id) {
        if (!confirm('Archive this animal record? Historical logs will be preserved.')) return;
        await this.api(`/api/animals/${id}?mode=archive`, { method: 'DELETE' });
        this.toast('Animal archived');
        await this.refreshAll();
    },

    async openAnimalProfile(id) {
        const p = await this.api(`/api/animals/${id}`);
        document.getElementById('profile-modal-title').textContent = `${p.tag_number} — ${p.name || p.breed} (${p.species_name})`;
        document.getElementById('profile-modal-body').innerHTML = `
            <div class="grid-2col" style="margin-bottom:16px;">
                <div>
                    <p><strong>Sex:</strong> ${p.sex} | <strong>Age:</strong> ${p.age_info.display} (DOB: ${p.dob})</p>
                    <p><strong>Category:</strong> ${p.production_category} | <strong>Status:</strong> ${p.status}</p>
                    <p><strong>Lineage:</strong> Dam: ${p.dam_tag || 'N/A'} | Sire: ${p.sire_tag || 'N/A'}</p>
                    <p><strong>Weights:</strong> Birth: ${p.birth_weight || '-'} kg | Current: ${p.current_weight || '-'} kg</p>
                </div>
                <div>
                    ${p.photo_path ? `<img src="${p.photo_path}" style="max-height:110px; border-radius:6px;">` : ''}
                    <p><strong>Notes:</strong> ${p.notes || 'None'}</p>
                </div>
            </div>
            <h4>Breeding History (${p.breedings.length})</h4>
            <p style="font-size:12px; margin-bottom:10px;">${p.breedings.map(b => `Service: ${b.service_date} (${b.pregnancy_status}) → Expected: ${b.expected_delivery_date || '-'}`).join('<br>') || 'No breeding records.'}</p>
            <h4>Veterinary & Health History (${p.health_records.length})</h4>
            <p style="font-size:12px; margin-bottom:10px;">${p.health_records.map(h => `${h.event_date}: [${h.record_type}] ${h.disease_or_condition} - ${h.medication}`).join('<br>') || 'No health records.'}</p>
            <h4>Growth & Weight Records (${p.weight_records.length})</h4>
            <p style="font-size:12px;">${p.weight_records.map(w => `${w.measurement_date}: ${w.weight_kg} kg (ADG: ${w.adg_kg_per_day ?? '-'} kg/d)`).join(' → ') || 'No weight logs.'}</p>
        `;
        document.getElementById('animal-profile-modal').classList.remove('hidden');
    },

    closeModal(id) { document.getElementById(id).classList.add('hidden'); },

    async loadBreeding() {
        const rows = await this.api('/api/breeding');
        document.querySelector('#breeding-table tbody').innerHTML = rows.map(r => `
            <tr>
                <td><strong>${r.tag_number}</strong></td>
                <td>${r.species_name}</td>
                <td>${r.service_date || '-'}</td>
                <td>${r.service_method}</td>
                <td>${r.expected_next_heat || '-'}</td>
                <td>${r.preg_check_date || '-'}</td>
                <td><strong>${r.expected_delivery_date || '-'}</strong></td>
                <td>${r.days_remaining !== null ? r.days_remaining + ' d' : '-'}</td>
                <td><span class="${r.pregnancy_status === 'Confirmed' ? 'tag-emerald' : 'tag-amber'}">${r.pregnancy_status}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="AgriPulse.quickUpdateBreeding(${r.id}, 'Confirmed')">Confirm Preg</button>
                    <button class="btn btn-sm btn-primary" onclick="AgriPulse.quickUpdateBreeding(${r.id}, 'Delivered')">Mark Delivered</button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="10">No breeding records logged yet.</td></tr>';
    },

    async submitBreeding(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/breeding', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Breeding event saved and gestation calculated');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async quickUpdateBreeding(id, status) {
        const body = { pregnancy_status: status };
        if (status === 'Delivered') {
            body.actual_delivery_date = new Date().toISOString().split('T')[0];
            body.offspring_count = 1;
        }
        await this.api(`/api/breeding/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        this.toast(`Breeding status updated to ${status}`);
        await this.refreshAll();
    },

    async loadHealth() {
        const rows = await this.api('/api/health');
        document.querySelector('#health-table tbody').innerHTML = rows.map(r => `
            <tr>
                <td>${r.event_date}</td>
                <td><strong>${r.tag_number}</strong></td>
                <td>${r.record_type}</td>
                <td>${r.disease_or_condition}</td>
                <td>${r.medication || '-'} (${r.dosage || '-'})</td>
                <td>${r.withdrawal_end_date || 'None'}</td>
                <td>${r.next_due_date || '-'}</td>
                <td>${r.recovery_status}</td>
                <td>${this.currency} ${r.cost.toLocaleString()}</td>
            </tr>
        `).join('') || '<tr><td colspan="9">No veterinary records logged yet.</td></tr>';
        await this.renderVaccinationGuide();
    },

    async submitHealth(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/health', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Health record saved');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async renderVaccinationGuide() {
        const spSelect = document.getElementById('vax-species-filter');
        const animalSelect = document.getElementById('vax-animal-checker');
        const banner = document.getElementById('vax-animal-banner');
        const tbody = document.querySelector('#vax-guide-table tbody');
        if (!spSelect || !tbody) return;

        let selectedAnimal = null;
        let animalHealthLogs = [];

        if (animalSelect && animalSelect.value) {
            selectedAnimal = await this.api(`/api/animals/${animalSelect.value}`);
            animalHealthLogs = selectedAnimal.health_records || [];
            const spName = selectedAnimal.species_name;
            if (spName.includes('Goat') || spName.includes('Sheep')) spSelect.value = 'Goats & Sheep';
            else if (this.vaccinationSchedules[spName]) spSelect.value = spName;

            banner.style.display = 'block';
            banner.innerHTML = `<strong>Checking Immunization Card for:</strong> ${selectedAnimal.tag_number} (${selectedAnimal.name || selectedAnimal.breed}) — <strong>Age:</strong> ${selectedAnimal.age_info.display} (${selectedAnimal.age_info.total_days} days old, Born: ${selectedAnimal.dob})`;
        } else if (banner) {
            banner.style.display = 'none';
        }

        const schedule = this.vaccinationSchedules[spSelect.value] || [];
        tbody.innerHTML = schedule.map((item, idx) => {
            let statusHtml = '<span style="color:#64748b;">Select animal above to check</span>';
            if (selectedAnimal) {
                const ageDays = selectedAnimal.age_info.total_days;
                const alreadyDone = animalHealthLogs.find(h =>
                    h.record_type === 'Vaccination' &&
                    h.disease_or_condition.toLowerCase().includes(item.disease.split(' ')[0].toLowerCase())
                );
                if (alreadyDone) {
                    statusHtml = `<span class="tag-emerald">Administered (${alreadyDone.event_date})</span>`;
                } else if (ageDays >= item.minDays) {
                    statusHtml = `<span class="tag-red">Due / Eligible Now (Age ${ageDays}d >= ${item.minDays}d)</span>`;
                } else {
                    const daysLeft = item.minDays - ageDays;
                    const dueDt = new Date();
                    dueDt.setDate(dueDt.getDate() + daysLeft);
                    statusHtml = `<span class="tag-amber">Upcoming in ${daysLeft}d (${dueDt.toISOString().split('T')[0]})</span>`;
                }
            }

            return `
                <tr>
                    <td><strong>${item.ageLabel}</strong></td>
                    <td><strong>${item.disease}</strong></td>
                    <td>${item.vaccine}</td>
                    <td>${item.route}</td>
                    <td>${item.boosterLabel}</td>
                    <td>${statusHtml}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="AgriPulse.prefillVaccine('${spSelect.value}', ${idx})">
                            Log Vaccine
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    },

    prefillVaccine(speciesKey, idx) {
        const item = this.vaccinationSchedules[speciesKey][idx];
        const animalChecker = document.getElementById('vax-animal-checker');
        if (animalChecker && animalChecker.value) {
            document.getElementById('health-animal-select').value = animalChecker.value;
        }

        const setVal = (id, name, val) => {
            const el = document.getElementById(id) || document.querySelector(`#form-health [name="${name}"]`);
            if (el) el.value = val;
        };

        setVal('health-type-input', 'record_type', 'Vaccination');
        setVal('health-condition-input', 'disease_or_condition', item.disease);
        setVal('health-diagnosis-input', 'diagnosis', `Preventive Immunization (${item.ageLabel})`);
        setVal('health-med-input', 'medication', item.vaccine);
        setVal('health-dosage-input', 'dosage', item.route);
        setVal('health-status-input', 'recovery_status', 'Resolved');

        if (item.boosterDays > 0) {
            const nextDt = new Date();
            nextDt.setDate(nextDt.getDate() + item.boosterDays);
            setVal('health-nextdue-input', 'next_due_date', nextDt.toISOString().split('T')[0]);
        } else {
            setVal('health-nextdue-input', 'next_due_date', '');
        }

        document.getElementById('form-health').scrollIntoView({ behavior: 'smooth' });
        this.toast(`Pre-filled ${item.disease} vaccine in form above — click Save to record!`);
    },

    async loadTasks() {
        const rows = await this.api('/api/tasks');
        document.querySelector('#tasks-table tbody').innerHTML = rows.map(t => `
            <tr>
                <td>${t.scheduled_date}</td>
                <td><strong>${t.activity_name}</strong></td>
                <td>${t.tag_number}</td>
                <td>${t.species_name}</td>
                <td><span class="${t.priority === 'High' ? 'tag-red' : 'tag-amber'}">${t.priority}</span></td>
                <td>${t.status}</td>
                <td>${t.completion_date || '-'}</td>
                <td>
                    ${t.status === 'Pending' ? `
                        <button class="btn btn-sm btn-primary" onclick="AgriPulse.updateTaskStatus(${t.id}, 'Completed')">Complete</button>
                        <button class="btn btn-sm btn-outline" onclick="AgriPulse.updateTaskStatus(${t.id}, 'Cancelled')">Cancel</button>
                    ` : '-'}
                </td>
            </tr>
        `).join('') || '<tr><td colspan="8">No routine management tasks scheduled.</td></tr>';
    },

    async submitTask(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Routine task scheduled');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async updateTaskStatus(id, status) {
        await this.api(`/api/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        this.toast(`Task marked as ${status}`);
        await this.refreshAll();
    },

    async loadNutrition() {
        const [feeds, logs] = await Promise.all([
            this.api('/api/feeds'),
            this.api('/api/feeding-records')
        ]);

        document.getElementById('feeding-feed-select').innerHTML = feeds.map(f =>
            `<option value="${f.id}">${f.feed_name} (${f.quantity_kg} kg avail)</option>`
        ).join('');

        document.querySelector('#feed-inventory-table tbody').innerHTML = feeds.map(f => `
            <tr>
                <td><strong>${f.feed_name}</strong></td>
                <td>${f.category}</td>
                <td><span class="${f.quantity_kg <= f.reorder_level_kg ? 'tag-red' : 'tag-emerald'}">${f.quantity_kg} kg</span></td>
                <td>${f.reorder_level_kg} kg</td>
                <td>${this.currency} ${f.unit_cost_per_kg}</td>
                <td>${f.dry_matter_pct}%</td>
                <td>${f.crude_protein_pct}%</td>
                <td>${f.metabolizable_energy_mj}</td>
            </tr>
        `).join('') || '<tr><td colspan="8">Feed inventory is empty. Add feed stock above.</td></tr>';

        document.querySelector('#feeding-records-table tbody').innerHTML = logs.map(l => `
            <tr>
                <td>${l.feeding_date}</td>
                <td>${l.feed_name}</td>
                <td>${l.target}</td>
                <td>${l.animal_count}</td>
                <td>${l.quantity_kg} kg</td>
                <td>${l.nutrition ? l.nutrition.dm_per_head_kg + ' kg' : '-'}</td>
                <td>${l.nutrition ? l.nutrition.cp_per_head_g + ' g' : '-'}</td>
                <td>${l.nutrition ? l.nutrition.me_per_head_mj + ' MJ' : '-'}</td>
                <td>${this.currency} ${l.total_cost.toLocaleString()}</td>
            </tr>
        `).join('') || '<tr><td colspan="9">No feeding allocations recorded yet.</td></tr>';
    },

    async submitFeedStock(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/feeds', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.toast('Feed inventory updated');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async submitFeedingLog(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/feeding-records', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Feeding recorded and stock deducted');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async loadProduction() {
        const rows = await this.api('/api/production');
        document.querySelector('#production-table tbody').innerHTML = rows.map(r => {
            let metric = '-';
            if (r.laying_pct !== undefined) metric = `Laying Rate: ${r.laying_pct}%`;
            if (r.dressing_pct !== undefined) metric = `Dressing: ${r.dressing_pct}%`;
            return `
                <tr>
                    <td>${r.record_date}</td>
                    <td><strong>${r.tag_number}</strong></td>
                    <td>${r.production_type}</td>
                    <td>${r.morning_yield}</td>
                    <td>${r.evening_yield}</td>
                    <td><strong>${r.total_yield}</strong></td>
                    <td>${metric}</td>
                    <td>${r.quality_notes || '-'}</td>
                </tr>
            `;
        }).join('') || '<tr><td colspan="8">No production records entered yet.</td></tr>';
    },

    async submitProduction(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/production', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Production record saved');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async loadWeights() {
        const rows = await this.api('/api/weights');
        document.querySelector('#weights-table tbody').innerHTML = rows.map(w => `
            <tr>
                <td>${w.measurement_date}</td>
                <td><strong>${w.tag_number}</strong></td>
                <td>${w.previous_weight_kg !== null ? w.previous_weight_kg + ' kg' : '-'}</td>
                <td><strong>${w.weight_kg} kg</strong></td>
                <td>${w.weight_change_kg !== null ? (w.weight_change_kg >= 0 ? '+' : '') + w.weight_change_kg + ' kg' : '-'}</td>
                <td><span class="${w.adg_kg_per_day !== null && w.adg_kg_per_day < 0 ? 'tag-red' : 'tag-emerald'}">${w.adg_kg_per_day !== null ? w.adg_kg_per_day + ' kg/d' : '-'}</span></td>
                <td>${w.body_condition_score || '-'}</td>
                <td>${w.notes || '-'}</td>
            </tr>
        `).join('') || '<tr><td colspan="8">No weight measurements recorded yet.</td></tr>';
    },

    async loadGrowthChart(animalId) {
        if (!animalId) return;
        const rows = await this.api(`/api/weights?animal_id=${animalId}`);
        const chronological = rows.slice().reverse();
        this.drawLineChart(
            'chart-growth',
            chronological.map(r => r.measurement_date),
            chronological.map(r => r.weight_kg)
        );
    },

    async submitWeight(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/weights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            this.toast('Weight recorded and ADG calculated');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    async loadCalendar() {
        const events = await this.api('/api/calendar');
        const year = this.calendarCursor.getFullYear();
        const month = this.calendarCursor.getMonth();
        const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
        document.getElementById('calendar-month-label').textContent = `${monthNames[month]} ${year} — Farm Schedule`;

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        let html = '';
        for (let i = 0; i < firstDay; i++) {
            html += `<div class="cal-day" style="background:#f1f5f9;"></div>`;
        }
        for (let d = 1; d <= daysInMonth; d++) {
            const iso = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            const dayEvents = events.filter(e => e.date === iso);
            html += `
                <div class="cal-day">
                    <div class="cal-day-num">${d}</div>
                    ${dayEvents.map(ev => `
                        <div class="cal-event" style="background:${ev.color}" title="${ev.title}"
                             onclick="${ev.animal_id ? `AgriPulse.openAnimalProfile(${ev.animal_id})` : ''}">
                            ${ev.title}
                        </div>
                    `).join('')}
                </div>
            `;
        }
        document.getElementById('calendar-grid').innerHTML = html;
    },

    changeCalendarMonth(offset) {
        if (offset === 0) this.calendarCursor = new Date();
        else this.calendarCursor.setMonth(this.calendarCursor.getMonth() + offset);
        this.loadCalendar();
    },

    async loadNotifications() {
        const showRes = document.getElementById('toggle-resolved-alerts').checked;
        const alerts = await this.api(`/api/notifications?include_resolved=${showRes}`);
        document.getElementById('notifications-full-list').innerHTML = alerts.map(a => `
            <div class="alert-item ${a.severity.split(' ')[0]}">
                <div>
                    <strong>[${a.severity}] ${a.title}</strong> (${a.category})
                    <div style="font-size:12.5px;">${a.message} — Due: ${a.due_date}</div>
                </div>
                <div>
                    ${!a.is_resolved ? `<button class="btn btn-sm btn-outline" onclick="AgriPulse.resolveAlert('${a.alert_key}')">Mark Resolved</button>` : '<span class="tag-emerald">Resolved</span>'}
                </div>
            </div>
        `).join('') || '<p>No active notifications.</p>';
    },

    async resolveAlert(key) {
        await this.api('/api/notifications/resolve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ alert_key: key })
        });
        await this.refreshAll();
    },

    async loadFinance() {
        const data = await this.api('/api/finance');
        const s = data.summary;
        document.getElementById('finance-kpis').innerHTML = `
            <div class="kpi-card"><span>Total Farm Income</span><strong>${this.currency} ${s.total_income.toLocaleString()}</strong></div>
            <div class="kpi-card"><span>Total Farm Expenditure</span><strong>${this.currency} ${s.total_expense.toLocaleString()}</strong></div>
            <div class="kpi-card"><span>Net Farm Balance</span><strong>${this.currency} ${s.net_balance.toLocaleString()}</strong></div>
        `;
        document.querySelector('#finance-table tbody').innerHTML = data.transactions.map(t => `
            <tr>
                <td>${t.transaction_date}</td>
                <td><span class="${t.transaction_type === 'Income' ? 'tag-emerald' : 'tag-amber'}">${t.transaction_type}</span></td>
                <td>${t.category}</td>
                <td>${t.enterprise}</td>
                <td>${t.animal_tag || '-'}</td>
                <td>${t.payment_reference || '-'}</td>
                <td>${t.description || '-'}</td>
                <td><strong>${this.currency} ${t.amount.toLocaleString()}</strong></td>
            </tr>
        `).join('') || '<tr><td colspan="8">No financial transactions recorded.</td></tr>';
    },

    async submitFinance(e) {
        e.preventDefault();
        try {
            const payload = Object.fromEntries(new FormData(e.target).entries());
            await this.api('/api/finance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            e.target.reset();
            this.setDefaultDates();
            this.toast('Financial transaction recorded');
            await this.refreshAll();
        } catch (err) { this.toast(err.message, true); }
    },

    exportReport(format) {
        const type = document.getElementById('report-type').value;
        const start = document.getElementById('report-start').value;
        const end = document.getElementById('report-end').value;
        const url = `/reports/export?type=${type}&format=${format}&start_date=${start}&end_date=${end}`;
        window.open(url, '_blank');
    },

    async submitSettings(e) {
        e.preventDefault();
        const payload = Object.fromEntries(new FormData(e.target).entries());
        await this.api('/api/settings', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        this.toast('Farm settings updated');
        await this.refreshAll();
    },

    async loadBackups() {
        const list = await this.api('/api/backup');
        document.getElementById('backup-list').innerHTML = list.map(b => `
            <div class="alert-item">
                <div>
                    <strong>${b.filename}</strong>
                    <div style="font-size:11px;">Created: ${b.created_at} (${b.size_kb} KB)</div>
                </div>
                <div style="display:flex; gap:6px;">
                    <a class="btn btn-sm btn-outline" href="/api/backup/download/${b.filename}">Download</a>
                    <button class="btn btn-sm btn-primary" onclick="AgriPulse.restoreBackup('${b.filename}')">Restore</button>
                </div>
            </div>
        `).join('') || '<p style="font-size:12px; color:#64748b;">No backups created yet.</p>';
    },

    async TriggerBackup() {
        await this.api('/api/backup', { method: 'POST' });
        this.toast('Database backup created successfully');
        await this.loadBackups();
    },

    async restoreBackup(filename) {
        if (!confirm(`Restore farm database from ${filename}? Current unsaved changes will be replaced.`)) return;
        await this.api('/api/backup/restore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename })
        });
        this.toast('Database restored successfully');
        await this.refreshAll();
    },

    drawBarChart(canvasId, dataObj, color) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const labels = Object.keys(dataObj);
        const values = Object.values(dataObj);
        if (labels.length === 0) {
            ctx.fillStyle = '#64748b';
            ctx.font = '13px Segoe UI';
            ctx.fillText('No database records available to chart yet.', 120, 110);
            return;
        }

        const maxVal = Math.max(...values, 1);
        const pad = 35;
        const chartW = canvas.width - pad * 2;
        const chartH = canvas.height - pad * 2;
        const barW = Math.min(48, (chartW / labels.length) * 0.6);

        labels.forEach((lbl, idx) => {
            const val = values[idx];
            const h = (val / maxVal) * chartH;
            const x = pad + (idx * (chartW / labels.length)) + 12;
            const y = canvas.height - pad - h;

            ctx.fillStyle = color;
            ctx.fillRect(x, y, barW, h);

            ctx.fillStyle = '#1e293b';
            ctx.font = 'bold 11px Segoe UI';
            ctx.fillText(val, x + 4, y - 5);

            ctx.fillStyle = '#475569';
            ctx.font = '11px Segoe UI';
            ctx.fillText(lbl.substring(0, 10), x, canvas.height - 14);
        });
    },

    drawLineChart(canvasId, labels, values) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (!values || values.length === 0) {
            ctx.fillStyle = '#64748b';
            ctx.font = '13px Segoe UI';
            ctx.fillText('No time-series data recorded yet.', 140, 110);
            return;
        }

        const maxVal = Math.max(...values, 1);
        const pad = 35;
        const chartW = canvas.width - pad * 2;
        const chartH = canvas.height - pad * 2;

        ctx.strokeStyle = '#059669';
        ctx.lineWidth = 2.5;
        ctx.beginPath();

        values.forEach((val, idx) => {
            const x = pad + (idx / Math.max(values.length - 1, 1)) * chartW;
            const y = canvas.height - pad - (val / maxVal) * chartH;
            if (idx === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();

        values.forEach((val, idx) => {
            const x = pad + (idx / Math.max(values.length - 1, 1)) * chartW;
            const y = canvas.height - pad - (val / maxVal) * chartH;
            ctx.fillStyle = '#14532d';
            ctx.beginPath();
            ctx.arc(x, y, 3.5, 0, Math.PI * 2);
            ctx.fill();
            if (idx % 2 === 0 || values.length <= 7) {
                ctx.fillStyle = '#475569';
                ctx.font = '10px Segoe UI';
                ctx.fillText(labels[idx].slice(-5), x - 12, canvas.height - 12);
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => AgriPulse.init());