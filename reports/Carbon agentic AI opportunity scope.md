# Change the buyer, not the engine: where carbonTraceAI's agents can earn money

*Research synthesis, 21 October 2026. It builds on two earlier reports in this folder: `CBAM agentic workflow market research.md` (the "CBAM report") and `Agentic AI sustainability opportunities.md` (the "opportunities report"). It also draws on five new research notes in `research_notes/Carbon agentic AI opportunity scope/`.*

## Executive summary

**Bottom line.** The best new idea for carbonTraceAI is not a jump into a different carbon market. It is a change of buyer and of product unit, on top of the engine the team already has. The pitch becomes a **"verifier-ready carbon evidence layer" for emerging-market heavy industry**. One plant's ERP (enterprise resource planning), meter and invoice data would be turned into the filings that plant owes under every carbon regime it faces:

- South Africa's carbon tax, including its larger offset allowance;
- South Africa's national greenhouse-gas (GHG) reporting;
- the EU and UK carbon border adjustment mechanisms (CBAM).

The same data would feed the CBAM-exposure reports that Egyptian banks now owe their regulator. Agents prepare paperwork, deterministic code does all the maths, and a named engineer, tax practitioner, banker or accredited verifier signs.

I re-scored 18 candidates on the six-criterion checklist from the opportunities report. Only three clear the bar of at least 9 out of 12 with no zero on mandate or payer:

1. **Multi-regime installation MRV (measurement, reporting and verification)**, built around South Africa: **10/12, build now.** The new evidence strengthens it. South Africa kept its 60% basic tax-free allowance to 2030, raised its offset allowance to 15% for combustion and 10% for process emissions, and ended the carbon-budget allowance. A R640/t penalty for exceeding carbon budgets is pending. Only one software vendor targeting this market was found.
2. **South African carbon-tax offset-allowance module**: **9/12, build inside #1.** It serves the same customers, and the first returns under the new limits fall due in July 2027.
3. **Egypt central-bank (CBE) CBAM-exposure screening for banks**: **9/12, the top channel experiment.** This reframes the earlier "banks pay for borrower data" idea (8/12). In its general form that idea is now downgraded to 5/12, because disclosure rules for banks were loosened in 2025–26.

The research also refines the earlier verdict to avoid carbon credits:

- **Generic voluntary-market project MRV** falls to 2/12. Prices averaged $3.50/t and primary market value has been flat for four years.
- **An "authorised-credit evidence agent"** for African cookstove, biodigester and methane developers selling into CORSIA (the aviation offsetting scheme) and Article 6 scores 8/12. It is worth a time-boxed test as a module, with hard kill criteria. Its ceiling is about $1–5M ARR (annual recurring revenue) in Africa.

The cross-cutting finding is that **verifiers are scarce in every new regime**. EU CBAM has 5 documented accredited verifiers, all EU-based, for about 40,000 installations; India has 18 verification agencies, 15 provisional; Japan had certified 7 by June 2026; only 19 of 48 accredited carbon-credit auditors have African offices. That makes a verifier-ready evidence pack the most reusable product across regimes, and it is why agents should draft and trace, never decide.

**What to do next.** Over 90 days, run three tests in parallel:

- sign one paying South African pilot for the 2026 tax year;
- secure one Egyptian bank willing to pay for, or co-fund, an exporter-book pilot;
- complete one verifier dry run.

Run the authorised-credit test as interviews only. Stop it if fewer than 3 of 10 developers report a real cost.

## How to read this report

- **Evidence labels.** [P] means a primary legal text, regulator or registry. [D] means a data vendor or analyst. [S] means press or secondary summaries, often of paywalled material. [V] means a vendor claim. [I] means our own inference.
- **Scores.** These are my judgements and should be re-scored after each validation step.
- **Operating rule.** Every agent design follows the rule set in the CBAM report: agents propose, deterministic code calculates, and a named human approves into the `raw_ref` audit trail.

## 1. Compliance carbon: taxes, emissions trading systems (ETS) and border schemes

**What it is.** Governments put a price on industrial emissions through a tax, an ETS (where firms surrender allowances), or a border charge on imports (CBAM). Each regime requires monitoring plans, activity data, third-party verification and annual filings.

**Scope.** ICAP (the International Carbon Action Partnership) counts **41 ETSs covering 26% of global emissions**. Three national systems launched in 2026: Japan, India and Vietnam ([ICAP](https://icapcarbonaction.com/en/news/out-now-icap-status-report-2026-steady-course-turbulent-waters)) [P]. The World Bank puts carbon-pricing revenue at about **$107bn in 2025**. The global average price is about $21/t, and the Sub-Saharan African average is **$19/t** ([World Bank OKR](https://openknowledge.worldbank.org/entities/publication/64c7e4b9-bdd4-4761-9f3f-35fcccb4b7ef), via [Esgrovia](https://www.esgrovia.com/en/blog/world-bank-released-state-and-trends-of-carbon-pricing-2026/)) [P via S; not checked against the PDF].

| Regime | Who is covered, and key dates | Payer | Competition | Fit for carbonTraceAI |
|---|---|---|---|---|
| **South Africa carbon tax, Phase 2** | Phase 2 runs 2026–2030. Allowances: 60% basic (kept), offsets 15%/10%, trade exposure up to 10%, performance 5%. The carbon-budget allowance ended in 2025. A R640/t rate on emissions above budget waits for a Gazette date ([Webber Wentzel](https://www.webberwentzel.com/News/Pages/navigating-phase-two-of-carbon-tax-amendments-allowance-reform-and-offset-expansion.aspx)) [S, law-firm reading of the Budget Review and draft bill, flagged as the "most likely" position]. NGER (national GHG emission reporting) returns are due 31 Mar 2027; SAGERS, the online reporting system, was suspended for two cycles ([Netzero Compare](https://netzerocompare.com/policies/south-africa-nger)). The carbon-budget regulations are still a draft ([Cliffe Dekker Hofmeyr](https://www.cliffedekkerhofmeyr.com/en/news/publications/2025/Practice/Environmental-Law/environmental-law-alert-14-august-Draft-Carbon-Budget-and-Mitigation-Plan-Regulations-Published-as-South-Africa-takes-important-steps-to-advance-national-climate-change-policy)) | **The producer, in cash** | Breathe ESG is the only software vendor seen ([Breathe ESG](https://www.breatheesg.com/resources/esg-carbon-reporting-software-south-africa)) [V]; the rest is consultancies | **Highest** |
| EU CBAM | Verification of first actual data; the first declaration is due 30 Sep 2027 | Importer (cash), producer (data) | Importer-side tools; no producer-side tool for Africa (CBAM report) | Current product |
| UK CBAM | Starts 1 Jan 2027. One source says SI 2026/995 requires verified full-year 2027 actual data, with registration moved to 31 Jan 2028 and the first return to 31 May 2028 ([Impakter](https://impakter.com/uk-cbam-si-2026-995-verification-rules/)) [S, single source, not checked on legislation.gov.uk] | UK importer | Same as EU CBAM | A second output format on the same engine |
| Türkiye ETS pilot | 2026 is report-only. 2027 allowances are 100% free. Verified 2026 reports are due **30 Apr 2027**; first surrender is Nov 2028 ([ICAP](https://icapcarbonaction.com/en/news/turkiye-issues-implementation-rules-tr-ets-pilot-phase)) [P via ICAP] | Operator | Local vendors Sustrack and Karbonet | Later; little cash at stake in the pilot |
| India CCTS (carbon credit trading scheme) | About 490 entities, plus about 255 steel units in a draft. Form A filings were due 31 Jul 2026. **No certificate had traded by about 7 Oct 2026**, so the 2x-price penalty is still undefined ([crbn.credit](https://crbn.credit/post/india-carbon-credit-certificate-trading-october-2026); [Reclimatize](https://reclimatize.in/india-ccc-carbon-credit-market-iex-trading-price-formation/)) [S] | Obligated entity | Crowded: The Sustainability Cloud, Climes, Breathe, Oren; consultants at about Rs 2 lakh a year | Later, low price |
| China, Japan, Korea | China ~3,300–3,700 entities, monthly evidence, state platform with 270+ automated checks ([MEE](https://xcoss.henan.gov.cn/typtfile/20251009/1613827be7d04b2aaa0cfc06b84f458e.pdf)) [P]; Japan ~300–400 firms, mandatory since Apr 2026 ([GlobalDeal](https://globaldeal.io/blog/japans-gx-ets-the-meetings-changed)) [S]; Korea 813 | Operator | State platform; Asuene, Zeroboard | **Closed to this team** |
| Brazil, Vietnam, Chile/Colombia | Brazil Stage 1 monitoring plans 2027, draft ([Mondaq](https://www.mondaq.com/brazil/climate-change/1828326/extraordinary-secretariat-for-the-carbon-market-submits-to-public-consultation-a-draft-ordinance-on-the-timeline-for-the-implementation-of-the-mrv-obligations-under-the-sbce)); Vietnam 110 facilities; Chile tax ~$5/t | Operator | Local consultancies | Medium-term, outside Africa |

**What changed since the earlier reports.**

- **South Africa is stronger.** The earlier conflict over whether the basic allowance is cut from 60% to 50% resolves in favour of 60% kept to 2030. That position is a law firm's reading, not the final Act. The 15%/10% offset allowance gives the same customer a second paid job: choosing and proving offsets. The pending R640/t overshoot penalty would add a third: carbon-budget and mitigation-plan drafting, once the regulations are final.
- **EU CBAM is weaker as a cash story.** The 17 July 2026 EU ETS review proposal would slow the phase-out of free allocation for CBAM sectors to 2038 ([SteelOrbis](https://www.steelorbis.com/steel-news/latest-news/ec-proposes-extending-free-ets-allowances-for-cbam-sectors-until-2038-eurofer-raises-concerns-1465483.htm); [ICAP](https://icapcarbonaction.com/en/news/eu-commission-publishes-eu-ets-review-proposal)) [P via S; a proposal, not law]. On top of 2026 certificates covering about 2.5% of embedded emissions (CBAM report), the euro argument for EU CBAM stays thin into the 2030s. That favours regimes where the producer pays.
- **No other African country** has a compliance carbon price in force. Nigeria, Kenya, Ghana and Egypt are active only in Article 6 and voluntary markets ([Africa Sustainability Matters](https://africasustainabilitymatters.com/africas-carbon-markets-enter-a-new-phase-as-article-6-opens-path-to-climate-finance/)) [S]. In Africa, South Africa is the compliance market.

**What agents would do, and what stays deterministic.**

| Role | Tasks |
|---|---|
| Agents propose | Extract fuel, electricity and process inputs from bills and lab certificates. Map ERP items and processes to each regime's boundary (CBAM installation and CN codes; SA tax source categories; NGER templates). Draft the monitoring methodology, an allowance-claim memo and a cross-regime reconciliation memo explaining why the totals differ. Draft replies to verifier and regulator queries. |
| Code computes | Emissions under each regime's rules, allowances, the offset limit by emission type, the CBAM default-versus-actual comparison, the carbon-price-paid deduction, and every output file. |
| Humans sign | A plant engineer approves mappings, a tax practitioner signs the return, and a verifier issues the opinion. |

**Verdict.** Build the multi-regime MRV around South Africa now. Treat Türkiye and India as later configurations of the same engine. Ignore China, Japan and Korea as markets; use China's monthly-evidence approach only as a design reference.

## 2. Carbon credit markets: voluntary, CORSIA, Article 6, compliance offsets and removals

**What it is.** Projects earn credits for reducing or removing emissions. Buyers use them voluntarily, or under compliance rules: CORSIA for airlines, Article 6 deals between governments, or domestic offset allowances such as South Africa's.

**Scope and prices.**

- **Voluntary carbon market (VCM).** Primary value was about **$1.4bn in 2025, flat for a fourth year**. The average price was **$3.50/t** ([MSCI](https://www.msci.com/research-and-insights/blog-post/carbon-credits-come-of-age-in-2025)) [D]. REDD+ (forest-protection) credits fell to $1.90/t and non-CORSIA cookstove credits sit at $0.60–2.45/t ([CIX](https://static.climateimpactx.com/CIX%20Intelligence%20-%20Market%20Pulse%20H1%202026.pdf)) [D].
- **CORSIA.** Airlines must cancel roughly **146–236 Mt of eligible units by 31 Jan 2028**. Only about **38 Mt** were issued and labelled by Sept 2026, about **24% of them African** ([IATA at ICAO](https://www.icao.int/sites/default/files/NACC/MeetingDocs/2026/ENVSUSTF1/07%20Presentations%20-%20Presentaciones/ENVSUSWG01-P10.pdf); [CAPA](https://centreforaviation.com/news/iata-corsia-eeu-supply-growing-but-falling-well-short-of-units-needed-by-2028-1373032)) [P/S; the Africa share is our sum from IATA's table].
- **CORSIA price.** The CIX CORSIA benchmark still **halved** in H1 2026, from $19.10 to $9.40/t, before recovering to about $12.5–13 by July–August ([CIX](https://static.climateimpactx.com/CIX%20Intelligence%20-%20Market%20Pulse%20H1%202026.pdf); [Abatable](https://abatable.com/blog/a-summer-of-sourcing-corsia-what-four-airline-mandates-told-us-about-price-and-readiness)) [D].
- **Article 6 sovereign buyers** pay more: CHF 27–35/t through Switzerland's KliK, about S$35/t from Singapore, and $30/t through Norway's TCAF fund ([UNFCCC Baku deck](https://unfccc.int/sites/default/files/resource/Accelerating_A6.4_Engagement_BakuClimateWeek2026.pdf)) [P].
- **Durable carbon dioxide removal (CDR)** contracted 30.4 Mt in 2025, but Microsoft holds **78.5%** of contracted tonnes and was reported to have paused buying in April 2026 ([CDR.fyi](https://www.cdr.fyi/blog/durable-cdr-demand-structure-snapshot-april-2026); [Heatmap](https://heatmap.news/carbon-removal/microsoft-carbon-removal-pause)) [D/S].

**Where the money is.** The gating step for higher-value credits is paperwork, not carbon maths. It covers:

- the host country's Letter of Authorisation (LoA);
- the corresponding adjustment (CA), in which the host removes the tonnes from its own national target;
- registry labelling;
- buyer due diligence.

In four airline tenders in July–August 2026, **119 offers from 38 suppliers** chased about 29 times the qualified demand, and **about one in three lacked eligibility steps** ([Abatable](https://abatable.com/blog/a-summer-of-sourcing-corsia-what-four-airline-mandates-told-us-about-price-and-readiness)) [D]. The authorisation uplift is roughly **$7–12/t** (CORSIA generic versus non-CORSIA cookstove prices) [I]. The integrity rules add work. The ICVCM's Core Carbon Principles (CCP, the quality label) approved cookstove methodologies that covered **under 3%** of existing cookstove credits ([Climate Home](https://www.climatechangenews.com/2025/03/07/most-cookstove-carbon-credits-ruled-out-of-quality-scheme-in-push-for-high-integrity/)) [S]. Peer-reviewed work found cookstove over-crediting of about **9.2x**, against **1.5x** for metered methods ([Berkeley RAEL](https://rael.berkeley.edu/wp-content/uploads/2024/07/Gill-Wiehl-Kammen-Haya-Cooking-the-Books-Nature-Sustiainability-2024.pdf)) [P, peer-reviewed]. That favours conservative, metered, auditable calculation.

**Risks that cap it.** Sovereign risk is real: Kenya never issued KOKO Networks an LoA, and KOKO shut on 31 Jan 2026 with about 15m credits of uncertain status ([Sylvera](https://www.sylvera.com/blog/koko-networks-collapse-corsia-carbon-credits-loa)) [D]. The universe is small: about 91 approved African Article 6 activities ([UNEP-CCC](https://prod.article6.ecritportfolio.org/global-data/regions/un-classification/africa)) [P] suggest roughly **30–60 African developers and asset managers** [I]. The host-registry layer is donor-funded; Kenya's GIZ-backed registry feeds a free regional one ([GIZ](https://www.giz.de/en/newsroom/stories/national-carbon-registry-kenia-giz)) [P]. And registries are automating their own review: Verra's digital process cut a cookstove review from 163 to 63 days ([Verra](https://verra.org/documents/april-2026-stakeholder-update-webinar/)) [P], Isometric raised $40M for "agentic certification" ([Isometric](https://isometric.com/writing-articles/isometric-raises-40m-to-bring-agentic-certification-to-the-industrial-economy)) [V], and Pachama, a nature-MRV company, was sold after layoffs ([Trellis](https://trellis.net/article/pachama-layoffs-carbon-market/)) [S].

**Compliance offsets.** South Africa's offset allowance rose to 15% (combustion) and 10% (process and fugitive emissions) from 2026. Retirements against the tax hit a record in 2025 ([Fastmarkets](https://fastmarkets.com/insights/south-africa-to-increase-carbon-offset-allowances-for-carbon-tax-budget-2025); [Anthesis](https://www.anthesisgroup.com/za/insights/south-african-carbon-tax-update-2026/)) [S]. One note says the offsets must come from South African projects. **Verify this against the current Carbon Offsets Regulations.** Other regimes with offset links (Chile up to 100%, Colombia 50%, Vietnam 30%, Japan 10%, Singapore 5%) each have different eligibility rules, and none sits in carbonTraceAI's geography.

**What agents would do.**

- *Authorised-credit evidence agent.* It checks a project against CCP conditions (for example the fNRB non-renewable-biomass parameter and metering and usage-survey evidence). It drafts the monitoring report from device data, assembles the LoA dossier with mapping to national climate targets, tracks CA status for each vintage, and builds the buyer data room. Code computes the tonnes; the validation and verification body (VVB) and the registry decide.
- *SA offset agent.* It reads registry certificates and checks project location, vintage, methodology and double-claiming. Code computes the limit for each emission type and the tax saving; a tax practitioner signs.

**Verdicts.**

| Segment | Verdict |
|---|---|
| Generic VCM or nature MRV | **Avoid (confirmed)** |
| SA offset module | **Build** |
| Authorised-credit agent | **Time-boxed test as a module, not the company** |
| CDR MRV, host registries, Article 6.4 transition addenda (deadline 31 Dec 2026, mostly Asian), airline procurement | **Avoid** |
| Industrial Article 6 credits from African plants (nitrous oxide, landfill gas) | **Watch.** It would turn the same plant data into authorised units later |

## 3. Scope 3 supplier data, product carbon footprints (PCFs) and decarbonisation

**What it is.** Scope 3 means emissions in a company's value chain. Big buyers ask suppliers for corporate emissions and PCFs: cradle-to-gate footprints per product, increasingly in the WBCSD PACT data format or automotive Catena-X format. Decarbonisation tools aim to turn measurement into reduction projects.

**Scope.**

- **Request volume is large.** CDP requested data from **about 45,000 suppliers** for 270+ buyers in 2025 ([ESG Today](https://www.esgtoday.com/cdp-reports-70-jump-in-companies-receiving-top-sustainability-reporting-scores/)), while **10,900 SMEs** disclosed ([CDP](https://www.cdp.net/en/disclose/why-disclose)) [P]. This is not a true response rate, but it suggests that most requested suppliers answer poorly or not at all [I].
- **Some demand is enforced by procurement, not by law.** Catena-X requires ISO 14067 PCFs plus a data-quality rating from end-2027 ([Tanso](https://www.tanso.de/en/blog/what-is-catena-x-and-why-do-automotive-suppliers-need-to-act-now)) [V].
- **Regulation is lagging.** The EU Battery Regulation's carbon-footprint act was still not adopted as of late September 2026 ([Traceable](https://traceable.digital/resources/blog/battery-carbon-footprint-declaration-deadline-not-started/)) [S].
- **SBTi Net-Zero Standard v2.0** (published 11 June 2026; validation from 2027) adds a "supplier alignment" route for Scope 3 targets ([ESG Today](https://www.esgtoday.com/sbti-releases-finalized-new-corporate-net-zero-standard/)) [S]. It is voluntary.

**Who pays, and the competition.** Buyers pay for networks (CDP, EcoVadis). Suppliers increasingly get calculators **free**: EcoVadis offers one to a supplier base it puts at 150,000+ ([EcoVadis](https://ecovadis.com/solutions/pcf-calculator/)) [V]. Consolidation is fast. Makersite raised €60m ([Tech.eu](https://tech.eu/2025/07/22/makersite-raises-eur60m-to-boost-product-development-with-ai-lifecycle-tools/)) and bought Siemens' SiGREEN exchange ([ESG Today](https://www.esgtoday.com/makersite-acquires-product-carbon-footprint-platform-sigreen-from-siemens/)); EcoVadis pipes supplier data into CO2 AI and Workiva ([PR Newswire](https://www.prnewswire.com/news-releases/ecovadis-and-co2-ai-partner-to-advance-scope-3-transparency-with-primary-data-precision-302868501.html)); Gravity, SINAI and Normative already automate buyer-side chasing [V]. In construction, One Click LCA claims environmental product declaration (EPD) costs below one-tenth of traditional levels ([One Click LCA](https://oneclicklca.com/software/manufacturing/concrete-epd-generator)) [V], yet 49% of EPD cost is verification and publishing, which software cannot remove ([One Click LCA](https://oneclicklca.com/en/resources/articles/top-epd-software-overview)). On decarbonisation, PwC finds 60% of companies use AI for it but **fewer than 1% have quantified reductions** ([PwC](https://www.pwc.com/us/en/services/esg/library/decarbonization-strategic-plan.html)) [D]; no credible measure-to-verified-abatement agent was found.

**Emerging-market angle.** European buyers now expect African exporters to supply footprint-grade data, driven by CBAM and EUDR, the EU deforestation rule ([Capmad](https://www.capmad.com/post/cbam-and-eudr-why-european-buyers-now-demand-carbon-footprints-from-african-exporters)) [S]. A CBAM installation dataset holds most of the inputs for a cradle-to-gate PCF of the same product. So an "answer once" agent is a cheap extension. It would fill a PACT-format PCF, CDP and EcoVadis answers and buyer questionnaires from the plant ledger [I]. There is no evidence that African suppliers will pay for it. The practical model is buyer-sponsored or bundled.

**What agents would do.** Map incoming questionnaires to fields already in the store and draft answers. Match bills of materials to emission factors as top-k suggestions. Draft "beyond the request" refusal letters. Code computes the PCF and its allocation; the supplier approves every outbound answer. No agent ever sends anything unapproved.

**Verdicts.**

| Segment | Verdict |
|---|---|
| Supplier "answer once" PCF and questionnaire agent | **Module of #1**, for retention |
| Buyer-side Scope 3 chasing and SBTi supplier tracking | **Avoid** (incumbents; the data sits with suppliers) |
| EPD and battery PCF automation | **Avoid** (crowded, or the deadline slipped) |
| Decarbonisation advisor | **Later upsell**, tied to South Africa's mitigation plans once carbon budgets bite |

## 4. Carbon finance: banks, development finance institutions (DFIs) and trade finance

**What it is.** Banks measure "financed emissions" (emissions attributable to their loans) under the PCAF standard. They assess borrowers' transition risk, run sustainability-linked loans (SLLs), and increasingly price carbon into trade finance. DFIs such as IFC impose GHG rules on the projects they fund.

**Scope and drivers.**

- **Supervision is real.** The ECB fined ABANCA €187,650 and Crédit Agricole **€7.55m** over climate materiality-assessment failures ([ECB](https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/ssm.pr251110~3e0b6f579e.da.html); [ECB](https://www.bankingsupervision.europa.eu/press/pr/date/2026/html/ssm.pr260213~d0ac373293.ga.html)) [P]. The EBA's ESG-risk guidelines have applied to large banks since January 2026 [P]. Both fines punish *process* failures, not poor emissions data [I].
- **Disclosure has been loosened.** The EU dropped the GAR and BTAR green-asset-ratio templates ([Management Solutions](https://www.managementsolutions.com/index.php/en/node/4275)), the Basel climate framework became voluntary ([ESG Today](https://www.esgtoday.com/basel-committee-releases-voluntary-framework-for-banks-disclosure-of-climate-risks/)), the ISSB narrowed financed-emissions reporting in IFRS S2 ([EY](https://www.ey.com/en_gl/technical/ifrs-technical-resources/issb-issues-targeted-amendments-to-ifrs-s2)), and the Net-Zero Banking Alliance shut down ([Finextra](https://www.finextra.com/newsarticle/46713/net-zero-banking-alliance-shuts-down)).
- **PCAF is used widely, but on proxies.** It has 719 institutions ([PCAF](https://www.carbonaccountingfinancials.com/files/1775053892_Annual-Report-Final-v2.pdf)) [P], but most corporate books use sector averages. More than 80% of African banks do not disclose portfolio emissions ([Euromoney](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)) [S].
- **SLLs are shrinking.** Volumes fell about 18% in 2025 (other sources say 30–52% for some periods) ([Environmental Finance](https://www.environmental-finance.com/content/market-insight/sustainable-loans-face-a-reset-as-digital-infrastructure-and-transition-finance-take-hold.html)) [D]. Post-signing verification is now mandatory wherever it drives a margin ratchet ([LMA](https://lma.eu.com/application/files/6317/4298/0865/Sustainability-Linked_Loan_Principles_-_26_March_2025.pdf)) [P].
- **CBAM is reaching trade finance.** The ICC says CBAM is becoming a credit and liquidity issue for exporters ([ICC](https://library.iccwbo.org/content/tfb/news/dcwn_02February2026101213.htm)) [S]. Turk Eximbank raised a **€1bn CBAM-adjustment loan** with a World Bank guarantee ([GTR](https://www.gtreview.com/news/europe/turk-eximbank-gets-e1bn-loan-to-help-exporters-adjust-to-cbam/)) [S].

**The Egypt finding.** The CBE issued a 2025 directive that requires banks to:

- give the CBE a list of their exporting clients;
- help those clients meet EU and UK CBAM;
- assess CBAM impact on their portfolios, especially steel, aluminium, cement, fertiliser and hydrogen;
- file **semi-annual reports from H2 2026** ([Zawya](https://www.zawya.com/en/economy/north-africa/egypt-cbe-directs-banks-to-back-exporters-in-meeting-international-sustainability-standards-awo3hb2t); [Daily News Egypt](https://www.dailynewsegypt.com/2026/02/16/cbe-catalyses-banking-sectors-shift-toward-sustainable-finance-governor-abdalla/)) [S; **the circular text was not obtained**].

Separately, Egypt's FRA Decision 36/2026 requires larger non-bank financial institutions to report verified Scope 1–2 emissions and offset about 20% ([ESG News](https://esgnews.com/?p=42178)) [S].

A Climate TRACE-based tool already estimated financed emissions for over 80% of one Egyptian bank's corporate book ([Climate TRACE](https://climatetrace.org/news/how-a-leading-egyptian-bank-gained-visibility-into-its)) [V], which shows both that banks there buy tools and that asset-level proxies compete with borrower data.

**Who pays, and the competition.** Large banks spend about $250–500k a year on ESG technology ([IBS Intelligence/Chartis](https://ibsintelligence.com/?p=560199)) [D, 2024 survey]. That money goes to incumbents now shipping agents: S&P Sustainable1 launched four bank agents ([S&P](https://www.spglobal.com/sustainable1/en/insights/blogs/from-hype-impact-ai-agents-for-banks)) and Watershed Finance added agents ([Watershed](https://watershed.com/events/watershed-finance-demo-october)) [V]. The pattern for borrower data is that **the bank pays for the pipe and the borrower supplies data free**:

- NatWest gives SMEs Cogo's tool at no charge ([Finextra](https://www.finextra.com/pressarticle/99734/natwest-and-cogo-create-carbon-toolkit-for-smes)).
- NatWest, NAB and Standard Chartered co-invested in FourTwoThree, an SME data-sharing platform.
- Sage pitches its accounting-ledger API to banks for moving SME data up the PCAF quality scale ([Fintech Times](https://thefintechtimes.com/?p=117794)). That is carbonTraceAI's ERP thesis, run by an incumbent.

**No bank was found paying per borrower for verified data.** DFIs (for example IFC's 25 kt project threshold, per [E3G](https://www.e3g.org/bank-metrics/greenhouse-gas-accounting-at-project-and-portfolio-level/)) are better treated as co-funders through technical-assistance budgets and credit-line conditions than as SaaS buyers [I].

**Verdict change.** The opportunities report's "lender-paid data packs" (8/12) is **downgraded to 5/12 in its general form**: banks paying for verified borrower emissions to improve PCAF scores. It is **reframed and upgraded to 9/12 as CBE-driven CBAM-exposure screening**. Here the bank pays a modest platform fee to meet a dated regulatory report. Exporters are onboarded through ERP ingestion and get verified product-level actuals, which have their own euro value because they replace EU defaults. The resulting provenance packs double as PCAF score-2 data and SLL evidence. Expect pilots to be small (tens of thousands of dollars), often funded by technical assistance, with 12–18-month procurement [I].

**What agents would do.**

| Role | Tasks |
|---|---|
| Agents propose | Ingest the bank's exporter list and customs and HS (Harmonised System) codes. Propose CN-code and sector mappings. Draft the CBAM section of the semi-annual CBE report and client outreach letters. |
| Code computes | Exposure, using EU defaults times export volume until actuals exist and actuals once they do. |
| Humans approve | A bank sustainability officer approves the report; the borrower approves sharing its data. |

## 5. Verification and consulting intermediaries

**What it is.** Accredited verifiers (testing, inspection and certification (TIC) firms, VVBs, Big-4 assurers) issue opinions on emissions reports. Consultants prepare those reports for clients. The thesis tested here: sell agents to these intermediaries, in the way Basis sells to accountants and DataSnipper to auditors.

**Scope.**

- **EU CBAM.** About **40,000 installations** need verification ([DIHK](https://www.dihk.de/de/newsroom/dihk-impuls-cbam-anpassungen-dringend-noetig-182882)) [P, industry body]. On 13 Oct 2026 a tracker documented **5 accreditations, all EU-based**, while the Commission's official list showed none ([cbamguide](https://cbamguide.com/compliance/accredited-verifiers/)) [S]. The first verification year requires a physical site visit ([EUR-Lex 2025/2546](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2546)) [P].
- **Fees** are estimated at €3k–150k+ per installation ([cbamguide](https://cbamguide.com/importers/verification/)) [V/S]. About 25% of a quote is travel and site time (iFactory) [V].
- **The rough cycle-one pool is €100–500m a year** [I], most of it captured by TIC majors.
- **Elsewhere.** India's register shows 18 verification agencies (ACVAs), 15 provisional ([BEE](https://beeindia.gov.in/view_content.php?lid=568&lang=1)) [P]. Japan certified 7 verifiers by June 2026 ([QCI](https://www.qcintel.com/carbon/article/japan-certifies-seven-emission-auditors-for-gx-ets-67052.html)) [S]. More than 90% of African carbon-credit verification is done by international auditors, and developers blame 10–50% of delays and overruns on auditor bottlenecks ([VCMI/Perspectives/GIZ](https://vcmintegrity.org/wp-content/uploads/2026/02/Strengthening-VVB-Capacities-Report_February-2026-v4.pdf)) [P, commissioned study].

**Rules on AI.** A joint UKAS–DAkkS bulletin (from the UK and German accreditation bodies) says AI may not make the final conformity decision. Adopting AI counts as a significant change that must be reported to the national accreditation body (NAB) ([UKAS–DAkkS](https://www.ukas.com/wp-content/uploads/2026/03/UKAS49_U266-UKAS-Co-Branded-Ai-Bulletin-v2.pdf)) [P]. Impartiality rules bar a body from consulting and verifying the same claim. TÜV NORD requires a two-year gap between the two ([TÜV NORD](https://tuv-nord.com/vn/vi/tai-lieu/tinh-doc-lap-va-tinh-khach-quan)) [P, firm policy]. Agents can therefore trace, re-perform calculations, flag issues and draft. They cannot decide, sign or replace site visits.

**Who pays, and the competition.** Buyers are concentrated. About 8–10 TIC groups plus the Big-4 handle most compliance verification. Bureau Veritas is buying capability, such as Aligned Incentives ([ESG Today](https://www.esgtoday.com/bureau-veritas-acquires-aligned-incentives-to-bolster-scope-3-product-carbon-footprint-capabilities)). Isometric runs its AI review inside its own registry, with no published metrics ([Isometric](https://isometric.com/writing-articles/launching-ai-assisted-validation-in-certify)) [V]. No startup selling an AI copilot to GHG verifiers was found. That is white space, but also no proof anyone will pay.

The best analogue is weak on monetisation. DataSnipper is valued at $1B but earns roughly $44.5M across 400k+ users, about $100 per user per year ([DataSnipper](https://www.datasnipper.com/resources/datasnipper-raises-100m); [GetLatka](https://getlatka.com/companies/datasnipper)) [V/low-reliability D]. Carbon verifiers number in the thousands, not hundreds of thousands [I]. Consultants are a proven channel: Greenly Pro, Persefoni Pro and Gaia all run white-label programmes ([Persefoni](https://persefoni.com/pro-consultant-program)). But at about ₹2 lakh (~€2,000) per Indian SME client a year ([The Wire](https://thewire.in/environment/how-the-eus-carbon-border-tax-is-reshaping-indian-msmes)) [S], a consultant can spend only a few hundred euros per client on tools [I].

**Verdict.** A standalone "DataSnipper for carbon verifiers" scores 8/12: **don't build it as the company**. Instead, make the evidence layer two-sided:

- the producer, or the consultant acting for it, pays;
- the verifier gets a free or cheap read-only re-performance seat.

That matches the CBAM report's advice to design the audit view for verifiers rather than use them as a sales channel. One caution: if a verifier re-checks numbers with the same engine that produced them, that can look like self-review. Mitigate it with a separate tenant, an independent recalculation path and disclosure.

## 6. Scored comparison

Criteria (each 0–2): **C1** mandate with an enforced deadline; **C2** payer with a budget; **C3** data access; **C4** human-review tolerance; **C5** distribution; **C6** defensibility. A candidate is viable at **≥9/12 with no zero on C1 or C2**. **Fit** (0–4) measures reuse of the engine and provenance (0–2) plus the same customers and Africa channel (0–2). "Prior" refers to the opportunities report.

| # | Opportunity | C1 | C2 | C3 | C4 | C5 | C6 | /12 | Fit | Prior | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Multi-regime installation MRV, South Africa-led** (SA tax + NGER + EU/UK CBAM; later carbon budgets, Türkiye, India) | 2 | 2 | 2 | 2 | 1 | 1 | **10** | 4 | 10 | **Build now** |
| 2 | **SA carbon-tax offset-allowance module** | 2 | 2 | 1 | 2 | 1 | 1 | **9** | 4 | new | **Build inside #1** |
| 3 | **Egypt CBE CBAM-exposure screening for banks** (bank pays, exporters onboarded) | 2 | 1 | 1 | 2 | 2 | 1 | **9** | 3 | (8) | **Top channel test** |
| ref | Current product: EU CBAM only | 2 | 1 | 2 | 2 | 1 | 1 | 9 | 4 | 9 | Keep as one output format |
| 4 | Authorised-credit evidence agent (CORSIA/Article 6.2, African tech credits) | 2 | 1 | 1 | 2 | 1 | 1 | 8 | 3 | (6) | Time-boxed test, module |
| 5 | Verifier re-performance workspace (sold to verifiers) | 2 | 1 | 1 | 2 | 1 | 1 | 8 | 3 | new | Free seat inside #1 |
| 6 | Consultant white-label agent platform | 2 | 1 | 1 | 2 | 2 | 0 | 8 | 3 | new | A channel for #1, not an idea |
| 7 | Japan GX-ETS / EU ETS climate-neutrality-plan drafting | 2 | 2 | 2 | 2 | 0 | 0 | 8 | 1 | — | Good market, wrong team |
| 8 | Supplier "answer once" PCF/questionnaire agent | 1 | 1 | 2 | 2 | 1 | 0 | 7 | 3 | 7 | Module of #1 |
| 9 | Türkiye ETS module | 2 | 1 | 2 | 2 | 0 | 0 | 7 | 3 | — | Later configuration |
| 10 | India CCTS module | 2 | 1 | 2 | 2 | 0 | 0 | 7 | 3 | — | Later; price too low |
| 11 | "Measure to verified abatement" decarbonisation agent | 1 | 1 | 1 | 2 | 1 | 1 | 7 | 3 | 7 | Later upsell |
| 12 | Industrial Article 6 crediting (N2O, landfill gas) from African plants | 1 | 1 | 2 | 2 | 0 | 1 | 7 | 3 | — | Watch |
| 13 | SLL KPI verification packs | 1 | 1 | 2 | 2 | 0 | 1 | 7 | 3 | (8) | Feature |
| 14 | Brazil SBCE Stage 1 monitoring plans | 1 | 1 | 2 | 2 | 0 | 1 | 7 | 2 | — | Medium term |
| 15 | Bank financed emissions / paid borrower data (generic) | 0 | 1 | 1 | 2 | 1 | 0 | 5 | 2 | 8 | **Downgraded; avoid** |
| 16 | Buyer-side Scope 3 chasing / SBTi supplier tracking | 1 | 2 | 0 | 2 | 0 | 0 | 5 | 1 | — | Avoid |
| 17 | Durable CDR MRV | 0 | 1 | 1 | 2 | 0 | 0 | 4 | 1 | — | Avoid (Isometric; one buyer) |
| 18 | Generic VCM / nature project MRV and design-document drafting | 0 | 0 | 0 | 1 | 1 | 0 | 2 | 1 | (6) | **Avoid (confirmed)** |

**How to read the table.** Rows 2 and 3 are the only new rows that both score 9 and reuse the engine. Row 7 shows why the checklist alone is not enough: Japanese and EU installations are excellent markets for someone else, but fit and distribution rule them out for a small Africa-focused team. Row 4 misses on payer, because developers form a small, cash-variable universe. Row 6 scores zero on defensibility because several white-label programmes already exist; its value is as a channel.

**Where this round's evidence changed earlier verdicts.**

| Earlier verdict | New evidence | Updated verdict |
|---|---|---|
| Lender-paid data packs 8/12 | Disclosure rules loosened (no GAR/BTAR, IFRS S2 relief, voluntary Basel, NZBA closed); no per-borrower payments seen; incumbents ship bank agents; CBE CBAM directive found | Generic form 5/12; **Egypt CBE screening 9/12** |
| Project carbon MRV 6/12, "avoid" | Commodity VCM still at $3.50/t; CORSIA and sovereign units $10–35/t; a third of CORSIA offers fail eligibility | Split: generic **2/12**; authorised-credit agent **8/12**; SA offset module **9/12** |
| SA basic allowance: 60% or 50%? | Phase 2 keeps 60% to 2030; offsets raised to 15%/10%; R640/t overshoot pending | Rank 1 strengthened |
| Zero CBAM verifiers (July 2026) | 5 documented by mid-Oct, all EU-based; India 18 mostly provisional; Japan 7; Africa >90% foreign auditors | The verifier-ready pack becomes the cross-regime product |
| EU CBAM money ramps to 2034 | Proposal to extend free allocation to 2038 | Lean on producer-paid regimes for revenue |

## 7. Recommended new idea and product shape

**Pitch (two sentences).** *carbonTraceAI turns one plant's ERP, meter and invoice data into verifier-ready filings for every carbon regime that plant faces: South Africa's carbon tax and offset allowance, national GHG reporting, and EU and UK CBAM. It also produces the CBAM-exposure reports banks now owe their regulators. AI agents do the paperwork, deterministic code does every calculation, and a named engineer, tax practitioner or verifier signs each output.*

Short form: **the carbon evidence layer for emerging-market heavy industry.** Lead with "deterministic and verifier-ready". Do not make "agentic" the headline (CBAM report).

**What actually changes from today's idea.**

| Dimension | Today (`docs/IDEA.md`) | New |
|---|---|---|
| Lead buyer | African CBAM exporter, whose EU importer is liable | South African carbon-tax payer, who is itself liable; Egyptian banks as a channel |
| Unit sold | CBAM XML per facility | **Installation-year evidence ledger**, with one output format per regime |
| Agent role | Not specified | Six bounded proposal agents behind an approval queue |
| Moat | Shared directory (the free O3CI portal undercuts it) | Cross-regime reconciliation, versioned rule libraries, verifier acceptance, `raw_ref` provenance |
| First sale | Self-serve subscription | Verification-readiness engagement for the 2026 data year |

**Product components.**

1. **Ledger.** The existing canonical store plus an installation-year state machine: data complete → calculations frozen → verifier linked → pack ready → verified → filed or shared.
2. **Regime outputs (deterministic).**
   - SA carbon tax: allowance schedule and offset limit.
   - NGER/SAGERS templates.
   - EU CBAM: O3CI record, communication template and monitoring methodology.
   - UK CBAM: 2027 actuals.
   - CBE bank exposure report.
   - Later: carbon budgets and mitigation plans, Türkiye, and the PACT PCF format.
3. **Approval queue** in the Next.js dashboard. It shows the diff, evidence links, confidence and approver role, as specified in the CBAM report.
4. **Verifier seat.** Read-only access with click-through to source documents and an independent recalculation path.

**Agent roles.**

| Agent | Proposes | Deterministic check | Human approver | Never does |
|---|---|---|---|---|
| Document intake | Activity data from bills, fuel invoices, lab certificates, multilingual scans | Unit and range validators; mass and energy reconciliation | Plant data owner | Fill gaps by guessing |
| Boundary mapper | Mapping of ERP items to CBAM CN codes, SA tax source categories and NGER categories (top-k with rationale) | Closed label lists; versioned mapping reused deterministically | Plant engineer | Choose emission factors or tiers |
| Filing-pack drafter | Monitoring methodology, allowance memo, cross-regime reconciliation memo, verifier evidence pack | Numbers inserted only as template variables from the store | Tax practitioner or compliance lead | Put a computed number in prose |
| Offset eligibility | Eligibility findings from registry certificates and project documents (location, vintage, methodology, double-claiming) | Offset limit and saving computed by rule tables | Tax practitioner | Buy or retire credits |
| Query responder | Replies to verifier findings and regulator queries, with evidence links | Every cited figure resolved from the ledger | Named compliance lead | Send without approval |
| Bank screener (Egypt) | Mapping of exporter list to CBAM sectors; draft CBE report section; client invitations | Exposure maths (defaults, then actuals) | Bank sustainability officer | Contact borrowers unapproved |

A seventh, internal **regulation watcher** compares official gazettes and EUR-Lex deterministically and summarises changes with verbatim citations for the team. All agents follow the CBAM report's controls:

- a `candidates` table;
- extended `raw_ref` (document hash, page, model version, approver);
- abstention below a confidence threshold;
- AI-assisted fields disclosed to the verifier;
- a hard deny-list: no submitting, no trading, no unapproved sends.

**Pricing hypotheses (all unvalidated).**

- A base fee per installation-year, anchored at the earlier €6k/facility/year (€499/month).
- Per-regime output fees.
- A per-return fee for the offset module.
- A bank platform fee plus a fee per screened exporter.

The realistic outcome is a capital-efficient niche business, not a venture-scale category. The opportunities report found SME carbon tools earn about €7.5k per customer per year.

## 8. 90-day validation plan (22 Oct 2026 – 20 Jan 2027)

The calendar drives the sequence:

| Date | Deadline |
|---|---|
| H2 2026 | CBE semi-annual reports begin |
| 31 Mar 2027 | NGER returns |
| 30 Apr 2027 | Türkiye verified reports |
| Jul 2027 | SA carbon-tax returns (first year of new offset limits) |
| 30 Sep 2027 | EU CBAM declaration |
| 31 Jan 2028 | CORSIA cancellation |

| Track | Weeks | Action | Pass | Kill or re-rank |
|---|---|---|---|---|
| A. SA producers (core) | 1–8 | 15 discovery calls with SA carbon-tax payers in steel, ferroalloys, cement, fertiliser and downstream aluminium that also export to the EU or UK. Ask who prepares the carbon-tax return, NGER submission and offset selection, at what cost, and how they reconcile these with CBAM data | ≥3 pay outside help for two or more of these filings and would consolidate at ≥€6k per installation-year; **1 signed paid pilot or LOI by day 90** | Most handle these in-house or within a bundled Big-4 engagement |
| A2. Pilot run | 6–12 | Run one plant's data through SA tax, NGER and CBAM outputs; produce the reconciliation memo and offset-limit calculation | Differences are explainable and the pack assembles without bespoke consulting | Boundaries need custom expert work for every plant |
| B. Egypt banks | 1–10 | Get the CBE circular text; meet 5 bank sustainability units and 1 DFI technical-assistance programme (for example IFC's work with Banque Misr) | 1 bank agrees to a paid or DFI co-funded exporter-book pilot | Banks are satisfied with default-times-volume spreadsheets, or no budget owner exists |
| C. Verifier dry run | 4–12 | One accredited CBAM verifier, a SANAS-accredited (South African) GHG verifier or an Indian ACVA reviews a sample pack and audit view | Verifier states a time saving and accepts the disclosed AI fields | Verifier treats AI-assisted fields as an inherent-risk flag |
| D. Authorised credits | 2–10 | 10 interviews with African authorised-unit developers and asset managers, plus Abatable as a possible channel | ≥3 of 10 report ≥$50k/yr in eligibility and evidence cost, or ≥3-month sale delays | Fewer than 3; CORSIA generic stays below $10; Abatable or a ratings firm launches an equivalent; LoA issuance stalls in more than one host (kill criteria from the credit-market note) |
| E. Agent evaluation | 3–12 | Build a labelled set of 200–500 pilot documents | Extraction beats the pdfplumber + Tesseract + rules baseline on accuracy and review time | It does not ship |
| F. Fact checks | 1–4 | SA offset location rule; R640 effective date; carbon-budget regulations; number of SA taxpayers; UK CBAM SI dates on legislation.gov.uk | Facts confirm the timeline | A major date slips (the case survives on carbon tax alone) |

**Overall decision at day 90.**

- **A passes:** commit to the new positioning.
- **A fails but B passes:** lead with the bank channel.
- **A and B both fail:** the problem is the payer, not the idea. Either sell the engine to consultants and verifiers as a tool, or consider whether the team should pursue the business at all.

**Team bandwidth.** Tracks A and C are mandatory. B and D are interview-led and should take no more than a quarter of founder time.

## 9. Risks

- **Regulatory slippage.** SA carbon-budget regulations are a draft and the R640 date is unset; UK CBAM dates rest on one source; the 2038 extension, if adopted, delays CBAM costs further. Mitigation: lead with the carbon tax, which is in force.
- **Payer still unproven.** No willingness-to-pay data exists for any regime in Africa, and SA taxpayer counts were not found, so the market is unsized.
- **Competition.** Breathe ESG markets SA tooling; Anthesis and the Big-4 serve SA emitters; Sage and incumbent bank platforms pursue the ERP-to-bank pipe; verifiers sell "pre-verification" (CBAM report).
- **Verifier acceptance and self-review.** No NAB decision on any AI verification tool was found; disclosed AI fields could increase sampling. Verifiers using the engine that produced the numbers could look like self-review.
- **Data sovereignty.** Producers and banks may refuse external LLM APIs, forcing redaction or self-hosting.
- **One-off spikes.** The first CBAM verification crunch (Q4 2026 to Sep 2027) and the CORSIA Phase 1 deadline are peaks; the recurring base is the annual tax, NGER and CBAM cycles. The credit module also carries sovereign risk (KOKO).
- **Agent failure modes.** Gartner expects over 40% of agentic projects to be cancelled by 2027, and Trellis documented an agent reproducing greenwashing language (opportunities report). Keep agents narrow and evaluated.
- **Credibility.** Replace the Mozal demo profile; Mozal has been on care and maintenance since March 2026 (CBAM report).

## 10. Evidence quality, conflicts and gaps

**Strongest evidence.** Primary texts and regulators: ICAP, the ECB press releases, the UNFCCC Baku deck, the BEE register, LMA principles, UKAS–DAkkS, EUR-Lex and CDP. Law-firm readings: Webber Wentzel on SA Phase 2, Cliffe Dekker. Data vendors: CIX, MSCI, CDR.fyi, Abatable. **Weakest evidence.** Agent performance, competitor capability and nearly all fee figures are vendor claims. No price for any agent product was found.

**Conflicts.**

| Item | Conflict | How handled |
|---|---|---|
| India ACVAs | 18 on the BEE register (Oct 2026) vs 1–2 in a search snippet and 2 in March 2026 | Register preferred |
| Covered entities | India ~490 vs ~740; Japan ~300–400 vs ~600 | Lower figures used |
| CBAM verifiers | 0 on the official list vs 5 documented by a tracker | Both stated |
| CORSIA price | CIX $9.40 (June) vs UNFCCC $11.6 June low and $19 Aug futures; World Bank and Malaysian $15–25 figures are stale | CIX/Abatable used for spot |
| CORSIA supply | "4–6x shortage" vs 29x tender oversubscription | Likely deferred buying plus ineligible offers |
| SLL decline; 2025 retirements | −18% to −52%; retirements up or down by counter | Ranges stated |
| Other | UK "Global ACI" vs "IAF" accreditation wording (probably consistent); Kenya's two bank-disclosure start dates | Flagged |

**Gaps that could change the ranking.** The number of SA carbon-tax payers; whether SA offsets must be domestic; the CBE circular text and its data fields; contract values at emerging-market banks; verifier willingness to pay and verification hours by task; PCF, EPD and supplier-tool prices; any survey of African supplier data capability; hours per compliance task; Türkiye and Brazil entity counts. Water, adaptation, physical-risk and nature domains remain unresearched (opportunities report).

## Sources

**Compliance regimes.**
[ICAP Status Report 2026](https://icapcarbonaction.com/en/news/out-now-icap-status-report-2026-steady-course-turbulent-waters) ·
[World Bank State & Trends 2026](https://openknowledge.worldbank.org/entities/publication/64c7e4b9-bdd4-4761-9f3f-35fcccb4b7ef) ·
[ICAP India CCTS](https://icapcarbonaction.com/en/news/compliance-obligations-under-indias-carbon-credit-trading-scheme-enter-force-seven-sectors) ·
[crbn.credit India](https://crbn.credit/post/india-carbon-credit-certificate-trading-october-2026) ·
[Reclimatize](https://reclimatize.in/india-ccc-carbon-credit-market-iex-trading-price-formation/) ·
[BEE ACVA list](https://beeindia.gov.in/view_content.php?lid=568&lang=1) ·
[ICAP China](https://icapcarbonaction.com/en/news/china-officially-expands-national-ets-cement-steel-and-aluminum-sectors) ·
[GlobalDeal Japan](https://globaldeal.io/blog/japans-gx-ets-the-meetings-changed) ·
[QCI Japan verifiers](https://www.qcintel.com/carbon/article/japan-certifies-seven-emission-auditors-for-gx-ets-67052.html) ·
[ICAP Korea](https://icapcarbonaction.com/en/ets/korea-emissions-trading-system-k-ets) ·
[Mondaq Brazil](https://www.mondaq.com/brazil/climate-change/1828326/extraordinary-secretariat-for-the-carbon-market-submits-to-public-consultation-a-draft-ordinance-on-the-timeline-for-the-implementation-of-the-mrv-obligations-under-the-sbce) ·
[Webber Wentzel SA Phase 2](https://www.webberwentzel.com/News/Pages/navigating-phase-two-of-carbon-tax-amendments-allowance-reform-and-offset-expansion.aspx) ·
[Cliffe Dekker carbon budgets](https://www.cliffedekkerhofmeyr.com/en/news/publications/2025/Practice/Environmental-Law/environmental-law-alert-14-august-Draft-Carbon-Budget-and-Mitigation-Plan-Regulations-Published-as-South-Africa-takes-important-steps-to-advance-national-climate-change-policy) ·
[Netzero Compare NGER](https://netzerocompare.com/policies/south-africa-nger) ·
[Breathe ESG SA](https://www.breatheesg.com/resources/esg-carbon-reporting-software-south-africa) ·
[ICAP Türkiye pilot](https://icapcarbonaction.com/en/news/turkiye-issues-implementation-rules-tr-ets-pilot-phase) ·
[Impakter UK CBAM SI](https://impakter.com/uk-cbam-si-2026-995-verification-rules/) ·
[ICAP EU ETS review](https://icapcarbonaction.com/en/news/eu-commission-publishes-eu-ets-review-proposal) ·
[SteelOrbis 2038](https://www.steelorbis.com/steel-news/latest-news/ec-proposes-extending-free-ets-allowances-for-cbam-sectors-until-2038-eurofer-raises-concerns-1465483.htm) ·
[Africa Sustainability Matters, Article 6](https://africasustainabilitymatters.com/africas-carbon-markets-enter-a-new-phase-as-article-6-opens-path-to-climate-finance/)

**Carbon credits.**
[MSCI](https://www.msci.com/research-and-insights/blog-post/carbon-credits-come-of-age-in-2025) ·
[CIX Market Pulse H1 2026](https://static.climateimpactx.com/CIX%20Intelligence%20-%20Market%20Pulse%20H1%202026.pdf) ·
[IATA at ICAO](https://www.icao.int/sites/default/files/NACC/MeetingDocs/2026/ENVSUSTF1/07%20Presentations%20-%20Presentaciones/ENVSUSWG01-P10.pdf) ·
[CAPA](https://centreforaviation.com/news/iata-corsia-eeu-supply-growing-but-falling-well-short-of-units-needed-by-2028-1373032) ·
[Abatable](https://abatable.com/blog/a-summer-of-sourcing-corsia-what-four-airline-mandates-told-us-about-price-and-readiness) ·
[UNFCCC Baku deck](https://unfccc.int/sites/default/files/resource/Accelerating_A6.4_Engagement_BakuClimateWeek2026.pdf) ·
[Sylvera on KOKO](https://www.sylvera.com/blog/koko-networks-collapse-corsia-carbon-credits-loa) ·
[UNEP-CCC Africa pipeline](https://prod.article6.ecritportfolio.org/global-data/regions/un-classification/africa) ·
[GIZ Kenya registry](https://www.giz.de/en/newsroom/stories/national-carbon-registry-kenia-giz) ·
[Climate Home cookstoves](https://www.climatechangenews.com/2025/03/07/most-cookstove-carbon-credits-ruled-out-of-quality-scheme-in-push-for-high-integrity/) ·
[Gill-Wiehl et al.](https://rael.berkeley.edu/wp-content/uploads/2024/07/Gill-Wiehl-Kammen-Haya-Cooking-the-Books-Nature-Sustiainability-2024.pdf) ·
[Verra April 2026 webinar](https://verra.org/documents/april-2026-stakeholder-update-webinar/) ·
[VCMI VVB capacity report](https://vcmintegrity.org/wp-content/uploads/2026/02/Strengthening-VVB-Capacities-Report_February-2026-v4.pdf) ·
[Fastmarkets SA offsets](https://fastmarkets.com/insights/south-africa-to-increase-carbon-offset-allowances-for-carbon-tax-budget-2025) ·
[Anthesis SA 2026](https://www.anthesisgroup.com/za/insights/south-african-carbon-tax-update-2026/) ·
[CDR.fyi](https://www.cdr.fyi/blog/durable-cdr-demand-structure-snapshot-april-2026) ·
[Heatmap](https://heatmap.news/carbon-removal/microsoft-carbon-removal-pause) ·
[Isometric Series A](https://isometric.com/writing-articles/isometric-raises-40m-to-bring-agentic-certification-to-the-industrial-economy) ·
[Trellis on Pachama](https://trellis.net/article/pachama-layoffs-carbon-market/)

**Scope 3, PCFs and decarbonisation.**
[ESG Today CDP](https://www.esgtoday.com/cdp-reports-70-jump-in-companies-receiving-top-sustainability-reporting-scores/) ·
[CDP](https://www.cdp.net/en/disclose/why-disclose) ·
[EcoVadis PCF Calculator](https://ecovadis.com/solutions/pcf-calculator/) ·
[EcoVadis–CO2 AI](https://www.prnewswire.com/news-releases/ecovadis-and-co2-ai-partner-to-advance-scope-3-transparency-with-primary-data-precision-302868501.html) ·
[Makersite/SiGREEN](https://www.esgtoday.com/makersite-acquires-product-carbon-footprint-platform-sigreen-from-siemens/) ·
[Tech.eu Makersite](https://tech.eu/2025/07/22/makersite-raises-eur60m-to-boost-product-development-with-ai-lifecycle-tools/) ·
[Tanso Catena-X](https://www.tanso.de/en/blog/what-is-catena-x-and-why-do-automotive-suppliers-need-to-act-now) ·
[Traceable battery act](https://traceable.digital/resources/blog/battery-carbon-footprint-declaration-deadline-not-started/) ·
[One Click LCA generator](https://oneclicklca.com/software/manufacturing/concrete-epd-generator) ·
[One Click LCA cost split](https://oneclicklca.com/en/resources/articles/top-epd-software-overview) ·
[PwC decarbonisation](https://www.pwc.com/us/en/services/esg/library/decarbonization-strategic-plan.html) ·
[ESG Today SBTi v2](https://www.esgtoday.com/sbti-releases-finalized-new-corporate-net-zero-standard/) ·
[Capmad](https://www.capmad.com/post/cbam-and-eudr-why-european-buyers-now-demand-carbon-footprints-from-african-exporters)

**Carbon finance.**
[ECB ABANCA](https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/ssm.pr251110~3e0b6f579e.da.html) ·
[ECB Crédit Agricole](https://www.bankingsupervision.europa.eu/press/pr/date/2026/html/ssm.pr260213~d0ac373293.ga.html) ·
[Management Solutions Pillar 3](https://www.managementsolutions.com/index.php/en/node/4275) ·
[ESG Today Basel](https://www.esgtoday.com/basel-committee-releases-voluntary-framework-for-banks-disclosure-of-climate-risks/) ·
[EY IFRS S2](https://www.ey.com/en_gl/technical/ifrs-technical-resources/issb-issues-targeted-amendments-to-ifrs-s2) ·
[Finextra NZBA](https://www.finextra.com/newsarticle/46713/net-zero-banking-alliance-shuts-down) ·
[PCAF 2025 report](https://www.carbonaccountingfinancials.com/files/1775053892_Annual-Report-Final-v2.pdf) ·
[Euromoney African banks](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/) ·
[Zawya CBE directive](https://www.zawya.com/en/economy/north-africa/egypt-cbe-directs-banks-to-back-exporters-in-meeting-international-sustainability-standards-awo3hb2t) ·
[Daily News Egypt](https://www.dailynewsegypt.com/2026/02/16/cbe-catalyses-banking-sectors-shift-toward-sustainable-finance-governor-abdalla/) ·
[ESG News FRA 36/2026](https://esgnews.com/?p=42178) ·
[Climate TRACE Egypt](https://climatetrace.org/news/how-a-leading-egyptian-bank-gained-visibility-into-its) ·
[Finextra Cogo](https://www.finextra.com/pressarticle/99734/natwest-and-cogo-create-carbon-toolkit-for-smes) ·
[Fintech Times Sage](https://thefintechtimes.com/?p=117794) ·
[S&P agents](https://www.spglobal.com/sustainable1/en/insights/blogs/from-hype-impact-ai-agents-for-banks) ·
[Watershed Finance](https://watershed.com/events/watershed-finance-demo-october) ·
[Environmental Finance SLLs](https://www.environmental-finance.com/content/market-insight/sustainable-loans-face-a-reset-as-digital-infrastructure-and-transition-finance-take-hold.html) ·
[LMA SLL Principles](https://lma.eu.com/application/files/6317/4298/0865/Sustainability-Linked_Loan_Principles_-_26_March_2025.pdf) ·
[ICC](https://library.iccwbo.org/content/tfb/news/dcwn_02February2026101213.htm) ·
[GTR Turk Eximbank](https://www.gtreview.com/news/europe/turk-eximbank-gets-e1bn-loan-to-help-exporters-adjust-to-cbam/) ·
[IBS Intelligence/Chartis](https://ibsintelligence.com/?p=560199) ·
[E3G IFC PS3](https://www.e3g.org/bank-metrics/greenhouse-gas-accounting-at-project-and-portfolio-level/)

**Verification and intermediaries.**
[DIHK](https://www.dihk.de/de/newsroom/dihk-impuls-cbam-anpassungen-dringend-noetig-182882) ·
[cbamguide verifiers](https://cbamguide.com/compliance/accredited-verifiers/) ·
[cbamguide fees](https://cbamguide.com/importers/verification/) ·
[EUR-Lex 2025/2546](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2546) ·
[UKAS–DAkkS AI bulletin](https://www.ukas.com/wp-content/uploads/2026/03/UKAS49_U266-UKAS-Co-Branded-Ai-Bulletin-v2.pdf) ·
[TÜV NORD impartiality](https://tuv-nord.com/vn/vi/tai-lieu/tinh-doc-lap-va-tinh-khach-quan) ·
[Isometric Certify](https://isometric.com/writing-articles/launching-ai-assisted-validation-in-certify) ·
[ESG Today BV](https://www.esgtoday.com/bureau-veritas-acquires-aligned-incentives-to-bolster-scope-3-product-carbon-footprint-capabilities) ·
[DataSnipper](https://www.datasnipper.com/resources/datasnipper-raises-100m) ·
[GetLatka](https://getlatka.com/companies/datasnipper) ·
[Persefoni Pro](https://persefoni.com/pro-consultant-program) ·
[The Wire](https://thewire.in/environment/how-the-eus-carbon-border-tax-is-reshaping-indian-msmes)

**Internal.** `reports/CBAM agentic workflow market research.md`; `reports/Agentic AI sustainability opportunities.md`; `docs/IDEA.md`; `research_notes/Carbon agentic AI opportunity scope/*.md`.
