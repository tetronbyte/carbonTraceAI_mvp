# Carbon credit markets as an agentic-AI opportunity (VCM, CORSIA, Article 6, compliance offsets, CDR)

Research notes, 21 October 2026. Scope: test the prior report's "avoid" rating for project-side carbon-credit MRV (row 7 in `reports/Agentic AI sustainability opportunities.md`) against fresh 2025–2026 evidence, segment by segment.

Evidence labels used below: **[P]** primary source (regulator, UN body, registry, the company's own data); **[D]** data vendor or analyst (MSCI, CIX, CDR.fyi, AlliedOffsets); **[S]** secondary press summary, often of a paywalled source; **[E]** my own estimate or inference, with the arithmetic shown.

---

## 0. Bottom line

1. **For generic, nature-heavy VCM project MRV, the "avoid" verdict stands, and the evidence for it is stronger now.**
   - Primary VCM value has been flat at about **$1.4bn for four years**. The average price fell to **$3.50/t** in 2025 [D, MSCI].
   - Benchmarks for REDD+ (**$1.90/t**) and non-CORSIA cookstoves (**$0.60–2.45/t**) drifted lower through H1 2026. Nature-based issuance fell by about a third [D, CIX; Climate Focus].
   - The MRV and ratings firms that served this segment have cut staff, been sold or pivoted: Pachama laid off staff and was sold, and Renoster pivoted.
2. **The verdict is wrong for one segment: correspondingly adjusted ("authorised") units.**
   - These units sell for 5–15x the price of unauthorised credits from the same projects:
     - CORSIA Phase 1 generic: **~$9.40–12.60/t** in mid-2026.
     - Swiss KliK ITMOs: **CHF 27–35/t**; Swiss cookstove deals: **$20–25/t**.
     - Singapore government purchase: **~S$35/t**.
     - Norway TCAF: **$30/t** [P, UNFCCC Baku deck; D, CIX].
   - The gating step is not carbon maths. It is a document- and evidence-heavy workflow: host-country Letter of Authorisation (LoA), corresponding adjustment, registry labelling, Article 6.2 reporting, buyer due diligence and, if the adjustment is missing, insurance.
   - African tech-based projects (cookstoves, biodigesters, methane) supply about **24% of labelled CORSIA units today** [P, IATA/ICAO, Sept 2026].
   - A defined, dated demand window closes **31 January 2028**.
3. **A second, smaller segment has a payer carbonTraceAI already sells to.** These are South African carbon-tax payers using the enlarged offset allowance: **15% combustion / 10% process** from the 2026 tax year, with returns due July 2027 [S, Anthesis/Fastmarkets]. This is a module, not a company.
4. **Durable CDR MRV is a real market, but it is dominated by Isometric and depends on one buyer.** Microsoft holds **78.5%** of contracted durable tonnes and was reported to have paused new purchases in April 2026 [D, CDR.fyi; S, Heatmap/Bloomberg]. African CDR is tiny: kilotonnes, not megatonnes. Avoid as core.
5. **Revised verdict for row 7:** split it.
   - "Generic VCM project MRV / PDD drafting": **Avoid** (confirmed).
   - "Authorised-unit eligibility and evidence agent for African tech-based credits (CORSIA, Article 6.2 buyers)": **Test** with hard kill criteria. The window runs to the CORSIA first-phase deadline and then rolls into Phase 2 (2027–2035, **0.88–1.35 Gt** demand) [P, UNFCCC Baku deck].
   - "SA carbon-tax offset-allowance module": **Build as an adjunct** to the multi-regime MRV engine that the prior report recommended.

---

## 1. VCM size, prices, retirements (2024–2026)

| Metric | Value | Source / quality | Note |
|---|---|---|---|
| Primary market value 2025 | "just over **$1.4bn**", flat for 4th year | MSCI Carbon Markets [D] ([MSCI](https://www.msci.com/research-and-insights/blog-post/carbon-credits-come-of-age-in-2025)) | Retirement-based estimate |
| Retirements 2025 | **202 MtCO2e**; issuance **294 Mt** | MSCI [D] (same) | Issuance > retirement → oversupply persists |
| Average price 2025 | **$3.50/t** (2024: $4.30); BBB+ index **$6.80** (2024: $5.60) | MSCI via UNFCCC Baku deck [P/D] | Quality spread widened to 1.9x; year-end high vs low-rated spread **>$7/t (~360%)** |
| OTC transaction value 2024 | **~$535m**, volume −25%, price −5.5% | Ecosystem Marketplace SOVCM 2025 [D] ([EM](https://www.ecosystemmarketplace.com/articles/sovcm-2025-finds-the-voluntary-carbon-market-in-transition-demand-holding-steady-as-turnover-stabilizes/)) | No EM 2026 edition (2025 data) found |
| Global issuance 2025 (all crediting incl. govt) | **~433 Mt**, +8%; retirements **−10–11%** (compliance retirements fell, voluntary stable) | World Bank State & Trends 2026 [P via S] ([Vertis](https://vertis.com/media/world-bank-state-and-trends-of-carbon-princing-2026/), [WB PDF](https://documents1.worldbank.org/curated/en/099051826185087983/pdf/P502283-3ee8b1dc-6f1a-46dd-8141-e6534fd34af9.pdf)) | Govt crediting mechanisms 24→34, their issuance +~40% |
| Retirements 2025, alternative counts | AlliedOffsets **+~3%**; Carbon Direct **−7%** | [S] ([Senken](https://www.senken.io/carbon-outlook/offtakes-are-up-260-percent-what-this-means-for-carbon-credit-supply-your-2026), [CRBN](https://crbn.credit/post/mid-2026-carbon-market-data-report)) | **Sources disagree on direction**; definitions differ |
| H1 2026 retirements | **104 Mt** (+4%, "strongest H1", AlliedOffsets); **98 Mt** (Climate Focus); Verra+GS combined **−9% YoY** | [S] ([CRBN](https://crbn.credit/post/mid-2026-carbon-market-data-report), [Climate Focus](https://climatefocus.com/publications/carbon-markets-2026-h1/), [Carbon Pulse](https://carbon-pulse.com/560555/)) | One Hess retirement (12.5m Guyana JREDD) ≈ 12% of H1 |
| H1 2026 issuance | **<100 Mt**; 2026 forecast **~200 Mt, lowest since 2019**; nature-based issuance **−1/3**; cookstoves + biogas became the largest source of new credits | Climate Focus [D via S] | Supply shifting to cookstove/biogas because of CORSIA |
| CCP-labelled share | **~1/5 of H1 2026 issuance** (record); CCP issuance **+64%** YoY; CCP retirements **+18%** | Climate Focus; AlliedOffsets [S] | Lloyds: only 4–10% of total issuance CCP-labelled historically |
| Non-CORSIA benchmarks H1 2026 | REDD+ CNX **$2.25→$1.90**; ARR CAX **~$12.2–12.9**; cookstove CCX **$0.60–2.45** (GS > VCS, LDC > DC) | CIX Market Pulse H1 2026 [D] ([CIX PDF](https://static.climateimpactx.com/CIX%20Intelligence%20-%20Market%20Pulse%20H1%202026.pdf)) | Lowest-traded-project benchmarks |
| Non-CORSIA activity mix H1 2026 | REDD+ 21.3%, cookstoves 18.4%, wind 12.4%; renewables fell from ~29% to ~18% | CIX [D] | Methane abatement steady at 12–13% |
| 2030 outlook | **$5–20bn** (2025 prices) | MSCI [D] | Wide range; treat as scenario only |

**How to read this.** "The VCM is dead" and "the VCM rebounded" are both wrong. Volumes are stable at about 180–200 Mt a year of retirements, but the money is not growing. Value is moving towards rated, labelled and authorised units, and away from the commodity tail. A software vendor priced off credit volume or developer margin in the commodity tail has no budget to capture.

Climate-tech carbon-market venture funding fell **61%** in H1 2026 (CTVC, cited in the prior report).

---

## 2. Integrity reforms and standards

### ICVCM Core Carbon Principles (CCP)
- **REDD+ approvals (Nov 2024):** ART TREES, VM0048 and JNR. The pipeline at the time was ~123m credits (ART) and ~300m (VM0048, first crediting period) ([ICVCM](https://icvcm.org/integrity-council-approves-three-redd-methodologies/)).
- **Cookstove approvals (Mar 2025):** VM0050 v1.0, GS TPDDTEC v4.0 and GS Metered & Measured, under conditions: MoFuSS or fNRB ≤ 0.3, among others. These methodologies covered **<3%** of available cookstove credits at end-2024 ([Climate Home](https://www.climatechangenews.com/2025/03/07/most-cookstove-carbon-credits-ruled-out-of-quality-scheme-in-push-for-high-integrity/)).
- **First CCP-labelled cookstove credits:** issued by Verra in Feb 2026 to a **Nigerian** project (VCS 2673) ([Verra](https://verra.org/verra-issues-first-ccp-labeled-clean-cooking-credits/)).
- **Later approvals:** Verra rice cultivation and landfill gas (Aug 2026 newsletter) ([Verra](https://verra.org/august-2026-newsletter/)).
- **Implication:** legacy cookstove inventory (most of the African stock) is not CCP-eligible. New-vintage credits under the approved methodologies are. This creates re-documentation and monitoring work, because projects must switch to the new methodology version and add metering or survey evidence.

### SBTi Corporate Net-Zero Standard v2.0
- **Published 11 June 2026.** Voluntary use from Feb 2027, mandatory for new or renewed targets from **31 January 2028** ([Watershed](https://watershed.com/blog/sbti-cnzs-2), [Ramboll](https://www.ramboll.com/en-us/insights/decarbonise-for-net-zero/new-sbti-guidance-for-corporate-net-zero-target-setting-goes-into-effect-in-2028)).
- **BVCM is replaced by "Ongoing Emissions Responsibility" (OER).** This is a voluntary recognition scheme with three tiers:
  - Engaged: 1% of S1–3.
  - Advanced: 100% of S1–2 plus 10% of S3.
  - Leadership: 100% of S1–3 for Category A companies.
- **Neutralisation (removals):** Category A companies must neutralise **1% of S1–3 by 2035**, rising to 100% by the net-zero year.
- **Credits still do not count towards reduction targets.**
- **Implication:** no SBTi-driven compliance-like demand before 2035. Near-term corporate demand stays voluntary and reputational. This **does not rescue** the commodity VCM in 2026–2028.

### Research evidence on over-crediting
- **Probst et al. (Nature Communications, Nov 2024):** a meta-study of 2,346 projects found **<16%** of credits are real reductions. Cookstoves came in at **11%**, avoided deforestation at **25%**, and wind and IFM showed no significant effect ([TUM](https://tum.de/en/news-and-events/all-news/press-releases/details/carbon-crediting-is-substantially-overestimated)).
- **Gill-Wiehl, Kammen and Haya (Nature Sustainability, 2024):** cookstove methodologies over-credit by **9.2x** in the sample and **~10.6x** when extrapolated. The GS metered methodology comes out at **1.5x**, the closest to reality ([Berkeley RAEL](https://rael.berkeley.edu/wp-content/uploads/2024/07/Gill-Wiehl-Kammen-Haya-Cooking-the-Books-Nature-Sustiainability-2024.pdf)).
- **Scandals:**
  - Verra suspended **27 C-Quest Capital cookstove projects** over alleged over-issuance, now subject to US criminal charges ([Argus](https://argusmedia.com/es/news-and-insights/latest-market-news/2582154-carbon-registry-verra-halts-27-cqc-cookstove-projects), [Verra](https://verra.org/c-quest-capital-statement/)).
  - Verra suspended **4 VVBs** over 37 rice projects.
  - The Kariba REDD+ suspension led South Pole's CEO to exit.

### Ratings divergence
- Agencies disagree materially. One Amazon REDD+ project was rated Tier 1 by Sylvera and low by BeZero and Calyx ([Carbon Market Watch / Perspectives](https://carbonmarketwatch.org/publications/assessing-and-comparing-carbon-credit-rating-agencies/), 2023).
- No 2025–26 quantitative inter-rater study was found. **Gap.**
- **Ratings-market health:**
  - BeZero revenue **+57%** in its latest financial year. Sylvera turnover **fell** while bookings grew ([Carbon Pulse, 15 Oct 2026](https://carbon-pulse.com/560806/), paywalled).
  - Renoster **exited ratings** in 2025 and became a CDR developer ([Carbon Pulse](https://carbon-pulse.com/436628/)).
  - Singapore appointed BeZero, Calyx and Sylvera to its integrity-assessment panel.
  - **Verdict:** the ratings/QA layer is consolidating around three incumbents, and there is no room for a new "verification agent" brand selling ratings.

**Is there an opportunity for verification/QA agents in integrity?**
- **Yes, but sell to the party that bears the integrity risk at a dated deadline,** not as a generic rating. That party is:
  - (a) developers who must pass VVB and registry review, or
  - (b) authorised-unit buyers (airlines, sovereign buyers) doing diligence.
- **The concrete, sellable integrity job is pre-submission QA.** For cookstoves and biodigesters, that means checking the fNRB/MoFuSS choice, usage-survey and metering evidence, and stacking/double-counting checks against the CCP conditions before the VVB sees the file.
- **Registries already reward this.** Verra's own digital review cut a cookstove review from **163 to 63 days**, and its findings went from 11 to 9 (see §6).

---

## 3. CORSIA first phase (2024–2026 obligations, cancel by 31 Jan 2028)

### Demand
- **IATA:** airlines must cancel **>200m EEUs by Jan 2028**. The IATA range is **170–236 Mt**, and ICAO/IATA show cumulative 213 Mt by 2026 ([CAPA](https://centreforaviation.com/news/iata-corsia-eeu-supply-growing-but-falling-well-short-of-units-needed-by-2028-1373032), [ICAO NACC deck, IATA, Sept 2026](https://www.icao.int/sites/default/files/NACC/MeetingDocs/2026/ENVSUSTF1/07%20Presentations%20-%20Presentaciones/ENVSUSWG01-P10.pdf)).
- **Independent estimates:** 146–236 Mt (Trove/MSCI, cited by Malaysia DGCA, Sept 2026).
- **Phase 2 (2027–2035):** **0.88–1.35 Gt**, when participation becomes mandatory [P, UNFCCC Baku deck].
- **Retirements so far:** only **3 airlines** had retired EEUs, **331,100 t** in total, as of the WB 2026 report.

### Eligible supply: definitions vary, so state which one you use

| Measure | Volume | Source |
|---|---|---|
| Issued and labelled CEEUs (ICAO dashboard) | **~37.5–38.0 Mt**, from 10 countries | ICAO dashboard via Malaysia DGCA paper (Sept 2026); IATA NACC deck |
| Units "benefiting from" CORSIA-compatible LoAs (incl. not yet issued) | **~72 Mt**, from **42 LoAs** (Aug 2026) | IATA, 18 Sept 2026 |
| Authorised and labelled | **~40 Mt**; demand is **4–6x** that | UNFCCC Baku deck (Sept 2026) |

**Labelled supply by host country (IATA, Sept 2026):**

| Host country | Volume |
|---|---|
| Guyana ART TREES | **24.96m** |
| Rwanda (GS 51k + VCS 4.58m) | **4.63m** |
| Madagascar | 2.60m |
| Uzbekistan | 1.57m |
| Malawi GS | 1.38m |
| Laos | 1.28m |
| Cambodia | 1.28m |
| Gambia | 0.20m |
| Tanzania | 0.15m |
| Sierra Leone | ~0 |
| **Total** | **38.03m** |

- **Africa ≈ 8.95m ≈ 24%** [E, summed from the table].
- **Pipeline LoAs:**
  - BURN Nigeria **5.2m** (11 Mar 2026).
  - DelAgua **4.78m** across Rwanda, Gambia and Sierra Leone.
  - Rwanda / Likano VCS 2984 **1.77m** (28 Jul 2026).
  - BURN earlier LoAs in Tanzania, Ethiopia and Malawi ([ASM](https://africasustainabilitymatters.com/rwanda-authorizes-1-77-million-carbon-credits-from-clean-cooking-project-for-potential-corsia-eligibility/), [BURN](https://www.burnstoves.com/carbon/carbon-blog/burn-expands-its-loa-footprint-across-africa-strengthening-a-multi-market-supply-pipeline)).

### Prices: the "shortage" did not produce high prices in 2026
- **CIX CP1 benchmark fell 50%** in H1 2026, from **$19.10 to $9.40/t** (January to mid-June) ([CIX](https://static.climateimpactx.com/CIX%20Intelligence%20-%20Market%20Pulse%20H1%202026.pdf)).
- **The resets coincided with:**
  - new supply: GS cookstove supply in Nov 2025 and Verra cookstove credits labelled in Jan 2026;
  - EU regulatory uncertainty: a draft proposal in late April to tighten Phase 1 eligibility for EU airlines, plus the extra-EU ETS scope question.
- **Three price tiers by June:**
  - generic cookstove/water: **$9–10**;
  - mid tier (mostly cookstove): **low-to-mid teens**;
  - jurisdictional REDD+: **high teens to ~$20**.
- **Rebound:** reference contracts rose to **~$12.5–13** in July–August after the Commission's **17 July 2026** ETS proposal ([Abatable](https://abatable.com/blog/a-summer-of-sourcing-corsia-what-four-airline-mandates-told-us-about-price-and-readiness)).
  - That proposal keeps CORSIA in EU law to 2035 and extends the ETS only to departures within 5,000 km of Frankfurt from 2029 ([B&D](https://www.bdlaw.com/publications/european-commission-proposes-to-extend-eu-ets-to-international-flights-beyond-europe-puts-corsia-on-trial/)).
  - Per Fastmarkets (cited in the UNFCCC deck), it also proposes removing the additional EU quality criteria for Phase 1.
  - UNFCCC deck price series: Oct 2025 peak **$23.2**; June 2026 low **$11.6** (series differ); July **$12.9**; Aug futures **$19.0**.
- **The World Bank** says CORSIA units traded at $15–22 "since Sept 2025". This is stale relative to the CIX data. The Malaysia DGCA paper's "$20–25" is also stale. **Use CIX/Abatable for mid-2026.**
- **Why prices fell despite the gap** (UNFCCC deck): eligible supply roughly **doubled January–June 2026**, while airlines **deferred purchases towards the 2028 deadline**.
- **Procurement reality** (Abatable, Jul–Aug 2026; [link](https://abatable.com/blog/a-summer-of-sourcing-corsia-what-four-airline-mandates-told-us-about-price-and-readiness)):
  - 4 airline RFPs drew **119 offers from 38 suppliers**, **~29x qualified demand**.
  - **36/119 (~1 in 3) lacked eligibility steps.**
  - 63 were labelled: 49 backed by a corresponding adjustment, 14 by insurance.
  - Airlines bought partial volumes.

### Interpretation
- **The demand is real, dated and large:** [E] 150–200 Mt × $10–20 ≈ **$1.5–4bn** for 2027–Jan 2028. IATA quotes $4–5bn. **But the margin is not in scarcity rents.**
- **The bottleneck is eligibility completion.** One-third of offered supply could not prove eligibility, and labelled units earn a premium. That is an evidence and workflow problem: LoA, CA reporting in BTRs, registry label, insurance, buyer KYC/diligence.
- **The price signal that matters to a developer is the eligibility uplift** [E]:
  - CORSIA generic $9.40–12.60 vs non-CORSIA cookstove $0.60–2.45 ≈ **$7–12/t**.
  - On a 5m-credit authorised portfolio, that is **$35–60m of value at stake**, enough to justify paying for software and services that reduce eligibility failure or delay.

### Host-country authorisation risk: KOKO Networks
- **Kenya never issued KOKO an LoA.** KOKO shut its Kenyan operations on **31 Jan 2026**: 700 staff, about 1–1.5m customers, around **15m credits** left with uncertain authorisation. It had a **$179.6m MIGA guarantee** at stake ([Sylvera](https://www.sylvera.com/blog/koko-networks-collapse-corsia-carbon-credits-loa), [Ecofin](https://www.ecofinagency.com/news-services/1202-52826-koko-networks-collapses-in-kenya-after-government-blocks-carbon-credit-sales), [African Business](https://african.business/2026/02/energy-resources/koko-failure-brings-cookstove-carbon-credit-model-into-question)).
- **Kenya's 2024 rules:** an LoA from NEMA, **25% of revenues** to the state/communities, and a **$4/credit levy**.
- **Lesson:** LoAs are political and discretionary. Software cannot remove sovereign risk, but it can make dossiers complete, consistent and fast to approve, and it can track the corresponding-adjustment chain. Any product must assume some projects never get authorised.

---

## 4. Article 6.4 (PACM) and Article 6.2

### PACM status

All figures below come from the UNFCCC Secretariat deck, Baku Climate Week, 7–8 Sep 2026 [P] ([PDF](https://unfccc.int/sites/default/files/resource/Accelerating_A6.4_Engagement_BakuClimateWeek2026.pdf)).

- **First issuance**, approved 26 Feb 2026: a Myanmar clean-cooking PoA transitioned from the CDM.
  - **648,783 t** for 2021–22, about **40% below** what the CDM would have credited.
  - Authorised for use in **Korea's K-ETS**.
- **Pipeline:** about **2,678 activities** (1,512 CDM transitions and 1,166 new PCNs).
  - **35 registered** (20 projects, 15 PoAs), worth about 39 Mt/yr, of which 72% is in Bangladesh and Uganda.
  - **2 have issued.**
- **Transition funnel:** 3,494 eligible → 1,512 requested → **418 host-approved by 30 Jun 2026** across 60 countries → 35 registered.
  - **357 approved activities must file addenda by 31 Dec 2026, with no extension.**
  - The CDM registry closes at end-2026.
- **Only 3 PACM methodologies are approved:** N2O from nitric acid, landfill gas, and grid renewables. Their pipeline is 407 PCNs, about 166 Mt/yr.
  - The new-methodology path takes **9–18 months** from submission to approval.
- **Readiness:** 129 Parties have a DNA, but only **69** have communicated participation requirements.
- **Implication:** the PACM is real but slow. The near-term document job is the **31 Dec 2026 addendum wave**, mostly Asian CDM-legacy developers, which is too soon and too far from Africa for carbonTraceAI. Later, new PCNs/PDDs need the mandatory **Sustainable Development Tool** and Paris-aligned baselines. These are template-heavy documents, but the payer is the developer and there is no public A6.4ER price yet.

### Article 6.2: sovereign buyers pay real prices

Source: UNFCCC Baku deck, buyer programme table [P].

| Buyer | Volume / budget | Price signal | Africa partners noted |
|---|---|---|---|
| Switzerland / KliK | **20 Mt by 2030** (~CHF 600m); ≥80 Mt for 2031–40; 22 new contracts in 2025 | **CHF 27–35/t**; cookstoves **$20–25** | Ghana (first African ITMO transfer, 11,733 t, Jul 2025), Senegal, others |
| Japan / JCM | **100 Mt by FY2030**; 31 partners, 293 projects; >$3bn invested | Project-financed; credit shares negotiated | Several African JCM partners; Japanese-technology model |
| Singapore | **2.175 Mt** for 2026–30 (~S$76m); second tender seeks **≥12m ITMOs** (opened 7 Sep 2026) ([CarbonCredits](https://carboncredits.com/?p=47558)) | **~S$35/t**; bids S$25–55 | Ghana, Rwanda among 12 implementation-agreement partners |
| Sweden | SEK 1.5bn to 2032 | n/d | **Ghana, Zambia, Kenya** |
| Norway (NOGER) | NOK 15bn mandate; $80m to TCAF | TCAF **$30/t** | via GGGI |
| Korea | **37.5 Mt by 2030** overseas | K-ETS allowance **~$20** (Q3 2026, up from $7) | MoUs with 10+ countries |

**Global and African counts:**
- 112 bilateral agreements/MoUs across 65 countries (Japan 32, Singapore 28, Switzerland 20) [P].
- UNEP-CCC Article 6 Pipeline, Africa (as of 4 Sep 2026): **35 agreements across 12 countries** (Kenya 5, Ghana 5, Zambia 4, Senegal 4, Tunisia 3, Rwanda 3) and **91 approved activities across 24 countries**, of which Kenya has 17 ([UNEP-CCC](https://prod.article6.ecritportfolio.org/global-data/regions/un-classification/africa)).
- **Ghana:** 12.7 Mt authorised (47% of its 24 Mt Article 6 budget) as of March 2026. Ghana had 44 Article 6.2 activities by July 2026. The first corresponding adjustment is due in **BTR2 (Dec 2026)** ([UNFCCC Ghana Q&A](https://unfccc.int/sites/default/files/resource/FMCP3_Ghana_Q&A.pdf)).
- **National registries:**
  - Kenya's National Carbon Registry (GIZ and Verst Carbon, Feb 2026), which feeds into a free, licence-free "African Registry for Carbon" with an AI "ARC Studio" planned ([GIZ](https://www.giz.de/en/newsroom/stories/national-carbon-registry-kenia-giz)).
  - Zambia's registry (SPAR6C, Aug 2026).
  - Zimbabwe's registry (May 2025).
- **Implication:** donor-funded, open-source registries make the host-government registry and authorisation layer a **poor software market**. It is a services and grants market. The commercial opportunity is on the **developer and buyer side of the authorised-unit flow**.

**The key insight for the "avoid" test.** About $20–35/t sovereign money and about $10–20/t CORSIA money exist now. Both require Article 6-grade MRV, sustainable-development reporting and authorisation evidence for each activity. The universe is small and countable: roughly 91 approved African activities plus the CORSIA-labelling pipeline, likely on the order of **30–60 developers or asset managers** in Africa [E]. That points to a high-ACV, low-count market and favours a service-heavy agent product rather than self-serve SaaS.

---

## 5. Compliance demand for offsets (2026 status)

| Jurisdiction | Rule | Demand / price | Software relevance |
|---|---|---|---|
| **South Africa** | Offset allowance up to **15% (combustion) / 10% (process, fugitive)** from 1 Jan 2026, up from 10%/5%; pre-2019 project credits usable to 31 Dec 2028; CDM, GS and VCS eligible; renewables threshold raised 15→30 MW ([Fastmarkets](https://fastmarkets.com/insights/south-africa-to-increase-carbon-offset-allowances-for-carbon-tax-budget-2025), [Anthesis 2026](https://www.anthesisgroup.com/za/insights/south-african-carbon-tax-update-2026/)) | Retirements against SA tax hit a **record in 2025**, with buyers favouring cookstoves ([Carbon Pulse](https://carbon-pulse.com/412163), paywalled). Tax R236/t (2025) rising; a 2025 JSE trade was at **$8.25/t**. Offsets must come from SA-based projects (Carbon Offsets Regulations; **verify the current rule**) | **High fit.** carbonTraceAI's SA carbon-tax users need eligibility checks, offset-limit calculation per emission type, and retirement and COAS evidence in the 2026 return (July 2027) |
| **Singapore** | Up to **5%** of taxable emissions via ICCs from implementation-agreement countries with a corresponding adjustment; tax **S$45** (2026–27), S$50–80 by 2030 | Eligible supply was scarce in early 2026; a consultant expects few eligible credits by end-2026, then possible oversupply; a Ghana developer reported no buyer commitments ([S&P via search](https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/030626-singapore-carbon-credit-buying-to-grow-as-2026-tax-hike-looms-participants)) | Buyer diligence is covered by the ratings panel (BeZero, Calyx, Sylvera). Low fit |
| **Colombia** | Carbon tax "non-causation", capped at **50%** since 2023; a new minister (29 Sep 2026) revoked the prior decree and signalled a return to 100% (needs a change in law) ([Carbon Pulse](https://carbon-pulse.com/555583/)) | ~**7.7 Mt** (Sep 2025–Feb 2026) and **~9.2 Mt** (Mar–Aug 2026) offset; ~71% offsetting rate; tax **~$8.78/t** | Domestic registries (EcoRegistry, ColCX); Latin American incumbents. Low fit for Africa |
| **Chile** | Green-tax offsets | Not researched in depth. **Gap** | — |
| **Korea K-ETS** | International offsets converted to KCUs; first A6.4ERs authorised for K-ETS; target 37.5 Mt overseas by 2030 | Allowance ~$20 (Q3 2026) | Sovereign/corporate buyer of Article 6 units; indirect |
| **Japan GX-ETS** | Mandatory from FY2026 (≥100 kt sites); eligible credits limited to **J-credits and JCM** (international VCM credits barred); proposed cap of 10% of emissions ([S&P](https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/070725-japan-mulls-barring-international-vcm-credits-before-gx-ets-launch-move-to-be-bullish-for-domestic-credits), [Mizuho](https://www.mizuhobank.co.jp/corporate/mhri/consulting/articles-2026-k0008/index.html)) | JCM is the only African route | JCM is Japanese-firm-led; low fit |
| **China CCER** | Relaunched Jan 2024; first issuance **~9.3–9.5 Mt** (Mar 2025, offshore wind and solar thermal); up to 5% of CN ETS obligations | Prices volatile, 73–107 yuan | Closed domestic market. No fit |
| **India CCTS offset mechanism** | 9 methodologies approved by BEE; more consulted May–Jun 2026; as of Apr 2026 offsets **cannot** be used for compliance | Pre-revenue | No fit for Africa |
| **EU 2040 target** | Article 6 credits up to **5% of 1990 emissions from 2036**; pilot 2031–35; **not usable in the EU ETS** ([ICAP](https://icapcarbonaction.com/en/news/eu-reaches-agreement-2040-climate-target-postpones-ets-2-one-year)) | ~900 Mt over 2036–40 (realistic profile) | Long-dated; signals demand for authorised African units after 2030 |
| **EU ETS removals** | 17 Jul 2026 proposal: +250 Mt cap 2031–40 to buy CRCF-certified permanent removals; **BioCCS and DACCS only, biochar excluded** ([Fastmarkets](https://www.fastmarkets.com/insights/eu-review-opens-door-to-carbon-removals-in-ets-confirms-international-credit-use-for-2040-goals/)) | Post-2031; domestic only | Not an African opportunity |

---

## 6. Operational workflow: where time and money go, and who pays

### Typical lifecycle (Verra/GS/PACM)
1. Feasibility and methodology eligibility.
2. PDD drafting, plus the SD tool (PACM) or SDG/safeguards annexes.
3. Stakeholder consultation (PACM global consultation: 28 days).
4. Validation by the VVB/DOE.
5. Registration review by the registry.
6. Host approval or authorisation (PACM host approval: 90 days after consultation; LoA for Article 6/CORSIA).
7. Monitoring period and data collection.
8. Monitoring report.
9. Verification by the VVB.
10. Issuance review.
11. For authorised units: CA reporting in the BTR / Article 6.2 initial and annual reports, and registry labelling.

### Timelines
- **To first issuance:** validation can take "up to a year". Design, validation and registration run about 1 year, and verification and issuance about another year, so **~18–24 months to first issuance** [E, from Verra lifecycle FAQs].
- **African VVB timeframes:** approximately **2–9 months** per validation/verification [P, Perspectives/VCMI/GIZ, Feb 2026].
- **Verra review:**
  - Initial review goal of ~20 business days per round, with 2–3 rounds typical (2024 guidance).
  - New SLAs from 1 Nov 2025.
  - 2026 goal: **cut average review time ≥20% vs 2025**.
  - Q1 2026: SLAs met in 19 of 21 categories.
  - **Digital PRR pilot:** cookstove review **63 days vs 163 days** for the traditional route, with findings down from 11 to 9. VVB response time fell **28 vs 38 days** (−26%). Average duration **127 vs 169 days** (−24%) [P, Verra April 2026 stakeholder webinar].
  - Verra's new registry (S&P Global Energy platform) went live **27 Jul 2026**, with APIs and Article 6 functions promised ([Verra](https://verra.org/verra-launches-next-generation-registry-with-sp-global-energy/)).
- **PACM:** addendum deadline 31 Dec 2026. New methodologies take 9–18 months.
- **CORSIA LoAs:** "takes time and sustained engagement" (BURN). There is no statutory clock in most African DNAs. KOKO waited and failed.

### Capacity bottleneck in Africa
Source: Perspectives/VCMI/GIZ, Feb 2026 [P] ([PDF](https://vcmintegrity.org/wp-content/uploads/2026/02/Strengthening-VVB-Capacities-Report_February-2026-v4.pdf)).
- **>90%** of African verification is done by international VVBs or non-African auditors.
- Only **19 of 48** accredited VVBs (GS, Plan Vivo, Verra) have offices in Africa.
- Developers attribute **10–50% of total project delays and cost overruns** to VVB bottlenecks.
- The binding constraint is **qualified lead auditors**, not the number of firms.
- **Market context:**
  - Africa produced about 20% of new projects listed in 2024 but only about 16% of retirements.
  - Five countries account for about 65% of issuance; Kenya alone has 23%.
  - **Cookstoves and REDD+ make up ~90% of African VCM supply.**
  - Gold Standard dominates: 79% in East and Southern Africa, 65% in West and Central Africa.

### Costs (thin public data: a **gap** to fill through discovery calls)
- **Validation:** **$12k–20k** per project (validator quote cited by GOGLA, undated).
- **Older land-use figures (FAO 2010):** documentation €50–100k, validation €15–25k, initial verification €20–25k.
- **Registry fees:** small, e.g. Plan Vivo PDD review $1.5–3k.
- **Forestry MRV:** €0.15–1.4/t (I4CE 2018). That is material when REDD+ sells at ~$2/t.
- **CDR MRV:** **>50% of total cost** for ERW, soil carbon and ocean alkalinity, and up to **73%** for biomass sinking ([LSE Grantham, Oct 2024](https://www.lse.ac.uk/granthaminstitute/publication/towards-improved-cost-estimates-for-monitoring-reporting-and-verification-of-carbon-dioxide-removal/)).
- **Bio-oil MRV:** Charm reported testing costs of >$200 per ton injected (2024), since cut by 88%.

### Who pays
- **Developers** pay consultants for the PDD and monitoring report, the VVB, registry fees and issuance levies.
- **Buyers** sometimes pay: Isometric charges buyers a flat verification fee, and KliK/ERPA buyers prepay.
- **Donors** pay for host-government capacity and registries.

**The pain is the most commercially actionable where three conditions hold:** (a) the credit is worth ≥$10/t because it is authorised, CORSIA or CDR; (b) a deadline exists (Jan 2028, Dec 2026, a tax return); and (c) a failed or slow submission has a measurable cost (lost eligibility uplift, a penalty, cash-flow delay).

---

## 7. Where agents are being applied: competitor map

| Player | Segment | What the "agent" or AI does | Status / evidence | Threat to carbonTraceAI |
|---|---|---|---|---|
| **Isometric** | CDR registry + "agentic certification" | Certify platform: agents cross-check sensor, satellite, supply-chain and lab data and flag discrepancies for human verifiers; claims "months → hours"; buyer-pays verification fee | $40M Series A (Jun 2026, AVP, AXA), with ICE taking it to **$50M**; >16Mt contracted, >200 projects; Microsoft, JPMorganChase, Boeing; expanding to industrial, fuel and data centres ([Isometric](https://isometric.com/writing-articles/isometric-raises-40m-to-bring-agentic-certification-to-the-industrial-economy)); reported approvals from ICVCM, CORSIA and ICROA ([Carbon Herald](https://carbonherald.com/isometric-first-carbon-registry-approval-icvcm-corsia-icroa/), not verified) | **High** in CDR and possibly industrial MRV. It is a registry, so a developer-side tool that feeds Isometric is complementary |
| **Verra** (registry) | Registry | Digital PRR tool from 1 May 2026: automated, system-assisted and human checkpoints; automated completeness checks; new S&P-built registry with APIs | Primary | The registry is automating its own review. A third-party "review agent" sold to registries is unlikely; a **developer-side pre-submission agent** aligned with Verra's digital forms benefits |
| **Gold Standard** | Registry | dMRV pilot running to Oct 2026; first fully digitised dMRV credits (Mar 2026, Hedera Guardian) ([Carbon Pulse](https://carbon-pulse.com/496286/)); SustainCERT verifying dMRV pilots | Primary/secondary | Same as Verra |
| **Kanop** | Nature dMRV | Eligibility Assessment Agent (VM0047, GS ARR, Isometric, Equitable Earth) produces reports "in hours"; claims 95% time saving and 70% cost cut vs consulting | Vendor claims ([Kanop](https://www.kanop.io/blog/reflecting-on-2025-kanops-year-in-review)) | Medium (nature only; carbonTraceAI is not in nature) |
| **Pachama → Carbon Direct** | Nature MRV and diligence | Remote-sensing diligence | ~20 layoffs (Jun 2025), then sold to Carbon Direct ([Trellis](https://trellis.net/article/pachama-layoffs-carbon-market/)) | Evidence that nature MRV software failed as a standalone business |
| **Sylvera, BeZero, Calyx, MSCI** | Ratings | Automated data analysis plus analyst review | Consolidating; government panels (Singapore); Mirova deals; BeZero +57% revenue | Low (do not compete) |
| **Renoster** | Ratings → CDR developer | — | Exited ratings in 2025 | Evidence that a weak ratings tail exits |
| **Abatable** | Procurement (incl. CORSIA RFPs) | Runs airline RFPs, readiness screening | 119 offers / 38 suppliers in Jul–Aug 2026 | Potential **channel/partner**: it already sees the "1 in 3 not eligible" problem |
| **CEEZER, Patch, Carbonmark, ClimateTrade, Cloverly, Rubicon** | Marketplaces / APIs | Carbonmark x402 endpoint lets AI agents buy and retire credits autonomously (Jul 2026) ([Carbonmark](https://www.carbonmark.com/post/agentic-commerce-comes-to-carbon-markets-what-ai-agents-see-when-they-buy-carbon-credits)); Cloverly shifting to supplier-side credit management | Operating; Rubicon offtakes with African biochar (Bio-Logical) | Low; buyer-side commodity |
| **PDD-drafting AI** | Developer documentation | Omdena/Transitry GPT-4 PDD generator (nature); an unnamed startup (Carbon Pulse, 18 Mar 2026) flags compliance gaps before certification; a 2023 product trained on past PDDs | **No funded leader found** | Opening exists, but PDD drafting alone is low value (one-off, cheap consultants) |
| **Carbonfuture, Puro, Riverse, CYNK (Kenya)** | CDR MRV / registries | Digital MRV for biochar etc.; CYNK builds dMRV for Tera (Kenya, Riverse) | Small | CDR niche; possible partners |
| **Straatos** | dMRV | Cited in the African VVB report as a dMRV actor | — | Unknown; check |
| **GIZ ARC / Verst Carbon** | Host registries | Free, licence-free registry; AI "ARC Studio" planned | Donor | Kills the commercial host-registry market in East Africa |

No 2026 AI-agent launch was found from Sylvera, BeZero, Abatable, CEEZER or Carbon Direct (one search; **gap**).

---

## 8. Durable CDR: market, MRV pain, payers, Africa

- **Volume:** 2025 contracted **30.4 Mt** durable (ClimeFi: 29.6 Mt). Q1 2026: **2.3 Mt**, the strongest Q1 so far ([CDR.fyi](https://www.cdr.fyi/blog/durable-cdr-market-update-carbon-unbound-east-coast-2026)).
- **Concentration** (as of 13 Apr 2026; [CDR.fyi](https://www.cdr.fyi/blog/durable-cdr-demand-structure-snapshot-april-2026)):
  - **Microsoft:** 36.4 Mt (**78.5%**), with only **91 kt delivered**.
  - **Frontier:** 1.84 Mt (4.0%).
  - **Everyone else:** 8.17 Mt (17.5%) but **90% of deliveries and 94% of retirements**. Non-Microsoft/Frontier 2025 contracted volume was 3.2 Mt.
- **Microsoft pause:** reported 10 Apr 2026 (Heatmap/Bloomberg). Microsoft denies an "indefinite" pause. It bought ~45 Mt in total ([Heatmap](https://heatmap.news/carbon-removal/microsoft-carbon-removal-pause)).
- **Frontier:** raised a further **$915M** (Jun 2026; Google and Anthropic named in headlines), doubling its commitments to **$1.8bn**, focused on 10–15 bets with 8–10-year offtakes. It expects >50 kt delivered in 2026. Its first in-situ mineralisation deal (~$12M) closed in Oct 2026 ([QZ headline](https://qz.com/anthropic-frontier-carbon-removal-coalition-915-million-061826), [Carbon Pulse](https://carbon-pulse.com/561001/)).
- **Method mix 2025:** BiCRS was 96% of purchases (BECCS 69%) and 91% of deliveries (biochar 80%).
- **Prices** (weighted averages, secondary, unverified):
  - biochar **~$136**;
  - BECCS ~$220;
  - ERW ~$352;
  - DAC ~$516;
  - Puro biochar index ~€135 (Aug 2026).
  - The buyer–supplier gap is **$98/t** (2026 survey), expected to fall to $48 by 2030 ([CDR.fyi survey](https://www.cdr.fyi/blog/cdr-pricing-survey-may-2026)).
  - Buyers cite price vs budget (65%), delivery risk (40%) and **MRV confidence** as blockers.
- **MRV pain is greatest in open-system methods** (ERW, ocean, soil). Biochar and BECCS MRV is "relatively clear". Biochar is excluded from the proposed EU ETS removal integration.
- **Africa:**
  - **Octavia Carbon (Kenya DAC):** targets ~1,000 t/yr by end-2026/27; ~$3–3.6M of credit sales; raising an $8M Series A.
  - **Bio-Logical (Kenya biochar, Puro):** **1,307 credits issued**, Rubicon offtake.
  - **Tera (Kenya, Riverse, CYNK dMRV)** and **EcoFix (Puro preliminary)**.
  - **Biochar Industrial Group** (West Africa, $1.5M pre-seed, Sep 2026).
  - No African projects found on the Isometric registry (one search; **gap**). ([Puro](https://registry.puro.earth/projects/664457), [ThinkGeoEnergy](https://www.thinkgeoenergy.com/octavia-carbon-direct-air-capture-as-an-enabler-of-geothermal-growth-in-kenya/), [AllAfrica](https://allafrica.com/stories/202609170599.html))
- **Verdict:** CDR MRV has a payer (buyers, through registry and verification fees), but it is captured by Isometric, Puro and Riverse. Demand depends on one buyer. African volume is in kilotonnes. **Avoid as core.** Possible light use: carbonTraceAI's deterministic LCA/calculation engine as a supplier-side data-prep tool for African biochar operators submitting to Puro or Isometric. That is small ARPU.

---

## 9. Sub-segments: is there a payer with budget in 2026–2028?

Scoring: Payer = who pays, and whether the budget is real. Urgency = whether there is a dated forcing function. Fit = how well it matches carbonTraceAI's deterministic engine, ingestion and audit trail, plus Africa. Comp = the competitive gap (higher = more room).

| # | Sub-segment | Payer & budget | Urgency | Fit | Comp gap | Verdict |
|---|---|---|---|---|---|---|
| A | Generic VCM nature MRV / PDD drafting (REDD+, ARR) | Developers with ~$2/t REDD revenue, failing; MRV vendors consolidating | Low | Low (geospatial, not ERP) | Low (Kanop, Pachama/Carbon Direct) | **Avoid (confirmed)** |
| B | **Authorised-unit eligibility and evidence agent for African tech-based credits** (cookstove, biodigester, methane, water). Covers LoA dossier, CA/BTR tracking, CCP-condition QA (fNRB, metering, usage surveys), monitoring-report generation, labelling, buyer-diligence pack | Developers and carbon asset managers with authorised inventories (BURN, DelAgua, Likano and others; ~30–60 African entities [E]); **$7–12/t uplift** on the CORSIA spread; sovereign buyers at $20–35/t | **High:** CORSIA cancellation 1 Dec 2027–31 Jan 2028; then Phase 2; Ghana BTR2 Dec 2026 | Medium–high: monitoring reports for tech methodologies are deterministic calculation plus evidence trail, matching the engine; Africa focus | Medium: no funded leader; Abatable, ratings firms and consultancies (South Pole, Climate Focus, Perspectives) do this manually | **Test (best carbon-credit candidate)** |
| C | PACM transition addenda / new A6.4 PDDs | CDM-legacy developers (mostly Asia) | Very high but **31 Dec 2026**, too soon | Low (geography, timing) | Medium | **Avoid** (missed window); revisit new A6.4 PDDs in 2027 |
| D | Host-government Article 6 infrastructure (registries, authorisation, BTR/AEF) | Donors (GIZ, UNDP, GGGI, World Bank) | Medium | Medium | **None:** free GIZ ARC, SPAR6C | **Avoid as product**; possible paid pilots via donor programmes |
| E | **SA carbon-tax offset-allowance module** (eligibility, limit by emission type, COAS retirement evidence, return reconciliation) | SA emitters, carbonTraceAI's existing ICP; they save R236+/t on up to 15% of emissions | **High:** 2026 tax year, returns July 2027 | **Very high** | High: Big-4 and consultants do it manually | **Build as module** inside multi-regime MRV (prior #1) |
| F | Singapore ICC / Colombia buyer diligence | Taxable facilities | Medium | Low | Low (ratings panel; Latin American incumbents) | Avoid |
| G | CORSIA airline procurement / compliance agent | Airlines, small and developing-state carriers especially (ICAO APAC paper asks for pooled procurement tools) | High | Low (not an emissions calculation; procurement) | Low (Abatable, CIX, brokers) | Avoid; partner if B proceeds |
| H | Durable CDR MRV | Buyers via registries | Medium (Microsoft pause) | Low–medium | Low (Isometric $50M) | **Avoid** core |
| I | Industrial/methane PACM credits (N2O, landfill gas) and Article 6 from industrial plants | Industrial plant owners (Egypt, Morocco, Nigeria, SA) monetising abatement via ITMOs | Medium (Morocco DNA plans phosphates and green hydrogen; Article 6 bottom-up track) | **High:** plant data, the engine, ERP ingestion | Medium | **Watch / later module.** Links the CBAM/MRV core to Article 6 revenue |

---

## 10. Implications for carbonTraceAI

1. **Do not build a carbon-credit company. Build two adjacencies onto the multi-regime installation MRV core.**
   - **(E) SA offset-allowance module:** low risk, same customers, a dated deadline (July 2027 returns).
   - **(I) industrial Article 6 crediting readiness:** later. It turns plant abatement into authorised units (N2O, landfill gas and grid renewables are the only approved PACM methodologies) and reuses the same data spine.
2. **Run segment B as a time-boxed experiment, not a pivot.**
   - **Thesis:** the money is in the authorisation and eligibility step, not in measurement. About 1 in 3 CORSIA offers fails eligibility. Labelled units earn a premium. Verra's digital submissions cut review time by ~60% for cookstoves.
   - **Agent job:** "take a tech-based African project from issued credits to CORSIA/A6.2-ready units, with a complete, consistent, auditable evidence pack". This covers:
     - (i) CCP-condition QA (fNRB/MoFuSS, metering, usage surveys);
     - (ii) monitoring-report generation from device or ERP data with a deterministic calculation trail;
     - (iii) a host-country LoA dossier with SD/NDC mapping;
     - (iv) CA/BTR status tracking per vintage;
     - (v) a buyer-diligence data room.
   - **Pricing anchor** [E]: a per-tonne fee of **$0.10–0.30/t** on authorised volume (1–3% of the $7–12 uplift), or **$30–80k/yr per developer**. 30–60 African entities gives a **$1–5M ARR ceiling in Africa**. That is a small market, unless the scope extends to Asian cookstove and methane developers and to Phase 2 (2027–2035, 0.9–1.35 Gt).
3. **Kill criteria for segment B** (decide by Q1 2027):
   - Fewer than **3 of 10** African authorised-unit developers or asset managers say eligibility and evidence preparation costs them ≥$50k/yr or delays a sale by ≥3 months.
   - CORSIA generic prices stay <$10 and the EU quality debate keeps airlines on the sidelines, so the uplift shrinks.
   - Abatable or a ratings firm launches an equivalent eligibility tool.
   - LoA issuance stalls in more than one major host (Kenya after KOKO).
4. **Integrity is a feature, not a product.**
   - Over-crediting research (cookstoves 9–11x, metered 1.5x) means the deterministic, conservative, metered-data approach is a selling point to buyers who must defend CORSIA or sovereign use.
   - Do not sell "AI ratings".
   - Never automate claims that the evidence does not support. The Trellis greenwashing-agent warning in the prior report applies.

---

## 11. Conflicts, caveats and gaps

- **CORSIA price:**
  - CIX shows $19.10 → $9.40 (H1 2026).
  - Abatable shows ~$12.5 (Jul–Aug).
  - The UNFCCC deck shows a June low of $11.6 and Aug futures of $19.0.
  - The World Bank ($15–22) and Malaysia DGCA ($20–25) figures are stale.
  - Use CIX/Abatable for spot and note that futures trade above spot.
- **CORSIA supply:**
  - 37.5–38 Mt labelled (ICAO dashboard).
  - 72 Mt "benefiting from LoAs" (IATA, includes unissued).
  - ~40 Mt (UNFCCC).
  - These measure different things. **The 4–6x shortage claim contrasts with the 29x oversubscription in Abatable's RFPs.** Reconciliation: buyers are deferring to the deadline, and many offers are not yet eligible.
- **2025 retirements:**
  - MSCI 202 Mt.
  - World Bank −10–11% (all crediting, compliance-driven).
  - AlliedOffsets +3%.
  - Carbon Direct −7%.
  - Definitions differ.
- **PACM transition approvals:** 110 (Jan 2026, VVB report) → 412/418 (Jun 2026, UNFCCC deck; two slides differ).
- **Gaps:**
  - No 2026 Ecosystem Marketplace SOVCM.
  - No current VVB fee benchmarks.
  - No full list of CORSIA LoAs by country.
  - SA offset retirement tonnage (paywalled).
  - Chile green-tax offsets.
  - No African Isometric projects verified.
  - Revenue of BeZero/Sylvera (paywalled).
  - A6.4ER prices (none public).
- **Paywalled:** Carbon Pulse items are cited from their headlines and summaries only.

---

## Key sources
- UNFCCC Secretariat, *Accelerating Article 6.4 Engagement*, Baku Climate Week, 7–8 Sep 2026: [PDF](https://unfccc.int/sites/default/files/resource/Accelerating_A6.4_Engagement_BakuClimateWeek2026.pdf)
- CIX Intelligence, *Market Pulse H1 2026*: [PDF](https://static.climateimpactx.com/CIX%20Intelligence%20-%20Market%20Pulse%20H1%202026.pdf)
- IATA at ICAO NAM/CAR, Sept 2026 (CEEU supply by country): [PDF](https://www.icao.int/sites/default/files/NACC/MeetingDocs/2026/ENVSUSTF1/07%20Presentations%20-%20Presentaciones/ENVSUSWG01-P10.pdf)
- Malaysia, ICAO APAC DGCA/61 IP/07/04 (CEEU price risk), Sept 2026: [PDF](https://www.icao.int/sites/default/files/APAC/Meetings/2026/2026%20DGCA61/Agenda%20Item07-Aviation%20and%20Environment/61-IP-07-04-MYS-MANAGING-CEEU-PRICE-VOLATILITY-AND-PROCUREMENT-RISK-FOR-AIRLINES.pdf)
- CAPA / IATA EEU supply, 18 Sep 2026: [link](https://centreforaviation.com/news/iata-corsia-eeu-supply-growing-but-falling-well-short-of-units-needed-by-2028-1373032)
- Abatable, CORSIA summer RFPs, Aug 2026: [link](https://abatable.com/blog/a-summer-of-sourcing-corsia-what-four-airline-mandates-told-us-about-price-and-readiness)
- MSCI, *Carbon Credits Come of Age in 2025*: [link](https://www.msci.com/research-and-insights/blog-post/carbon-credits-come-of-age-in-2025)
- World Bank, *State and Trends of Carbon Pricing 2026*: [PDF](https://documents1.worldbank.org/curated/en/099051826185087983/pdf/P502283-3ee8b1dc-6f1a-46dd-8141-e6534fd34af9.pdf); summary: [Vertis](https://vertis.com/media/world-bank-state-and-trends-of-carbon-princing-2026/)
- Verra, April 2026 stakeholder webinar (digital review metrics): [link](https://verra.org/documents/april-2026-stakeholder-update-webinar/)
- Perspectives/VCMI/GIZ, *Pathways for Strengthening VVB Capacity in Africa*, Feb 2026: [PDF](https://vcmintegrity.org/wp-content/uploads/2026/02/Strengthening-VVB-Capacities-Report_February-2026-v4.pdf)
- Sylvera on KOKO / LoAs: [link](https://www.sylvera.com/blog/koko-networks-collapse-corsia-carbon-credits-loa)
- CDR.fyi demand structure (Apr 2026) and market update (Jun 2026): [1](https://www.cdr.fyi/blog/durable-cdr-demand-structure-snapshot-april-2026), [2](https://www.cdr.fyi/blog/durable-cdr-market-update-carbon-unbound-east-coast-2026)
- Heatmap on the Microsoft pause, 10 Apr 2026: [link](https://heatmap.news/carbon-removal/microsoft-carbon-removal-pause)
- Isometric Series A: [link](https://isometric.com/writing-articles/isometric-raises-40m-to-bring-agentic-certification-to-the-industrial-economy)
- Probst et al. 2024 (TUM release): [link](https://tum.de/en/news-and-events/all-news/press-releases/details/carbon-crediting-is-substantially-overestimated); Gill-Wiehl et al. 2024: [PDF](https://rael.berkeley.edu/wp-content/uploads/2024/07/Gill-Wiehl-Kammen-Haya-Cooking-the-Books-Nature-Sustiainability-2024.pdf)
- SBTi CNZS v2 summary (Watershed): [link](https://watershed.com/blog/sbti-cnzs-2)
- UNEP-CCC Article 6 Pipeline, Africa: [link](https://prod.article6.ecritportfolio.org/global-data/regions/un-classification/africa)
- Singapore second ITMO tender: [link](https://carboncredits.com/?p=47558)
- Colombia non-causation: [Carbon Pulse](https://carbon-pulse.com/555583/), [data dive](https://carbon-pulse.com/559190/)
- South Africa offsets: [Fastmarkets](https://fastmarkets.com/insights/south-africa-to-increase-carbon-offset-allowances-for-carbon-tax-budget-2025), [Anthesis 2026](https://www.anthesisgroup.com/za/insights/south-african-carbon-tax-update-2026/)
- EU ETS removals and 2040 credits: [Fastmarkets](https://www.fastmarkets.com/insights/eu-review-opens-door-to-carbon-removals-in-ets-confirms-international-credit-use-for-2040-goals/), [ICAP](https://icapcarbonaction.com/en/news/eu-reaches-agreement-2040-climate-target-postpones-ets-2-one-year)
