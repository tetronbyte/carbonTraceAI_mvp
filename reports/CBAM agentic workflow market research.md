# Sell verifier-ready evidence, add agents sparingly

carbonTraceAI does not need an agentic AI workflow at its core, and putting one there would hurt. CBAM verifiers re-perform calculations against a **5% materiality level per CN code**. They treat complex or opaque data systems as an inherent risk, and they issue negative opinions when a number cannot be traced to primary records. That means the calculation engine, factor and default selection, allocation and final outputs must stay deterministic code, which is what carbonTraceAI already has. Agents add real value only at the messy edges: reading scanned and multilingual documents, mapping ERP item masters to CN codes, drafting verifier evidence packs, and later chasing missing data. Even there, they should only write proposals that a named human commits into the existing `raw_ref` audit trail. What SMEs and mid-caps on both sides of the border want in 2026 is verified actual data, produced cheaply and in time for the **first annual declaration on 30 September 2027**. What they lack most is verifier capacity: **zero CBAM-accredited verifiers as of July 2026**, against roughly **40,000 installations** that need verification. No competitor ships a CBAM agent, and nobody offers ERP-native, producer-side tooling for Sub-Saharan Africa, so that lane is open. Several founding assumptions no longer hold, though:

- **Mozal** has been on care and maintenance since **15 March 2026**.
- **Fertiliser defaults** carry only a **1% mark-up**.
- **The 2026 phase-in** makes this year's certificate cost small.
- **The Commission's free O3CI portal** already does the "share once with every buyer" job the moat plan counted on.

The recommendation has three parts. Build three narrow agents first: an evidence-pack drafter, a CN-mapping suggester, and a document-extraction assistant that ships only if it passes an accuracy test. Defer supplier outreach. Refuse any agent that computes, selects factors or submits. Before writing any agent code, re-validate the beachhead, the default-versus-actual economics and verifier acceptance.

## Buyers want verified actual data before September 2027, and verifiers are the choke point

CBAM's definitive regime has applied since 1 January 2026, but the money and paperwork come later. Certificate sales open on **1 February 2027**, and the first annual declaration and surrender for 2026 imports is due **30 September 2027** (moved from 31 May). The quarterly holding requirement has been cut from 80% to 50% of embedded emissions ([Mayer Brown](https://www.mayerbrown.com/de/insights/publications/2025/10/eu-adopts-cbam-simplification-regulation-10-key-amendments-and-challenges-ahead)). The Omnibus simplification (Reg. (EU) 2025/2083) replaced the per-consignment exemption with a **50-tonne annual threshold per importer**. That exempts about **182,000 importers, mostly SMEs and individuals**, while still covering more than 99% of embedded emissions ([European Commission](https://taxation-customs.ec.europa.eu/news/officially-published-simplifications-carbon-border-adjustment-mechanism-cbam-2025-10-20_en)). Verification is required only when an importer declares actual values rather than defaults, and verifiers could not register before 1 September 2026 ([Mayer Brown](https://www.mayerbrown.com/de/insights/publications/2025/10/eu-adopts-cbam-simplification-regulation-10-key-amendments-and-challenges-ahead)). The practical result is a demand peak for producer-side verified data that runs from now (October 2026) to roughly mid-2027. That is a narrow window, and it rewards whoever is verification-ready first.

### EU importers still rank supplier data as their top problem

The best survey evidence predates 2026, but it is consistent. In an IHK NRW survey of 2024, about **91%** of respondents named "information gathering from third-country suppliers" as their main challenge ([IHK NRW](https://www.ihk-nrw.de/blueprint/servlet/resource/blob/6265662/b62ce0024a4ab5f99610ffad4041051a/cbam-ergebnisse-umfrage-data.pdf)). In IHK Hessen's survey, almost **70%** rated the reporting portal unsatisfactory to very bad, and one firm reported that none of its suppliers had heard of CBAM ([IHK Frankfurt](https://www.frankfurt-main.ihk.de/international/beratung-kontakte/esg-compliance/cbam-umfrage-2024-6320252)). Aluminium consumers surveyed by FACE complained that they "repeatedly request and verify the same emissions data across the supply chain". They asked for a certified public registry of carbon values by installation and HS code, and they expect non-EU suppliers to absorb CBAM costs through lower prices ([FACE](https://face-aluminium.com/face-survey-results-impact-of-cbam-tariffs-and-supply-risks-on-the-aluminium-value-chain/)).

The 2026 complaints have shifted toward the regime itself. DIHK's June 2026 paper says there are not enough accredited verifiers for about 40,000 installations, so firms will be forced onto defaults. It also says the December 2025 default values sit "well above" earlier references and that responsibilities between customs, DEHSt and the EU portal are unclear. DIHK asks for a multilingual cost calculator and an EU self-assessment tool ([DIHK](https://www.dihk.de/de/newsroom/dihk-impuls-cbam-anpassungen-dringend-noetig-182882)). The Commission's own impact assessment puts the average importer's annual compliance cost at **€4,248 to €20,637** ([Commission SWD(2025) 988](https://taxation-customs.ec.europa.eu/document/download/71d4f753-4a2d-4367-bb10-c1967cb7f28d_en?filename=SWD_2025_988_1_EN_impact_assessment_part1_v4.pdf)).

After the Omnibus, the "SME importer" left in scope is mostly a mid-cap just over 50 tonnes with no compliance team, or a customs representative. Indirect customs representatives can now hold authorised-declarant status, and declarants can delegate submission to an EU-established third party ([Mayer Brown](https://www.mayerbrown.com/de/insights/publications/2025/10/eu-adopts-cbam-simplification-regulation-10-key-amendments-and-challenges-ahead)). That makes brokers a plausible distribution channel. carbonTraceAI should not try to build them a product.

### Non-EU producers lack MRV capacity, local verifiers and bargaining power

Monitoring, reporting and verification (MRV) capacity is the producer's problem, and on the producer side it is uneven. A 2026 South African aluminium policy brief says the major producers (Hulamin, South32 Hillside) already have emissions accounting systems. Accredited local verifiers are scarce, though, so firms depend on costly international services ([AFPH brief](https://img1.wsimg.com/blobby/go/b2d05cc3-7b8c-4f0d-a62a-66af7434f28f/downloads/f7ea9290-c2f9-4e3c-82b2-d08b90c4c0a0/AFPH_Policy%20Brief%20Aluminium%20Sector-12AUG.pdf?ver=1786527675602)). TIPS found South Africa's steel and aluminium sector "not ready financially and administratively" ([TIPS](https://www.tips.org.za/research-archive/sustainable-growth/green-economy-2/item/4791-tips-south-africa-iron-steel-and-aluminium-industries-readiness-to-respond-to-cbam)).

The ICC says the Commission's installation guide and communication template are too complicated for most suppliers, and that the Excel template's fields diverge from what the law actually requires ([ICC](https://iccwbo.org/news-publications/statement-letters/open-letter-on-the-carbon-border-adjustment-mechanism-cbam/)). Producers also treat production and energy data as commercially sensitive and fear it will weaken them in price negotiations ([Clean Carbon](https://cleancarbon.ai/blog/cbam-data-collection-from-vendors/)).

Hard costs are dominated by verification. Estimates range widely:

| Source | Estimate per installation |
|---|---|
| [The Trade Hub](https://www.thetradehub.eu/en/guides/cbam/verification) | **€3,000–15,000** |
| [cbamguide](https://cbamguide.com/importers/verification/) (vendor-sourced; complex fertiliser plants at the top end) | **€5,000–50,000** |

A small Indian exporter pays about ₹2 lakh (~€2,000) a year for a CBAM consultant ([The Wire](https://thewire.in/environment/how-the-eus-carbon-border-tax-is-reshaping-indian-msmes)). The underserved producer segment is therefore not the national champions. It is the mid-sized steel, cement and fertiliser plants and secondary aluminium processors that have no MRV system, buy verification from abroad, and get price-squeezed by EU buyers.

### Nobody yet has the inputs needed to finish the first cycle

Several pieces of the 2026 machinery are still missing:

- **Verifiers.** As of 11 July 2026, no verifier held CBAM accreditation, and the first accreditations were expected around September ([cbamguide](https://cbamguide.com/compliance/accredited-verifiers/)). This report found no figure for October.
- **Site visits.** A physical site visit is mandatory in an installation's first verification year ([EUR-Lex 2025/2546](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2546)).
- **Registry mechanics.**
  - Only one verifier can be active per installation in the Registry.
  - Declarants must hand their EORI numbers to operators outside the Registry.
  - A saved record is not a verified one.

  ([Materia Intel](https://www.materiaintel.com/insight/cbam_registry_o3ci_operator_verifier_portal))
- **Declarations module.** DEHSt said declarations could not yet be created in the Registry and expected that capability from Q4 2026.
- **Carbon-price deduction.** The implementing act on deducting third-country carbon prices was still pending ([DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)).
- **Communication template.** A third party reports the template is still v2.1 from December 2024, built for the transitional period ([cbamfile](https://cbamfile.com/cbam-news)).
- **System-to-system interface.** German chambers have asked for one because Excel upload does not scale; none exists ([DIHK](https://www.ihk.de/blueprint/servlet/resource/blob/6348374/5c473efffb95b8836201da1c33abc1be/dihk-stellungnahme-cbam-register-data.pdf)).

The honest caveat is that hard 2026 quantitative evidence is thin. Most current "pain point" material is association advocacy or vendor content, and no survey measures how many hours each CBAM task actually takes.

## Six findings break the current beachhead and moat assumptions

The product's technical core is sound. Several of the commercial premises written into `docs/IDEA.md` and baked into the demo data are not. The table summarises them, and the paragraphs that follow explain the three that matter most.

| Current assumption | What the evidence says | Implication |
|---|---|---|
| Mozal is a beachhead profile; the demo shows "Mozal Q2 2026: 204,207 tCO2e" | South32 put Mozal on care and maintenance on **15 Mar 2026** after failing to secure affordable power ([Engineering News](https://engineeringnews.co.za/article/south32-places-mozal-on-care-and-maintenance-2026-03-16)) | The smelter produced essentially nothing in Q2 2026. A demo titled "Mozal Q2 2026" discredits the product with any informed buyer, investor or verifier. Rename it as a generic primary-aluminium profile and re-target. |
| Demo "CBAM cost €6.74M" for the quarter | Certificates cover about **2.5%** of embedded emissions in 2026 (CBAM factor 97.5%), rising to 100% by 2034 ([Werksmans/Polity](https://www.polity.org.za/article/south-african-exporters-take-note-2026-08-21)). Egyptian urea's net 2026 cost is under €5/t against a gross €172–195/t ([cbamguide Egypt](https://cbamguide.com/countries/egypt/)) | If the phase-in applies as described, 204,207 t × 2.5% × the reported Q3 2026 price of €82.32 ([cbamguide](https://cbamguide.com/software/best-cbam-software/)) is roughly **€0.4M**, not €6.7M. The exact figure depends on the benchmark-based free-allocation adjustment. The importer pays it, not the producer. The 2026 ROI story must be about protecting contracts and the 2027–2030 ramp, not about this year's cash. |
| Fertiliser (OCP) is the second beachhead and avoiding default penalties is the pitch | Default mark-ups are 10/20/30% for steel, aluminium and cement but a **flat 1% for fertilisers** until re-evaluation by end-2027 ([Luxembourg CA](https://environnement.public.lu/fr/emweltprozeduren/Autorisations/cbam-en/cbam-certificated-and-price.html)) | The fertiliser pitch only works where actuals are well below the country default. Verification is required only for actuals, so a fertiliser importer facing a 1% mark-up may rationally skip actuals altogether. |
| Verifier partnerships (DNV, TÜV, BV) as a referral channel | **Zero** CBAM-accredited verifiers as of July 2026 ([cbamguide](https://cbamguide.com/compliance/accredited-verifiers/)); verifiers also sell competing "pre-verification" services ([SGS](https://www.sgs.com/news/2026/05/cbam-pre-verification-changing-the-narrative)); a local Moroccan verifier network already exists ([virESG](https://viresg.com/en/cbam-morocco)) | Scarce verifiers have no reason to refer clients. Treat them as the user you design the audit view for, not as a sales channel. Whether a verifier can refer clients to a data tool without compromising its impartiality is untested and should be asked. |
| Moat via a shared "verified-EE directory" and supplier-portal network effects | The O3CI portal lets operators upload installation data once and share it with all declarants, with verification status visible ([DEHSt](https://www.dehst.de/EN/Topics/CBAM/CBAM-definitive-regime-2026/cbam-definitive-regime-2026_node.html)); CarbonChain runs a free public catalogue of steel and aluminium installations ([CarbonChain](https://www.carbonchain.com/cbam)) | The regulator built the share-once directory and gives it away. The moat must be in *preparing* O3CI-ready, verifier-proof data, not in distributing it. |
| EU XML for declarant upload and an "estimation >20%" verifier flag | Producers enter data in O3CI and the *declarant* files the annual declaration ([Commission CBAM Registry](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry-and-reporting_en)). The 20% estimate cap was a transitional-period rule ([SGS eCustoms](https://ecustoms.sgs.com/2024/07/22/the-start-of-the-transitional-period-for-cbam/)). In the definitive period, estimation methods must be in the monitoring plan and conservative, and any data gap is a misstatement ([Commission verification guidance §4.8](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)) | The XML mapped to the transitional reporting act and the 20% flag both target the wrong regime and the wrong actor. The producer deliverables are an O3CI-ready installation record, a filled communication template, a monitoring-methodology document and a verifier evidence pack. |

Mozal is the most visible break, but the aluminium thesis also suffers more broadly. An estimated 14–47% of Mozambique's exports fall under CBAM ([Energy Monitor](https://www.energymonitor.ai/carbon-markets/how-cbam-threatens-africas-sustainable-development/)), and that exposure sat almost entirely in one smelter that has now stopped. South Africa's large aluminium producers already run emissions accounting. So the more immediate African targets lie elsewhere. One is South African iron and steel, with an estimated USD 1.66bn of exposed exports; there the domestic carbon tax gives a deduction lever, but only with verified data ([cbamguide countries](https://cbamguide.com/countries/); [Lex Africa](https://lexafrica.com/2026/09/south-african-exporters-face-rising-costs-under-eu-carbon-rules/)). The other is mid-sized fertiliser plants in Egypt (USD 1.25bn) and Morocco (USD 0.72bn), with Algeria close behind ([SOAS](https://www.soas.ac.uk/sites/default/files/2026-05/16%20Persenda%20CBAM.pdf)).

OCP itself is a weak first customer. It targets 100% renewable electricity by 2027 and is investing $7bn in green ammonia ([Hespress](https://en.hespress.com/127493-127493.html)), which suggests in-house or Big-4 MRV capacity. Morocco already has a local competitor, virESG, which offers French and Arabic and a local verifier network. Morocco's CESE also says only 3.7% of trade with the EU is affected ([FNH](https://fnh.ma/article/developpement-durable/macf-union-europeenne-bilan-industriels-marocains)).

There is an offsetting positive. The proposed downstream extension would add about 180–200 steel- and aluminium-intensive products from 2028. The Council adopted its general approach on 12 June 2026, but the extension is not yet law ([Reed Smith](https://www.reedsmith.com/our-insights/blogs/trade-compliance-resource-hub/4874/commission-proposes-expansion-of-eu-cbam-to-downstream-goods-and-addresses-potential-cbam-abusive-practices/); [OneStopESG](https://onestopesg.com/esg-news/eu-cbam-carbon-border-tax-expansion)). If it passes, a second and much larger wave of fabricators would join scope. Many of them run mid-market ERPs and have no MRV capability, which fits carbonTraceAI's ERP-native wedge better than smelters do.

The "Africa-specific sector defaults" moat also deserves scepticism. Default values are fixed by the EU per country in Implementing Regulation 2025/2621, and the Commission publishes them in Excel ([Finnish Customs](https://tulli.fi/en/-/the-default-values-and-benchmarks-for-the-cbam-definitive-period-have-been-published-in-excel-format-there-are-also-new-guidance-videos-on-the-cbam-registry)). Anyone can load them. The defensible asset is the *actuals* pipeline, together with the evidence that makes those actuals verifiable.

## Deterministic code covers the regulated core; agents only help at the messy edges

The question "is an agentic workflow necessary?" has a precise answer once you look at what verifiers do. They are not asked to trust software. They are asked to re-perform it.

### Verifiers re-perform calculations, so every number must be reproducible

The Commission's 141-page verification guidance of 24 August 2026 never mentions artificial intelligence. A full-text search finds only "artificially coloured" in a cement CN description. The guidance is still structurally hostile to unexplained numbers ([Commission guidance](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)). Its key requirements are:

- **Assurance and materiality.** Verifiers work to reasonable assurance at a **5% materiality level per CN code**, and "materiality is not a tolerance band": every identified misstatement must be corrected.
- **Inherent risks.** Verifiers must apply professional scepticism. They are to treat complex data management systems, manual transfers between systems, incorrect emission-factor use, and incorrect precursor identification as inherent risks.
- **Control risks.** Missing segregation between data input and data checking is a control risk.
- **IT systems.** IT systems must be "designed, documented, tested, implemented, controlled and maintained".
- **Estimates and data gaps.** Estimates are allowed only if the monitoring plan defines them and they do not underestimate emissions. Data gaps count as misstatements.
- **Grounds for a negative opinion.** Missing primary data, or a methodology the verifier cannot follow, triggers a "limitation of scope", which is a form of negative opinion.

An LLM-generated emission value fails these tests in three ways. A re-run gives a different answer, so the verifier cannot re-perform it. An agent that both enters and checks data breaks segregation of duties. And an undisclosed AI choice of default value is exactly the "incorrect selection" verifiers are told to check. carbonTraceAI's deterministic engine and `raw_ref` chain already pass these tests by construction, which makes them the verifier-facing asset. Whether an AI layer raises a verifier's inherent-risk rating, and so increases sampling and fees, is an untested inference. No verifier has published a position on it.

### Reliability evidence splits cleanly by task

The research literature lines up task by task:

| Task | Best evidence on LLM accuracy | What it means for carbonTraceAI |
|---|---|---|
| **Arithmetic** | LLM accuracy drops by up to **65%** when a single irrelevant clause is added ([Apple GSM-Symbolic](https://arxiv.org/html/2410.05229v2)). | No LLM should touch the arithmetic, and none needs to, because the engine exists. |
| **HS/CN classification** | Best fine-tuned model: **40%** exact at 10 digits, **57.5%** at 6 digits. GPT-5-Thinking: 25% at 10 digits ([ATLAS, arXiv 2509.18400](https://arxiv.org/abs/2509.18400)). A commercial test found 6% of AI suggestions were entirely hallucinated codes ([TariffTel](https://www.tarifftel.com/blog/can-ai-give-you-an-accurate-tariff-code/)). | Autonomous classification is unacceptable. Constrained shortlists with human confirmation are reasonable, because CBAM's Annex I is a small, closed set of codes. No CBAM-specific benchmark exists to confirm this. |
| **Emission-factor matching** | Amazon's Parakeet: **86.9%** top-1 and **93.1%** top-10 ([Amazon Science](https://www.amazon.science/publications/parakeet-emission-factor-recommendation-for-carbon-footprinting-with-generative-ai)). | This is Scope 3 spend matching. In CBAM the factor values are fixed by law, so the useful transfer is mapping messy ERP item names to categories, not choosing factors. |
| **Document extraction** | Top key-field extraction score is about **91** on a vendor leaderboard ([Nanonets](https://nanonets.com/blog/idp-leaderboard-1-5/)). One test fell from 83.8% to **68.1%** once line-item tables were included ([HackerNoon](https://hackernoon.com/can-your-llm-handle-an-invoice-i-tested-5heres-the-truth)). | Useful, but every field needs validation against the 5% materiality budget. |
| **Regulatory Q&A** | Commercial legal tools built on retrieval-augmented generation (RAG) hallucinated **17–33%** of the time ([Stanford HAI](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-queries)). | That disqualifies authoritative compliance answers. |

The materiality arithmetic makes the extraction point concrete. If one fuel invoice in ten is misread and nobody catches it, the error can exceed 5% of a good's specific embedded emissions. LLM extraction is acceptable only with cross-footing, unit checks, an ERP quantity match and human confirmation of low-confidence fields.

### Most agent projects fail, and CBAM is mostly a well-defined task

The adoption evidence counsels restraint. Gartner predicts more than **40% of agentic AI projects will be cancelled by end-2027**, citing "escalating costs, unclear business value or inadequate risk controls". It also estimates that only about 130 of thousands of "agentic" vendors are real, with the rest "agent washing" ([Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)). McKinsey finds 88% of firms use AI, but only **39%** report any enterprise-level EBIT impact, and most of those put it under 5% ([McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-state-of-ai-2025)). MIT NANDA's widely quoted "95% see no return" rests on a weak sample ([critique](https://robtlee73.substack.com/p/the-genai-divide-report-a-masterclass)), so it should not carry weight.

Anthropic's own engineering guidance draws the relevant line. Predefined workflows suit well-defined tasks where predictability matters, agents suit open-ended problems, and builders should find "the simplest solution possible" ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents)). CBAM compliance — ingest, calculate with legally fixed formulas, render a fixed schema — is a predictable workflow. Only a few sub-tasks are open-ended, such as chasing a non-responsive supplier or interpreting a free-text verifier query.

### The AI Act costs little; data sovereignty is the real objection

A CBAM extraction or classification agent fits none of the AI Act's Annex III high-risk categories. In addition, the Digital Omnibus (Reg. (EU) 2026/1744, in force 27 July 2026) postponed Annex III obligations to 2 December 2027 ([Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/eu-digital-omnibus-on-ai-enters-into-force); [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)). Article 50 transparency duties have applied since 2 August 2026, so any chat-style assistant must tell users they are dealing with AI ([AI Act Art. 50](https://artificialintelligenceact.eu/article/50/)).

The sharper constraint is moving data across borders. Nigeria's data protection commission (NDPC) fined MultiChoice NGN 766m, partly for unlawful cross-border transfers ([Mondaq](https://www.mondaq.com/nigeria/privacy-protection/1798234/cross-border-data-transfers-and-international-compliance-legal-opportunities-in-global-tech-transactions)). South Africa's POPIA restricts transfers to jurisdictions with substantively similar protection ([BBD Software](https://bbdsoftware.com/article/data-residency-sovereignty-what-african-and-eu-firms-must-know/)). Most CBAM data is not personal, but invoices and supplier emails are. Producers' bigger fear is commercial: that their production volumes leak into a buyer's price negotiation. A self-hostable fine-tuned model for classification was about 5× cheaper than a frontier reasoning model ([ATLAS](https://arxiv.org/abs/2509.18400)). A design with redaction, zero-retention contracts and a self-hosted fallback therefore removes a sales objection at modest cost.

### Steelmanning the case for agents

The best argument for agents is that the labour sits in data capture, and supplier non-response is what pushes firms onto penalising defaults. The Commission calls defaults "the very last resort" ([Commission guidance §2](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)). French, Arabic and Portuguese scanned invoices are also where a vision-language model could plausibly beat Tesseract plus rules. And no competitor has a credible CBAM agent, so differentiation is available. These are real points. They support narrow, bounded LLM steps at intake and drafting. They do not support an agentic core, and nothing in the evidence says buyers will pay for "agentic" as a label.

The task map below is the defensible split. It follows the regulated-workflow framework in the research notes and the verifier risk list.

| Task | Deterministic code or LLM? | Pattern |
|---|---|---|
| Emission calculation, uncertainty, allocation, reconciliation | **Deterministic only** | Existing engine; verifier must be able to re-perform |
| Selecting emission factor, default value or methodology tier | **Deterministic only** | Priority rules in code per IR 2025/2547 and 2025/2621 |
| Final XML / O3CI entry / Registry submission | **Deterministic + human** | Renderer plus human approval; legally attributable act |
| Default-vs-actual cost decision per product and year | **Deterministic** | Calculator aware of mark-ups (including the 1% fertiliser exception) and the CBAM factor |
| Anomaly detection (month-over-month jumps, mass balance, ERP-vs-invoice mismatch) | **Deterministic detection, LLM explanation** | Reproducible rules flag the issue; LLM drafts possible causes |
| Template / XSD pre-validation | **Deterministic validator, LLM explanation** | Validator decides; LLM explains failures in plain language |
| Document extraction from scans and multilingual bills | **Bounded LLM step** | Extract → schema validation → cross-checks → human confirms low-confidence fields |
| ERP item master → CN code / precursor category | **LLM suggestion** | Constrained to the Annex I list; top-k candidates with a rationale; human confirms; mapping versioned and reused deterministically |
| Monitoring methodology narrative and verifier evidence pack | **LLM draft** | Numbers inserted by reference from the store, never generated; human signs |
| Precursor-supplier and buyer-request loops | **The one true agent case** | Multi-turn and unpredictable; every outbound message human-approved; replies parsed into candidate records |
| Regulatory Q&A "copilot" | **Do not build** | 17–33% hallucination in mature legal RAG |

## Competitors cluster on the importer side, and none ships a CBAM agent

The CBAM software market has three layers. CBAM-only specialists sell mainly to EU declarants. Broad ESG and supply-chain suites have bolted on CBAM modules. ERP incumbents are arriving late. Prices are mostly quote-based, and the only "AI" in CBAM tools is branding or chatbots ([cbamguide](https://cbamguide.com/software/best-cbam-software/); [Coolset](https://www.coolset.com/academy/top-cbam-software-tools-7f11d)).

| Vendor | Side / region | What it does | Pricing | Gap or lesson for carbonTraceAI |
|---|---|---|---|---|
| CarbonChain (London, $10M Series A 2023) | Both; commodity traders and installations | Supplier outreach, in-house validation, installation modelling, SGS-validated product-footprint method, free public installation catalogue ([CarbonChain](https://www.carbonchain.com/cbam)) | Quote | No ERP integration or AI mentioned. Lesson: third-party methodology validation sells trust. |
| CBAMBOO (London) | Importer-first, free supplier side | Supplier calculation, "verification-ready" reports, XML "compatible" with the registry ([cbamguide](https://cbamguide.com/software/cbamboo/)) | €9k / €19k / €31k per year (third-party, unverified) | Importer-paid supplier portals make the producer side free, which is a direct pricing threat. |
| kolum, Dubrink (EU) | Importer mid-market | Supplier invitations in 20+ / 15 languages, actual-vs-default per CN code, XML, audit trail ([kolum](https://www.kolum.earth/en/cbam/product); [Dubrink](https://www.dubrink.com/cbam-compliance-for-importers)) | Custom | No Arabic; no producer ERP ingestion. |
| CbamTrack | SMB importer self-serve | Communication sheet, supplier portal, XML/Excel/JSON, anomaly detection, what-if simulator ([CbamTrack](https://cbamtrack.com/pricing)) | €0 / €79 / €199 per month | Shows the price floor; exposed after the Omnibus removed small importers. |
| osapiens, IntegrityNext, Carbmee, Sphera, Assent, VERSO | Suites with a CBAM module | Supplier data collection, cost exposure, XML; Assent has an AI chatbot for suppliers ([osapiens](https://osapiens.com/en/solutions/carbon-management/cbam); [Assent](https://www.assent.com/solutions/esg-supply-chain/cbam/)) | Quote | Importer workflows; no producer-side depth for emerging markets. |
| SAP (Jun 2026) | Declarant-first, operator support "later" | Green Ledger CBAM liabilities live; data capture, dashboard and reports "coming soon"; supplier Excel with "automated interpretation" ([SAP News](https://news.sap.com/2026/06/sap-introduces-cbam-declarants-solution/)) | Enterprise | Even SAP had no complete CBAM product by mid-2026. A future operator module is the long-term threat for SAP-run producers. |
| virESG / virCBAM | Producer, Maghreb | XML, utility (ONEE) electricity-data integration, Moroccan grid factors, **EN/FR/AR**, local verifier network claimed 40–50% cheaper ([virESG](https://viresg.com/en/cbam-morocco)) | Not shown | Closest analogue. It already occupies Morocco and could move south. |
| Sustrack S-CBAM, Karbonet (Türkiye) | Producer | Monitoring plan and emissions reports from production data; read-only verifier access; national default table ([Sustrack](https://sustrack.ai/products/s-cbam); [Karbonet](https://karbonet.com/cbam-software)) | Not shown | Integrations are per project, not ERP-native. Lesson: give verifiers read-only access. |
| CarbonSettle, CleanCarbon.ai, The Sustainability Cloud (India) | Producer MSMEs | Managed "send us bills, we file" service with a free first quarter; consultancy plus "AI-based" software claiming 200+ exporters; aggressive SEO pages for Egypt and Algeria ([CarbonSettle](https://carbonsettle.com/cbam-steel-exporters-india); [CleanCarbon.ai](https://cleancarbon.ai/); [TSC Egypt](https://www.thesustainabilitycloud.com/blog/cbam-software-in-egypt/)) | Free first quarter; otherwise quote | SME producers buy outcomes, not software. Low-cost Indian services are the price competitor in Africa. |

Three gaps are clear. First, no Sub-Saharan CBAM software vendor was found; South Africa has only consultancies and certifiers such as TÜV Rheinland, SCS and Anthesis ([TÜV SA](https://www.tuv.com/south-africa/en/lp/cbam-and-environmental-services/)). Second, no vendor offers ERP-native ingestion on the producer side. Third, Portuguese and Arabic support is rare. Those gaps are carbonTraceAI's lane.

The competitive risks are real too. The importer may simply hand the producer a free supplier portal. Indian managed services undercut on price. And the post-Omnibus importer market is about a tenth of its former size by count. That last point explains why self-serve importer tools look exposed, and why general carbon-software consolidation continued through 2026: Diginex bought Plan A at about €55M, and Greenly reportedly bought Normative ([Dealroom](https://app.dealroom.co/news/note/lightspeed-backed-carbon-accounting-startup-plan-a-acquired-by-diginex-in-55m-deal); [Clean the Sky](https://www.cleanthesky.com/innovation/climate-data-company)). The number of non-EU producers did not shrink, which makes producer-side demand the more resilient segment.

### Agent tools outside CBAM show the copyable patterns

Leading carbon and trade platforms have shipped agents, and the serious ones share a design. The LLM proposes. A ledger or engine computes. A human approves.

| Product | What shipped | Pattern worth copying |
|---|---|---|
| Watershed | A Mapper agent matches messy procurement text to emission factors, and a separate Judge agent scores each match blind. Reported results: 98.9% "defensible" on the Parakeet set, 90.7% on a harder 1,039-item set, and about 0.3% error on matches the Judge rates high ([Watershed](https://watershed.com/blog/how-we-benchmark-and-measure-the-accuracy-of-watershed-ai-for-emissions-factor-mapping)). It also runs data-cleaning agents "with documented assumptions" ([Watershed 2026](https://watershed.com/blog/sustainability-ai-in-2026-what-works-what-doesnt-and-why-the-difference-matters)). | Mapper/Judge separation with a confidence-routed human queue, which fits CN and precursor mapping directly. |
| Sweep "Sweepy" (22 Sep 2026) | Takes an outcome and orchestrates the tasks; claims ">90%" faster turnaround; approval-gate details undisclosed ([EIN Presswire](https://www.einpresswire.com/article/943872581/sweep-takes-ai-beyond-assistance-to-run-end-to-end-sustainability-workflows)) | Outcome-level UX, but undisclosed gates are exactly what a verifier would question. |
| Persefoni Analytics Agent (5 May 2026) | Natural-language analytics on top of a traceable "CO2e Activity Ledger" ([NetZero Compare](https://netzerocompare.com/articles/persefoni-launches-ai-agent-to-help-companies-analyze-emissions-data-faster)) | Read-only agent over a deterministic ledger. |
| ServiceNow sustainability document intelligence | Highlights AI-extracted fields and requires a justification for any override ([ServiceNow](https://www.servicenow.com/docs/r/s82Zw_idTcTEahshu77BGw/qb7nfXduz_10xuazJfw~xA)) | Flag-and-justify UI that writes straight into an audit trail. |
| Altana + Cervo AI (21 Jul 2026) | "Fully-agentic" customs-entry writing from unstructured data, a deal possibly over $100M ([BusinessWire](https://www.businesswire.com/news/home/20260721109771/en/Altana-Acquires-Cervo-AI-to-Deliver-End-to-End-Agentic-AI-Platform-for-Customs-Brokerage)) | Proof that agentic drafting of regulated filings is fundable. A broker still files the entry. |
| Norm Ai | Regulations encoded as checking agents; a compliance agent inside Microsoft 365 Copilot with an audit trail ([PR Newswire](https://www.prnewswire.com/news-releases/norm-ai-launches-compliance-agent-for-microsoft-365-copilot-302769123.html)) | "Regulation as checker", useful for an internal reg-watch tool. |

In CBAM itself the field is empty. Microsoft's "EU CBAM Copilot" was a fee estimator, and its documentation is archived ([Microsoft Learn](https://learn.microsoft.com/en-us/industry/release-plan/2024wave2/cloud-sustainability/estimate-carbon-fee-eu-cbam-copilot)). The only agentic CBAM declaration builder found is a hackathon demo, CarbonLot ([NitroStack](https://nitrostack.ai/university/6a47e78ac305f1c3b0338b94/submissions/6a5b2a9712494ab65b9364cc)). Watershed itself warns that general-purpose LLMs "cannot distinguish a defensible estimate from a hallucinated one", and that multi-agent pipelines without logging break the calculation lineage auditors follow ([Watershed](https://watershed.com/blog/sustainability-ai-in-2026-what-works-what-doesnt-and-why-the-difference-matters)). The strongest market positioning is the one Watershed and Persefoni already use: no LLM touches the arithmetic.

## Agents should write proposals that a human commits into raw_ref

The safe pattern adds a small, explicit layer between the LLM and the canonical store. It maps one-to-one onto what verifiers check: IT quality assurance, segregation of duties, an audit trail, and conservative gap-filling.

**Candidates, not facts.** Every LLM output lands in a `candidates` table with status `proposed`. Only a human action promotes it to the canonical store, or, for low-risk fields, a deterministic validator above a threshold. The approver must hold a different role from the uploader, which preserves the segregation of duties the guidance names ([Commission guidance](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)).

**`raw_ref` provenance, extended.** Today `raw_ref` points to the source JSONL and the ERP document. Extend it to also record:

- the source document's hash, page and bounding box;
- the model ID and version, and the prompt-template version;
- the raw model output and its confidence;
- the approver and the timestamp.

The log must be append-only. Never re-run a model to "reproduce" a result. The stored output is the evidence.

**Numbers by reference.** Agents call the calc engine, the defaults table and the validators as tools. Drafted evidence packs embed values as template variables resolved from the store, so no generated sentence can contain an invented figure.

**Abstention instead of guessing.** A field below the confidence threshold goes to a human. Missing data is never filled by an LLM. It goes either to supplier chasing or to a conservative estimation method already documented in the monitoring plan, flagged as such.

**Disclosure to the verifier.** AI-assisted fields are marked in the evidence pack so the verifier can target its sampling. That turns AI from a hidden risk into a documented control.

**Hard deny-list.** Agents never submit to the Registry, never buy or surrender certificates, never accept a verifier collaboration request, and never send a message without approval. Enforce this by withholding those tools entirely.

The SDKs provide pause points but not the surrounding machinery. LangGraph has `interrupt()` with durable checkpointers ([LangChain](https://docs.langchain.com/oss/python/langgraph/interrupts)). The OpenAI Agents SDK has `needs_approval` ([OpenAI](https://openai.github.io/openai-agents-python/tools/)). The Claude Agent SDK has PreToolUse hooks that return allow, deny or ask, with deny taking precedence ([Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/permissions)). None of them supplies notifications, timeouts, escalation or audit records ([The Handover](https://thehandover.xyz/blog/openai-agents-sdk-needs-approval)). The approval queue in the Next.js dashboard, showing a diff, evidence links, confidence and a reasoning summary, is therefore product work carbonTraceAI must build itself, and it is the real asset.

The Registry's own semantics already demand explicit state tracking. Uploading XML creates only a draft ([Commission webinar](https://customs-taxation.learning.europa.eu/pluginfile.php/34802/mod_resource/content/1/SDEV-CBAM-DECLARANTS-TRM-Webinar.pdf)), and a saved O3CI record is not a verified one. An installation-year state machine (data complete → calculations frozen → verifier linked → evidence pack ready → verified → shared with buyers by EORI) should therefore come before any orchestrating agent.

Two disciplines keep the agent work honest. First, an evaluation set built from pilot documents, roughly 200–500 labelled bills, invoices, certificates and ERP item lines. It should be re-run on every model or prompt change and included in the IT-QA file verifiers will ask for. Second, kill criteria. If an LLM step does not beat the existing pdfplumber + Tesseract + rules pipeline by a pre-agreed margin on both field accuracy and human review time, it does not ship. That directly addresses the "unclear business value" failure mode behind Gartner's 40% cancellation forecast.

The build order follows dependency and the calendar, not novelty:

| Phase | Timing | Build | Gate before moving on |
|---|---|---|---|
| 0. Deterministic foundations | Now → Dec 2026 | Default-vs-actual economics calculator (mark-ups, 1% fertiliser rule, CBAM factor, carbon-price deduction); O3CI-ready installation record and communication-template round-trip parser; switch from transitional to definitive-period rules; installation-year state machine; `candidates` table, approval queue and extended `raw_ref`; auth and multi-tenancy | A pilot customer's real data runs end-to-end; the calculator shows actuals beat defaults for that customer |
| 1. Onboarding agents | Q4 2026 → Q1 2027 | CN / precursor mapping suggester (Mapper/Judge, closed Annex I list); document-extraction assistant behind the existing OCR | Eval set built; extraction beats the OCR baseline; mapping top-3 accuracy measured on the pilot's item master |
| 2. Verification-season agent | Q1 → Q2 2027 | Monitoring-methodology and evidence-pack drafter; verifier-query response drafter, with numbers by reference only | One accredited verifier reviews a pack in a dry run and confirms it saves time and that disclosed AI fields are acceptable |
| 3. Outreach agent | After the first verification cycle (H2 2027) | Buyer-request inbox and precursor-supplier chasing, with every send approved, replies parsed into candidates and EORI distribution tracked; internal reg-watch (deterministic EUR-Lex diff plus LLM summary with verbatim citations) | Measured hours on chasing justify it; customers consent to the messaging channels |

## Build three agents, defer one, refuse five

The recommendation is deliberately narrow. Each agent chosen has a bounded output, a deterministic check behind it, and a direct link to the scarcest resource in the 2026–27 cycle, which is verifier time.

| Build first | Why it earns its place | Hard limits |
|---|---|---|
| **1. Evidence-pack and monitoring-methodology drafter** | First-year physical site visits plus scarce verifiers make verification-ready documentation the most valuable output. The `raw_ref` graph already holds everything it needs. | Numbers come only from the store via template variables. A human signs. AI-drafted text is labelled. |
| **2. CN-code / precursor mapping suggester** | Lowers onboarding cost for each new customer, which is the services-to-product lever. Works on a closed label set. Proven Mapper/Judge pattern. | Top-k candidates with a rationale. A human confirms. The mapping is versioned once and then reused deterministically. |
| **3. Document-extraction assistant** (conditional) | SMEs without clean ERP data hold their activity data in bills and certificates, often French, Arabic or Portuguese scans. | Ships only if it beats Tesseract plus rules on the eval set. Page and bounding-box provenance. Low-confidence fields go to a human. |
| **Defer: outreach agent** | The only genuinely open-ended loop. Integrated producers have fewer upstream precursor suppliers, so the value is unproven until it is measured. | Every outbound message human-approved. |

The refuse list matters as much. Do not build an LLM that computes emissions or uncertainty. Do not let an agent select emission factors, default values or methodology tiers. Do not build a conversational CBAM regulatory copilot, given the 17–33% hallucination rates. Do not let anything autonomously submit to the Registry, accept verifier collaborations or act on certificates. Do not build a multi-agent "orchestrator" over the whole lifecycle before the deterministic state machine exists. Browser automation of the O3CI portal also stays off the list until the Registry's terms of use are checked. And drop "agentic" as the headline positioning. Given Gartner's warnings about agent washing, "deterministic, verifier-ready, with AI-assisted data capture" is the stronger claim with sophisticated buyers. That positioning is a judgement call, not a sourced finding.

Validate before writing agent code. Each step below has a pass condition that would change the plan.

| Validation step | Question it answers | Pass condition |
|---|---|---|
| Replace the Mozal profile and run 10–15 discovery calls with South African steel and aluminium processors and mid-size Egyptian and Moroccan fertiliser plants | Is there a reachable buyer who is neither shut down nor already served by in-house MRV or virESG? | At least 3 producers confirm EU buyers are demanding actuals and that they lack an MRV system |
| Run the default-vs-actual calculator on each prospect | Do actuals beat defaults by more than the cost of verification plus software? | A positive margin for 2027 and 2028 at realistic verification fees (€3k–50k) |
| Pre-verification dry run with one accredited verifier (once accreditations exist) | Does the `raw_ref` audit view cut verifier days, and are disclosed AI-assisted fields acceptable or a risk flag? | Verifier states a time saving and raises no inherent-risk objection |
| Time study during the pilot | Where do the hours actually go: extraction, mapping, chasing or evidence assembly? No source quantifies this | Agent priority confirmed by measured hours |
| Labelled eval set on the pilot's documents | Does a VLM beat pdfplumber + Tesseract on African multilingual scans? | Pre-agreed margin on field accuracy and review time |
| Pricing test against €499/facility/month (~€6k/yr) | Will producers pay against a free first quarter from CarbonSettle, ~€2k/yr consultants and free importer portals? | An LOI at or near the proposed price, or a validated outcome-based price (for example, priced per verified installation-year) |
| Data-residency check with the pilot | Is an external LLM API acceptable for invoices and ERP extracts? | Written acceptance, or a confirmed need for redaction or self-hosting |
| Confirm O3CI upload formats and the definitive communication template | Can output be bulk-uploaded, or is manual entry required? | Documented format, or a manual-entry helper scoped instead |

## Conclusion

The research reframes what carbonTraceAI sells. The product is not CBAM compliance software in the abstract. It is a way to make a scarce, newly accredited verifier's job cheaper and faster for producers whose EU buyers now hold the liability. On that framing the deterministic engine and the `raw_ref` chain are the product, and agents are a productivity layer whose job is to make the verifier's sample easy to draw and quick to check. Agents are not themselves a selling point. That also explains why the first sale is likely to be a verification-readiness engagement for the 2026 data year, timed against verifiers' first physical site visits, rather than a self-serve subscription. And it explains why the 2026 cost numbers should not lead the pitch, since the money only becomes material as the CBAM factor falls toward 2030.

The geography and sector story should shift accordingly: away from one shut-down smelter and a fertiliser segment with a 1% mark-up, and toward South African steel, mid-size North African fertiliser plants where actuals clearly beat defaults, and above all the downstream fabricators who would join scope from 2028 if the extension passes. Those firms run mid-market ERPs and have no MRV teams, which is where an ERP-native, multilingual, verifier-proof pipeline has no current competitor. The biggest unknown is not technical. Nobody yet knows how the first cohort of CBAM verifiers will treat AI-assisted data, and one dry run with one verifier is worth more than any agent feature built before it.
