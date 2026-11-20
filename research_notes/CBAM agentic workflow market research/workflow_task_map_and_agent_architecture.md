# CBAM Operational Workflow (2026 Definitive Period): Task Map and Agent Architecture for carbonTraceAI

Research date: 12 October 2026. Scope: post-Omnibus definitive regime (from 1 Jan 2026), producer (non-EU installation operator) and importer (authorised CBAM declarant) side, labour-intensive tasks suited to human-approved AI agents, and agent architecture patterns. Transitional-period (Oct 2023 to Dec 2025) specifics are flagged where they're used as evidence.

Source quality note: the Commission's official pages (taxation-customs.ec.europa.eu, EUR-Lex), DEHSt (the German national competent authority) and the Commission impact assessment are primary. Many of the 2026 process details only appear in vendor or consultant explainers (cbamguide.com, CBAM Pulse, Materia Intel, CarbonChain, etc.), and those vendors sell compliance tooling. Each finding below says which kind of source it comes from.

---

## Q1. Producer (installation operator) workflow: steps, rules, and which steps take the most time

### Takeaway
A non-EU operator's 2026 cycle has these steps: define the installation and production routes; document the monitoring methodology; collect activity data (fuels, electricity, precursors, outputs); calculate specific embedded emissions; optionally register in the O3CI portal and upload the data there; link a verifier and host a mandatory physical site visit in the first verification year; then share the data with each EU declarant. That last step needs each declarant's EORI number, exchanged outside the Registry. The work that takes the most effort is documentation and evidence assembly (boundary, monitoring method, source records, allocation choices) plus preparing for the verifier. The same verified dataset then has to reach several customers.

### Cited Findings

**Legal stack for the definitive period (operator side)**
- Actual embedded emissions must be monitored and recorded under the methods in Implementing Regulation (EU) 2025/2547 and verified by accredited verifiers under Implementing Regulation (EU) 2025/2546, with accreditation under 2025/2551. Default values are in Implementing Regulation (EU) 2025/2621, which is available in the registry. — [DEHSt, CBAM definitive regime 2026](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- Conflicting citation: one secondary guide calls 2025/2546 the delegated act. The EUR-Lex text points to Delegated Regulation 2025/2551 (Annex II, Section 2.12) for the site-visit requirement. Check against the Official Journal. — [EUR-Lex 2025/2546](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2546); [cbamguide.com implementing regulations list](https://cbamguide.com/learn/implementing-regulations/)
- The Commission has published definitive-period default values and benchmarks in Excel. The Excel file only covers the Annex I default values. It does not include, for example, default values for indirect emissions or electricity. — [Finnish Customs (Tulli)](https://tulli.fi/en/-/the-default-values-and-benchmarks-for-the-cbam-definitive-period-have-been-published-in-excel-format-there-are-also-new-guidance-videos-on-the-cbam-registry)
- Commission guidance on CBAM concepts shows a "first publication of this document for the definitive period" dated 14.08.2026. — [Guidance No. 1, Introduction to CBAM concepts (mirror on trungtamwto.vn)](https://trungtamwto.vn/download/24375/guidance-no.-1--introduction-to-cbam-concepts.pdf)

**Step 1–3: Installation boundary, monitoring methodology, activity data and records**
- A legal commentary on the Commission's 24 August 2026 verification guidance says non-EU producers should do the following: identify the specific installation, not just the corporate group; keep records covering the production boundary, fuel and electricity, inputs, outputs, process emissions, allocation choices, default values, any third-country carbon price paid, and the calculations sent to the verifier; and document the methodology clearly enough for an outside verifier to follow. — [Kohen Avocats, Aug/Sep 2026](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)
- The same source says operators should report process changes early, because they may require recalculation before the declaration deadline. It also says operators should keep actual emissions separate from default values and confirm that Registry information concerns the same installation and goods. — [Kohen Avocats](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)
- In the O3CI portal, operators enter each installation's annual emissions records once. The records cover production routes, goods, direct and indirect emissions, and any carbon price effectively paid in the country of production. — [Materia Intel, O3CI operator/verifier portal](https://www.materiaintel.com/insight/cbam_registry_o3ci_operator_verifier_portal)

**Step 4: Communication Template (Excel)**
- The ICC says the installation guide and the "communication template" are too complicated for most suppliers. It also says the information the law requires differs from what the CBAM Excel sheet asks for. Importers concentrate on completing the sheet, while exporters concentrate on the legal requirements. — [ICC open letter on CBAM](https://iccwbo.org/news-publications/statement-letters/open-letter-on-the-carbon-border-adjustment-mechanism-cbam/)
- A consultant writes that suppliers need patience and resources to learn the GHG methodology before they can fill in the template. — [Vis-map, Feb 2024 (transitional period)](https://vis-map.com/2024/02/26/getting-suppliers-installations-to-fill-cbam-communication-template/)
- The search did not turn up a confirmed definitive-period version of the Communication Template with an official download link (see Gaps).

**Step 5: CBAM Registry — O3CI portal (Operators of Third-Country Installations)**
- Third-country operators can register voluntarily in the O3CI portal, which is part of the CBAM registry. There they can provide emissions and company data directly to declarants, and their verification status is visible. Registration reduces manual data entry and makes actual values easier to use. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- In O3CI, non-EU operators upload installation and emissions data for reporting declarants, and declarants retrieve it through the "Emissions" tab. EU-established operators use the Authorisation Management Module (AMM) instead. Dated documents on the page: non-EU access request guidance (19 Feb 2026); O3CI forms and registration guides (24 Feb 2026); delegation of access rights guide (4 Jun 2026); user manual for the installation operators and verifiers portal (27 Aug 2026); verifier access/registration guidance and quick guide (28 Aug 2026); declarants portal user manual (21 Aug 2026). E-learning covers O3CI registration and request management (10 sessions), deregistration, and search/navigation. — [European Commission, CBAM Registry and reporting](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry-and-reporting_en)
- Access requests require a company registration certificate, proof of representation (such as a power of attorney) and the authorised representative's ID. The Commission's access-request guidance is dated January 2026 (v2.00). — [Commission, CBAM Third Countries Operators access request procedure (PDF)](https://taxation-customs.ec.europa.eu/document/download/9361fade-6f19-4799-b2ef-f6a4ff681af2_en?filename=CBAM-Operators-Non-EU-Companies-Guidance-on-access-request-procedure-v2.00.pdf); summarised in search results alongside the [technical user manual](https://taxation-customs.ec.europa.eu/document/download/bc281bd8-6cef-4859-97e2-590d563c08be_en?filename=CBAM+Registry+access+for+non-EU+installation+operators+%E2%80%93+technical+user+manual-v1.20-EN.pdf)
- The installation operators and verifiers portal manual is 146 pages, published 27 Aug 2026. The Registry applies format and plausibility checks, but a saved record is not a verified one. — [Materia Intel](https://www.materiaintel.com/insight/cbam_registry_o3ci_operator_verifier_portal)
- Sharing with declarants: the declarant must give the operator its EORI number outside the Registry. Without the correct EORI, the installation record may not reach the right EU customer. A future update is planned to let operators share with all interested declarants. — [Materia Intel](https://www.materiaintel.com/insight/cbam_registry_o3ci_operator_verifier_portal); search summary of [Commission CBAM Registry page](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry_en)

**Step 6: Verification (accredited verifier, site visits)**
- Physical site visits:
  - A physical site visit is required in all cases in the first year subject to verification.
  - From the second consecutive year, the verifier may switch to a virtual visit or waive the visit if specific criteria are met. A virtual visit requires a physical visit in the immediately preceding reporting period. A waiver requires physical visits in the two preceding reporting periods.
  - Physical visits should take place at least every two years.
  - A virtual visit can also replace a physical one when "serious, extraordinary and unforeseeable circumstances" prevent the physical visit.
  - The verifier's decision does not need competent-authority approval, but the verifier must inform the operator without delay.
  — [EUR-Lex, Implementing Regulation (EU) 2025/2546](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2546) (via search excerpt; full Art. 3–4 not retrieved)
- Materiality: a 5% materiality level is reported only by a secondary guide and was not confirmed in the regulation text. — [cbamguide.com verification](https://cbamguide.com/compliance/verification/) (unconfirmed)
- Verifiers must register in the CBAM Registry within two months of receiving CBAM accreditation, and not before 1 September 2026. — [Kohen Avocats, quoting Commission guidance of 24 Aug 2026](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)
- Verifiers can use the O3CI portal from 1 September 2026. Verification reports are expected through the CBAM Registry from January 2027. These dates come from secondary summaries. — [CBAM Pulse updates](https://cbampulse.com/updates); [Materia Intel](https://www.materiaintel.com/insight/cbam_registry_o3ci_operator_verifier_portal)
- An operator and its verifier must have an active collaboration in the Registry before the verifier can view installation data. Either party can start the request, and the other must accept it. An engagement letter or email does not create the permission. Only one verifier can be active per installation at a time. — [Materia Intel](https://www.materiaintel.com/insight/cbam_registry_o3ci_operator_verifier_portal)
- Site-visit preparation: keep a visit plan, access records, a list of interviewees, and an explanation for any unavailable document. Obtain the verifier's accreditation scope, status, and any suspension or withdrawal history. — [Kohen Avocats](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)
- Verification cost:
  - EUR 3,000–15,000 per installation, according to The Trade Hub. — [The Trade Hub](https://www.thetradehub.eu/en/guides/cbam/verification)
  - EUR 5,000–50,000 per installation, according to cbamguide.com. The site itself says this figure traces back to vendors, not authorities. — [cbamguide.com](https://cbamguide.com/importers/verification/)
  - About EUR 4,000 per installation in the Commission's 2021 impact assessment. That figure predates the first-year physical-visit obligation. — [search summary of cbamguide/The Trade Hub](https://cbamguide.com/importers/verification/)
  - INR 5–15 lakh for Indian exporters. — [The Sustainability Cloud](https://www.thesustainabilitycloud.com/blog/eu-cbam-verifiers-complete-guide-and-checklist-for-indian-exporters-2026-ready/)
- Capacity: a commentary says verifier capacity was "acute" as of April 2026, and that no defensible published figure compares accredited verifier capacity with the number of installations needing a first physical visit before September 2027. — [cbamguide.com verification](https://cbamguide.com/importers/verification/) (secondary)
- Non-EU verifiers can qualify if their accreditation body has a mutual recognition agreement with the European accreditation body. — [cbamguide.com](https://cbamguide.com/importers/verification/) (secondary)

### Inferences
- **Producer task map (2026 cycle) with rough effort.** The effort figures are my inference. No source gave hours.
  1. Installation and boundary definition, production-route mapping, CN code list: one-off, heavy. Done once per installation and revisited when the process changes. Agent fit: medium. An agent can draft a boundary and process description from ERP BOM/routing data and site documents, but an engineer must sign it off.
  2. Monitoring methodology document (the evidence the verifier reviews): one-off plus annual updates, heavy, mostly writing and evidence assembly. Agent fit: high for drafting from templates plus installation data. The human approves.
  3. Activity data collection: recurring and heavy, the biggest data-wrangling block. This means fuel invoices, meter reads, electricity bills and PPAs, precursor purchase records, and production output. Agent fit: high for OCR/extraction (pdfplumber + Tesseract already exist), reconciliation against ERP, and gap detection.
  4. Emission factors and default values: medium effort. An agent can retrieve the right default value or benchmark from the 2025/2621 Excel tables, but the calculation must stay deterministic.
  5. Precursor data from upstream suppliers: heavy and slow, a multi-tier communication loop (Q3). Agent fit: high for chasing, parsing and validating replies.
  6. Communication Template / O3CI data entry: medium, but repeated per customer and per version. Agent fit: high for filling and validating the template. The Registry has no confirmed API, so O3CI entry may still be manual or browser-driven.
  7. Verification preparation (evidence pack, site-visit plan, interviewee list, responses to verifier queries): heavy in the first year, because the physical visit is mandatory. Agent fit: high for assembling the evidence index and drafting answers to queries.
  8. Distribution to multiple EU customers (collecting EORIs, sharing records): light per customer, but it grows linearly. Agent fit: high (CRM-style tracking).
- The 146-page portal manual, the one-active-verifier rule and the EORI exchange outside the Registry all suggest a lot of procedural know-how. An agent can encode that as a checklist and status tracker.
- Verifier scarcity before the 30 Sep 2027 deadline means a "verification-ready" evidence pack has commercial value. Fewer verifier days may reduce fees, but that is an inference.

### Gaps
- No primary source gave hours or person-days per installation for monitoring-plan drafting, data collection or template completion.
- Could not confirm whether a new definitive-period Communication Template exists, or its version number. Also could not confirm whether O3CI accepts a template, XML or bulk upload as opposed to manual form entry. The Materia Intel summary did not cover upload formats.
- The full text of Art. 3 (conditions d–e) and Art. 4 of 2025/2546 was not retrieved. The 5% materiality threshold is unconfirmed.
- No source specific to African operators: Tunisian, Egyptian, Mozambican or South African aluminium and fertiliser plants, local verifier availability, or MRA status of African accreditation bodies.

---

## Q2. Importer (authorised declarant) workflow: authorisation, CN codes, per-shipment data, annual declaration, certificates, 50% holding, carbon price deduction

### Takeaway
An importer above 50 t per year (or importing any electricity or hydrogen) needs authorised-declarant status through the AMM. It must then collect installation-level emissions per shipment or supplier, and reconcile customs import data against those emissions. The DRMC module helps with that reconciliation. The first annual declaration (covering 2026) is due 30 Sep 2027. Certificate sales start 1 Feb 2027. From 2027, the declarant must hold certificates at each quarter-end equal to at least 50% of year-to-date embedded emissions (reduced from 80% by the Omnibus). A deduction for carbon price paid requires documented, net-of-rebate payments. The detailed method is set by a 2026 implementing act.

### Cited Findings

**Authorisation and de minimis**
- Importers need authorised CBAM declarant status before importing electricity, hydrogen, or more than 50 t of other CBAM goods. Registering in or logging into the registry is "not sufficient" and must not be confused with authorisation. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- Under TARIC code Y238, importers who applied by 31 March 2026 may import above the threshold provisionally until a decision is made. Exempt importers use TARIC Y137, which can no longer be used once DEHSt determines the threshold has been exceeded. Indirect customs representatives are not "importers" and cannot use the threshold. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- Conflict: a myDPP explainer says the Y238 provisional route runs until 27 September 2026 at the latest. Another guide says unauthorised declarants could not import at all from 1 April 2026. — [myDPP](https://mydpp.app/en/knowledge/cbam-registration-authorised-declarant-deadlines); [search summary](https://www.gravityplatform.com/blog/cbam-guide-requirements-deadlines-and-who-has-to-comply)
- The 50 t threshold is expected to exempt about 182,000 importers while still covering over 99% of in-scope emissions. — [Commission TAXUD news, 20 Oct 2025](https://taxation-customs.ec.europa.eu/news/officially-published-simplifications-carbon-border-adjustment-mechanism-cbam-2025-10-20_en)

**Registry modules for declarants**
- AMM handles authorisation applications. DRMC (data reconciliation for monitoring and control) gives declarants a view of data on goods, emissions, certificates and penalties, and helps them anticipate the 50% rule. Declarants retrieve operator data from O3CI through the "Emissions" tab. The declarants portal user manual is dated 21 Aug 2026. — [Commission CBAM Registry and reporting](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry-and-reporting_en)

**Annual declaration**
- The annual declaration is due by 30 September each year for the preceding year. The first is due 30/09/2027 for 2026 imports. It must contain goods volumes by production installation, embedded emissions, the certificates to surrender (including any reductions), and copies of verification reports. As of DEHSt's page, declarations cannot yet be created in the registry, and this is expected from Q4/2026. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- Importers may use default values or actual values. Actual values must be verified, and a copy of the verification report accompanies the declaration. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- If no actual data with verifier confirmation is received, the importer must use default values. — [CBAM Slovenia](https://www.cbam.si/en/novica/how-to-obtain-cbam-data-from-a-supplier/)
- Default values carry a mark-up of 10% in 2026, 20% in 2027 and 30% from 2028. — [CarbonPassport guide](https://carbonpassport.ai/guides/cbam-data-request-from-eu-buyer.html) (secondary; check against IR 2025/2621)

**Certificates: purchase, surrender, quarterly holding**
- From 1 February 2027, Member States sell certificates to authorised declarants on a common central platform managed by the Commission. Declarants can buy at any time during the year. The price derives from EU ETS auction prices. — [DEHSt, CBAM certificates](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/CBAM-certificates/cbam-certificates_node.html)
- Certificates bought for 2026 imports are reported to be priced on the quarterly average of 2026 ETS auction prices, and from 2027 on a weekly average. — [cmtradelaw, Apr 2026](https://www.cmtradelaw.com/2026/04/carbon-border-adjustment-mechanism-cbam-first-release-of-cbam-certificate-price/); [cbamguide certificates](https://cbamguide.com/compliance/certificates/) (secondary; sources differ on detail)
- Surrender is due by 30 September each year. The number is adjusted for EU ETS free allocation, with the CBAM factor falling from 97.5% in 2026 to 14% in 2033. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- Quarterly holding (Art. 22(2), (2a)): from 2027, the certificate balance at each quarter-end must be at least 50% of the embedded emissions of all goods imported since 1 January. The calculation can be based on default values or on the previous year's surrendered certificates. For importers who were initially exempt, the obligation first applies at the end of the quarter after the threshold is exceeded. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)
- The Omnibus (reported as Regulation (EU) 2025/2083) reduced the holding level from 80% to 50%. There is no holding obligation in 2026. — [cbamjournal / search summary](https://www.cbamjournal.com/post/eu-cbam-certificate-surrender-explained-2026-2027-part-i); [EY, CBAM Omnibus adopted](https://www.ey.com/en_gl/technical/tax-alerts/eu-adopts-cbam-omnibus-regulation)
- Repurchase of excess certificates is reportedly to be requested by 31 October of the surrender year, and unused 2026 certificates are reportedly cancelled on 1 Nov 2027. These dates are unconfirmed in the secondary sources themselves. — [cbamguide certificates](https://cbamguide.com/compliance/certificates/)

**Carbon price paid deduction (Art. 9)**
- A reduction is allowed only if a carbon price was actually paid in the third country. All rebates and compensation mechanisms that lower the effective price must be deducted, and payments must be documented. If the Commission sets yearly default carbon prices, declarants can use those instead. Reductions based on default emission values can only use the default carbon prices. A forthcoming implementing act, due in 2026, will set the detailed method. — [DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)

**Cost burden (importer side)**
- Average annual compliance cost per importer is estimated at about EUR 4,248 (low) to EUR 20,637 (high), based on about 18,000 importers in the baseline. Total annual baseline compliance cost is EUR 76m–371m, and one-off adjustment costs are up to EUR 388m in total, ranging from 0 to EUR 129,000 for the largest importers. The wide range reflects differing survey responses. — [Commission SWD(2025) 988 Part 1, impact assessment, 17 Dec 2025](https://taxation-customs.ec.europa.eu/document/download/71d4f753-4a2d-4367-bb10-c1967cb7f28d_en?filename=SWD_2025_988_1_EN_impact_assessment_part1_v4.pdf) (per search excerpt; Annex 4 not opened)
- Higher estimates come from a steel-industry article: up to EUR 81,900 per declarant per year, and EUR 2.1bn per year in total plus EUR 2.3bn for IT, consulting and training. This is an advocacy source and conflicts with the Commission's range. — [steelnews.biz](https://steelnews.biz/cbam-expansion-bureaucracy-costs-are-out-of-control/)

### Inferences
- **Importer task map with agent fit (inference):**
  1. Threshold monitoring and authorisation application: an agent can track cumulative net mass per year and alert as it approaches 50 t. The application itself requires documents and a human submission.
  2. CN code determination: an agent can classify product descriptions or ERP item masters against Annex I CN codes, with human approval. This is a common error source (see Q3).
  3. Supplier and installation identification per shipment, linking customs lines to the operator/installation ID in O3CI: heavy matching work. Agent fit is high for fuzzy matching of supplier names and invoice lines to installations, with a confidence score and a human queue.
  4. Collecting actual emissions or falling back to defaults: an agent can request, chase, parse and validate data, and compute the cost of falling back to defaults as a negotiation lever.
  5. Reconciliation against customs data (DRMC): the deterministic engine reconciles, and an agent explains the variances.
  6. Quarterly 50% holding forecast and certificate purchase plan: the deterministic engine computes the numbers, and an agent drafts the purchase recommendation. Buying certificates is a financial transaction and must be executed by a human.
  7. Annual declaration assembly (volumes by installation, emissions, deductions, verification report attachments): an agent can assemble and pre-validate the package, and a human signs and submits.
  8. Carbon-price-paid evidence pack: an agent can gather proof of payment and net out rebates, but the method waits on the 2026 implementing act.
- carbonTraceAI serves producers. Its customers' EU buyers are the declarants, so the most valuable agent output on the importer side is buyer-ready data delivery: O3CI records, filled templates and verification reports keyed by EORI. Building importer-side tooling is a separate market.

### Gaps
- Not confirmed: whether the 2026 implementing act on carbon price paid has been adopted.
- Not confirmed: whether the declaration module went live in Q4/2026 (DEHSt said "expected").
- Did not open Annex 4 of SWD(2025) 988 for a breakdown of cost by task (for example, hours on supplier data versus registry filing).
- The CBAM factor and benchmark details by product, which matter for aluminium and fertiliser free-allocation adjustment, were not researched.

---

## Q3. Known pain-heavy tasks, with evidence

### Takeaway
The evidence supports four main pain points. First, supplier data collection is slow, fragmented and manual, and it can run several tiers deep. Second, suppliers find the template and methodology too complex, and the template's content diverges from the legal requirements. Third, registry and XML validation and portal reliability caused problems in the transitional period: XSD errors, decimal-precision limits, lost drafts, and "uploaded" not meaning "submitted". Fourth, operator/installation confusion and missing actual data make reports "incomplete". No source quantified hours per task.

### Cited Findings

**Supplier communication loops**
- CarbonChain says supplier data collection is often "slow, fragmented, and highly manual". Producers lack systems, expertise or incentives, and are unclear on what counts as CBAM-compliant data, which leads to gaps, inconsistencies or unusable submissions. — [CarbonChain CBAM](https://www.carbonchain.com/cbam) (vendor)
- Companies use different methods to request emissions data from suppliers, so requests are not standardised. — [IntegrityNext, first 10 months of CBAM](https://www.integritynext.com/resources/blog/article/insights-from-the-first-10-months-of-eu-cbam) (vendor)
- Importers depend heavily on suppliers and have no direct control over how exporters outside the EU gather data. — [The Sustainability Cloud](https://www.thesustainabilitycloud.com/blog/eu-importers-cbam-challenges/)
- CBAM effectively targets smelters, which can sit two to five tiers deep in the supply chain. — [Vis-map](https://vis-map.com/2024/02/26/getting-suppliers-installations-to-fill-cbam-communication-template/)
- Suppliers outside the EU are often reluctant to share data and may risk violating domestic data-protection laws. — [ICC open letter](https://iccwbo.org/news-publications/statement-letters/open-letter-on-the-carbon-border-adjustment-mechanism-cbam/)
- Suppliers treat production and energy data as business-sensitive and fear it could affect price negotiations. — [Clean Carbon](https://cleancarbon.ai/blog/cbam-data-collection-from-vendors/) (vendor)
- For low-value or irregular imports, the effort suppliers must spend can be disproportionate to the cost of using default values. — [Vis-map](https://vis-map.com/2024/02/26/getting-suppliers-installations-to-fill-cbam-communication-template/)

**Template and methodology complexity / versioning**
- The template and guide are too complicated for most suppliers, and the Excel fields diverge from what the law requires. — [ICC](https://iccwbo.org/news-publications/statement-letters/open-letter-on-the-carbon-border-adjustment-mechanism-cbam/)
- Transitional-period XML templates were tied to specific versions. For example, Commission webinar slides reference CBAM v1.1.1.0 and an XSD plus sample published on the CBAM site. — [Commission SDEV CBAM Declarants webinar](https://customs-taxation.learning.europa.eu/pluginfile.php/34802/mod_resource/content/1/SDEV-CBAM-DECLARANTS-TRM-Webinar.pdf)
- DEHSt publishes the quarterly report structure XSD and stypes.xsd. An accompanying XLS lists which fields are optional or mandatory and the predefined values allowed for certain fields (transitional). — [DEHSt transitional registry](https://dehst.de/EN/Topics/CBAM/Transition-phase/Transitional-registry/transitional-registry_node.html)

**Registry / XML rejections (transitional evidence)**
- The Commission's known-errors list (Feb 2024) recorded several XSD validation errors when uploading quarterly report XML. Affected elements included MIME, Binary, ExchangeRate and ApplicableMethodologyConfirmation, with fixes due in a later release. The decimal allowance on mass and emissions fields was raised from 5 to 7. — [Commission known errors list (via Assolombarda)](https://www.assolombarda.it/servizi/ambiente/informazioni/cbam-transitional-registry-list-of-it-changes-known-errors/@@download/file/2024%2002%2020%20CBAM%20Transitional%20Registry%20-%20List%20of%20IT%20Changes%20&%20Known%20Errors.pdf)
- The Dutch authority warned of fields rejecting values with more than five decimals, and of draft edits that might not save or might save incorrectly (data loss). — [NEa CBAM newsletter, Feb 2024](https://www.emissieautoriteit.nl/binaries/nederlandse-emissieautoriteit/documenten/hulpdocument/2024/02/29/nieuwsbrief-cbam-februari/Nieuwsbrief+CBAM+februari+2024.pdf)
- A successful XML upload only creates a draft, which must then be submitted through the UI. Uploads are zip packages containing the XML and attachments. — [Commission declarants webinar](https://customs-taxation.learning.europa.eu/pluginfile.php/34802/mod_resource/content/1/SDEV-CBAM-DECLARANTS-TRM-Webinar.pdf)
- The Commission allowed "request delayed submission", adding 30 days, for declarants hit by system errors. — [CMS law note](https://cms.law/en/tur/legal-updates/cbam-no-penalties-for-delayed-reporting-due-to-technical-difficulties); [Commission ICS2/registry issues update](https://taxation-customs.ec.europa.eu/news/update-technical-issues-related-cbam-transitional-registry-and-import-control-system-2-ics2-2024-01-29_en)
- German chambers (DIHK) asked for a guaranteed system-to-system connection, saying an Excel upload is not enough at high volumes. This shows stakeholders want an API, not that one exists. — [DIHK statement on CBAM register](https://www.ihk.de/blueprint/servlet/resource/blob/6348374/5c473efffb95b8836201da1c33abc1be/dihk-stellungnahme-cbam-register-data.pdf)

**Content errors**
- Common errors: confusing operator (the company) with installation (the plant); missing actual data (from Q3 2024, estimates were capped at 20% of embedded emissions, transitional); reports without actual data treated as incomplete. — [SGS eCustoms](https://ecustoms.sgs.com/2024/07/22/the-start-of-the-transitional-period-for-cbam/); [RSM Hungary on CBAM notifications/sanctions](https://www.rsm.hu/blogs/customs-excise-green-taxes/cbam-notifications-are-arriving-the-era-of-sanctions-is)
- Definitive period: Registry information must concern the same installation and goods, and actual emissions must be kept separate from default values. — [Kohen Avocats](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)

### Inferences
- Ranked pain points where agents could take on the work (inference):
  1. Supplier and precursor data loop: request, chase, parse, validate, re-request.
  2. Evidence and document extraction for the monitoring methodology and verifier pack.
  3. Template/XML pre-validation against the current XSD or template version, before anything reaches the Registry. This mostly needs a deterministic validator, with an LLM explaining failures.
  4. Matching operator to installation to CN code to shipment.
  5. Multi-customer distribution (EORI management).
- Unit and CN mapping errors are a plausible pain point (for example, tonnes versus kg, and aluminium chapter 76 versus downstream articles), but I found no quantified source. Treat this as hypothesis, not evidence.
- The "upload is not submission" and "saved is not verified" rules call for explicit state tracking: draft, validated, submitted, verified.

### Gaps
- No definitive-period (2026) data on Registry rejection reasons or error frequencies. All XML evidence is from 2024.
- No measured hours per supplier, template or report from any survey. CarbonChain, IntegrityNext and others give qualitative claims only.
- No evidence specific to unit or CN mapping errors.

---

## Q4. Agent architecture patterns suited to CBAM (tool-calling over deterministic engines, orchestration, MCP, HITL, evals, audit, residency, cost)

### Takeaway
The three main SDKs all support a pattern that fits CBAM: the LLM plans, extracts and drafts, while deterministic tools (calc engine, XSD/template validators, ERP connectors) compute. Every side-effectful or filing-related action passes through a durable human approval gate. LangGraph uses `interrupt()` plus checkpointers, the OpenAI Agents SDK uses `needs_approval` with `result.interruptions`, and the Claude Agent SDK uses PreToolUse hooks with allow/deny/ask plus `canUseTool`. None of them supplies notifications, timeouts, escalation or audit records out of the box, so carbonTraceAI must build the approval queue and audit log itself.

### Cited Findings

**Human-in-the-loop primitives**
- LangGraph: `interrupt()` pauses a graph and `Command(resume=value)` resumes it. A checkpointer makes the pause durable. Interrupts can sit inside tool functions so a human can review or edit a tool call before it runs. — [LangChain docs, Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- LangChain JS has a `humanInTheLoopMiddleware` for tool approval built on interrupts. — [LangChain reference](https://reference.langchain.com/javascript/langchain/index/humanInTheLoopMiddleware)
- OpenAI Agents SDK (Python): tools can be marked `needs_approval=True`, or given a callable that decides per call. Without an `on_approval` callback, the run pauses and returns pending requests in `result.interruptions`, which are approved or rejected through the run state before resuming. — [OpenAI Agents SDK, Tools](https://openai.github.io/openai-agents-python/tools/); [JS human-in-the-loop guide](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/); [OpenAI guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- According to a third-party write-up, the OpenAI flag only pauses execution. It "does not notify, time out, escalate, or produce an audit record". — [The Handover blog](https://thehandover.xyz/blog/openai-agents-sdk-needs-approval) (third-party)
- An open GitHub issue requests "provider-neutral institutional authority evidence for tool approvals", which suggests approval evidence and audit are not built in. — [openai-agents-python issue #5288](https://github.com/openai/openai-agents-python/issues/5288)
- Claude Agent SDK: hooks evaluate first (allow, deny or continue), then deny rules, then permission mode, then the `canUseTool` callback. A PreToolUse hook can return `permissionDecision` ("allow", "deny" or "ask"), a reason, and `updatedInput`. Deny takes precedence over ask, and ask over allow. PostToolUse runs after execution and cannot prevent side effects. — [Claude Agent SDK, Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions); [Claude Agent SDK, Hooks](https://platform.claude.com/docs/en/agent-sdk/hooks)

**MCP and domain tools (reference implementations)**
- `carbon-factor-matcher`: an MCP server that matches activities to emission factors. It uses keyword plus embedding retrieval and lets the calling agent choose from ranked candidates, in Chinese and English. The PyPI listing is proprietary, with a free tier of 300 queries/day using the ELCD database and a paid Pro tier. — [GitHub](https://github.com/Nikeandocean/carbon-factor-matcher); [PyPI](https://pypi.org/project/carbon-factor-matcher/2.3.8/)
- `jagan-shanmugam/climatiq-mcp-server` (MIT, Python): tools such as search-emission-factors and custom-emission-calculation. It may be dormant (only a few commits; activity unverified). — [GitHub](https://github.com/jagan-shanmugam/climatiq-mcp-server); [ChatForest review](https://chatforest.com/reviews/sustainability-climate-mcp-servers/)
- `pipeworx-io/mcp-climatiq` (MIT): exposes search_factors and estimate_emissions, and appears to be a gateway to a hosted endpoint. — [GitHub](https://github.com/pipeworx-io/mcp-climatiq)
- `starrybodies/ghg-calculator`: offline, with 967 GHG Protocol factors embedded. — [ChatForest review](https://chatforest.com/reviews/sustainability-climate-mcp-servers/)
- No CBAM-specific open-source Communication Template parser was found. Generic building blocks include ExcelAlchemy (Pydantic to and from Excel templates, with parse and validate) and xlparser. — [ExcelAlchemy GitHub](https://github.com/RayCarterLab/ExcelAlchemy); [xlparser PyPI](https://pypi.org/project/xlparser/0.2.1/)

### Inferences
**Proposed reference architecture for carbonTraceAI.** This section is design inference built on the cited primitives and the existing stack.

1. **Deterministic core stays authoritative.** The existing CBAM calc engine, the XML/CSV/JSON renderers and the Pydantic canonical store remain the only source of numbers. Agents never compute embedded emissions in free text. They call `calc_engine.run(installation_id, period)` and cite the output IDs. This fits the verifier's need for a methodology "an outside verifier can follow" (Kohen Avocats, above).
2. **MCP servers wrapping the existing stack.** Each server is a thin wrapper over the FastAPI endpoints:
   - `erpnext-mcp`: read-only queries for fuel and energy purchases, BOMs, production, and items by CN code.
   - `canonical-store-mcp`: read the store, plus write *proposals* only.
   - `cbam-calc-mcp`: run calculations, compare against default values, run sensitivity and uncertainty analysis.
   - `cbam-validate-mcp`: XSD and template-version validation, unit checks, mass balance, and CN-to-route consistency.
   - `docs-mcp`: OCR and extraction through the existing pdfplumber/Tesseract pipeline, plus an evidence index.
   - `defaults-mcp`: the IR 2025/2621 default value and benchmark tables loaded from the Commission Excel.
3. **Orchestrator-worker per lifecycle stage.** An orchestrator holds the installation-year state machine: boundary defined, monitoring method drafted, activity data complete, calculations frozen, verifier linked, evidence pack ready, verified, distributed to customers. Workers handle one stage each:
   - Document-extraction worker: invoices and meter sheets go to canonical records with confidence scores and page/bbox provenance.
   - Data-gap and anomaly worker: checks month-over-month changes, mass balance and missing months.
   - Supplier/precursor outreach worker: drafts emails and WhatsApp messages, parses replies and filled templates, re-requests missing fields.
   - Monitoring-methodology drafting worker.
   - Verifier-query response worker: drafts answers with evidence links.
   - Customer distribution worker: tracks EORIs, which customer received which version, and template version.
4. **HITL approval queue as a product surface.** It lives in the Next.js dashboard. Every write to canonical data, every outbound message, every artifact for the Registry or a customer, and every certificate-related recommendation becomes a queued proposal. Each proposal carries a diff, evidence links, a confidence score and the agent's reasoning summary. Durable pausing comes from LangGraph checkpointers, the OpenAI `interruptions` state, or Claude `canUseTool`/"ask" hooks. Notifications, timeouts and escalation have to be built, because the SDKs don't provide them (The Handover, above).
5. **Hard deny-list for side effects.** Agents never submit to the CBAM Registry, never buy, surrender or resell certificates, and never accept verifier collaboration requests autonomously. These are human-only actions, enforced through Claude PreToolUse deny rules or by withholding the tools. This matches the Registry's own model, where the "upload creates draft; human submits" rule already exists.
6. **Audit log.** An append-only log records agent-run ID, model and version, prompt hash, tool calls with inputs and outputs, approver ID and decision, and timestamps, linked to canonical record versions. Verifiers expect calculations and evidence to be traceable, and SDK approval flags produce no audit record on their own.
7. **Eval harness.** Golden sets would include:
   - Labelled invoices and meter sheets from African plants, for extraction F1.
   - CN-code classification cases.
   - Seeded-error datasets with unit mistakes, missing months and operator/installation swaps, for detection recall.
   - Supplier reply corpora, for parse accuracy.
   - Regression tests that the agent never changes calc outputs.
   These would run in CI alongside `tests/test_pipeline.py`. This is a recommendation. No CBAM-specific public eval set was found.
8. **Data residency / sovereignty.** Operators already see production and energy data as business-sensitive, and some may face domestic data-protection constraints (ICC, Clean Carbon, above). One option is a model-routing layer:
   - Open-weight models (Llama, Mistral, Qwen class) self-hosted in-country or in an EU region for extraction and classification on raw plant documents.
   - Frontier API models for drafting and reasoning over redacted or aggregated data.
   This is an inference. I found no source on specific African hosting regions or model licences for this use case.
9. **Cost per run (rough reasoning, no sourced pricing).** Most volume is document extraction: dozens to hundreds of invoices per installation per year. Reasoning-heavy runs (methodology drafting, verifier answers) are few per year. LLM spend per installation-year is likely small next to the EUR 3k–50k verification fee range and the EUR 4k–21k per-importer compliance cost (above). This needs measuring with real token counts, and current model pricing must be checked before quoting.

### Gaps
- No published reference implementation of an agentic CBAM workflow (open-source or academic) was found in this research window.
- No sourced per-token pricing or benchmark of extraction accuracy for open-weight versus frontier models on emissions documents.
- No information on whether the CBAM Registry offers or plans a system-to-system API for O3CI or declarations. Without one, final Registry entry stays manual or browser-driven, and the Registry's terms should be checked before any browser automation.
- No sources on EU/African cloud regions or residency legislation, such as South Africa's POPIA or Egypt's data protection law, as they apply to industrial data.

---

## Q5. Open-source / reference implementations and EU template parsers

### Takeaway
There's little reusable open-source work. The search turned up generic emission-factor MCP servers (some proprietary or dormant) and general Excel/Pydantic parsing libraries. It found no open-source CBAM Communication Template parser, no CBAM agent repo, and no academic papers on CBAM agents. carbonTraceAI would need to build a template parser and its validator, and doing so could become a differentiator.

### Cited Findings
- Emission-factor MCP servers: carbon-factor-matcher (proprietary or freemium), climatiq-mcp-server (MIT, possibly dormant), pipeworx mcp-climatiq (MIT, hosted gateway), ghg-calculator (offline, 967 factors). — [carbon-factor-matcher](https://github.com/Nikeandocean/carbon-factor-matcher); [climatiq-mcp-server](https://github.com/jagan-shanmugam/climatiq-mcp-server); [mcp-climatiq](https://github.com/pipeworx-io/mcp-climatiq); [ChatForest roundup](https://chatforest.com/reviews/sustainability-climate-mcp-servers/)
- Generic tools that could support a template parser: ExcelAlchemy (Pydantic class to and from Excel template, parse and validate uploads) and xlparser (xls/xlsx/csv to dict/json). — [ExcelAlchemy](https://github.com/RayCarterLab/ExcelAlchemy); [xlparser](https://pypi.org/project/xlparser/0.2.1/)
- The Commission's transitional XSD, sample files and DEHSt's field-optionality XLS are the official schema references for building validators. They may need to be replaced by definitive-period equivalents. — [DEHSt transitional registry](https://dehst.de/EN/Topics/CBAM/Transition-phase/Transitional-registry/transitional-registry_node.html); [Commission webinar](https://customs-taxation.learning.europa.eu/pluginfile.php/34802/mod_resource/content/1/SDEV-CBAM-DECLARANTS-TRM-Webinar.pdf)

### Inferences
- Default emission-factor databases such as Climatiq and the GHG Protocol factors are not CBAM default values. CBAM needs the IR 2025/2621 tables and installation-specific factors. The existing MCP servers are useful as patterns, not as data sources.
- A versioned Communication Template parser (openpyxl plus Pydantic, keyed by template version, round-tripping read and write) combined with the existing renderers would let agents both read supplier-filled templates and generate customer-specific copies.

### Gaps
- Only general web search was used. GitHub code search for strings such as "CBAM" with "openpyxl" or "communication template" was not run directly and may find small repos.
- No academic papers (arXiv) on LLM agents for CBAM or MRV were found in this research window.
- The structure and versioning history of the definitive-period Communication Template is unknown and needs a direct download from the Commission CBAM website.
