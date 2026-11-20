# Agentic AI for Operational (Non-Reporting) Sustainability Problems: Operations, Physical Systems and Markets (2024-2026)

Scope note: These notes cover operations, physical systems and markets. Compliance reporting (CSRD, CBAM, ISSB and similar) is out of scope. Research was done in October 2026. Nearly all quantitative "results" below are vendor-reported, and I flag that each time. Independent or peer-reviewed validation of agentic systems was rare in every domain. "Agentic" is also used loosely: many products sold as agents are ML optimisers or copilots with a human approving each action. I note the distinction where the sources allow.

---

## 1. Industrial energy efficiency and decarbonisation: factory energy management, HVAC/compressed air/steam optimisation, autonomous building control

### Takeaway
This is the most mature operational domain. Closed-loop AI control of HVAC, chillers and process setpoints is in production at thousands of sites. Vendors claim 10-30% energy savings, but nearly all of that evidence is self-reported. The new LLM "industrial copilots" from Siemens and Schneider are mostly engineering assistants (code generation, troubleshooting), not autonomous energy optimisers, and I found no published energy-savings figures attributable to them.

### Cited Findings
**Phaidra (autonomous control agents for industrial cooling, data centres and pharma)**
- Phaidra claims 10-30% energy-efficiency improvements in live deployments and says utility savings pay back the subscription within months. These are vendor claims relayed by an aggregator. — [Sacra](https://sacra.com/c/phaidra/)
- Named deployments: data-centre operator STT GDC (Singapore) and pharmaceutical manufacturing at Merck. — [Sacra](https://sacra.com/c/phaidra/)
- For NVIDIA's DSX/Omniverse AI-factory blueprint, Phaidra claims thermal control within 0.5°C, which it describes as an 80%+ reduction in the size of thermal spikes, plus "significant PUE improvements" from cutting chiller-plant energy. — [Phaidra blog](https://www.phaidra.ai/blog/phaidra-nvidia-ai-agents-for-gigawatt-scale-ai-factories)
- Pedigree: the founder led the DeepMind/Google project that cut data-centre cooling energy by about 40% in an already-optimised facility. This predates 2024. — [Sacra](https://sacra.com/c/phaidra/)
- Raised a $50M+ Series B in October 2025, led by Collaborative Fund with NVIDIA participating. Also launched "Phaidra Prism", an AI assistant for troubleshooting AI-factory operations. — [The AI Insider](https://theaiinsider.tech/2025/10/13/collaborative-fund-leads-phaidras-50m-series-b-to-build-the-ai-factories-of-the-future/); [Phaidra blog](https://www.phaidra.ai/blog)
- Phaidra also markets a manufacturing product, "Phaidra Factory". — [Phaidra Factory](https://www.phaidra.ai/products/phaidra-factory)

**BrainBox AI / Trane (autonomous HVAC control plus the ARIA generative-AI "virtual building engineer")**
- Trane completed its acquisition of BrainBox AI, first announced on 18 December 2024. — [Trane press release](https://www.trane.com/commercial/asia-pacific/my/en/about-us/press-releases/Trane-Technologies-Completes-Acquisition-of-BrainBox-AI.html); [Facilities Dive](https://www.facilitiesdive.com/news/trane-technologies-agrees-to-acquire-brainbox-ai/736155/)
- Headline claims: energy reductions of "up to 25%" and GHG reductions of "up to 40%". These are maximums, not typical results. — [Sustainable Business News](https://sustainablebiz.ca/trane-to-acquire-montreals-brainbox-ai)
- Toronto pilot (around 2021): 25% and 29% energy savings in two GWL Realty Advisors buildings. Small sample, and I found no published methodology. — [Sustainable Business News](https://sustainablebiz.ca/trane-to-acquire-montreals-brainbox-ai)
- Claimed scale: more than 14,000 commercial buildings. — [Cooling Post](https://coolingpost.com/world-news/trane-technologies-buys-ai-pioneer)
- Analyst-reported (Memoori, based on company data): Dollar Tree went from 616 pilot sites to about 3,000 stores, with more than $1M in savings and payback under 12 months. An Amazon grocery pilot reportedly cut energy use by about 15%, more than double its target. — [Memoori](https://memoori.com/trane-technologies-ai-strategy-smart-buildings/)
- ARIA is a generative-AI building-management assistant. It combines data from HVAC, lighting, weather forecasts, energy bills and utility tariffs. — [HVACR Trends](https://hvacrtrends.com/trane-and-brainbox-ai-join-forces/?amp=1)

**Fero Labs (explainable ML for process/recipe optimisation in steel and chemicals)**
- Gerdau case study (secondary source): alloy costs cut by $3 per tonne of steel, "millions of pounds" of ferroalloys saved each year, and quality variation reduced by 15%. — [AI Expert Network](https://aiexpert.network/ai-at-gerdau/)
- Spanish-language press relaying company claims: up to 34% less use of mined alloying ingredients, and about 450,000 tCO2 per year avoided, mostly upstream from avoided alloy extraction, smelting and transport. The article's figure of 11.9 Mt/year for all US steel is an extrapolation, not a result. — [Río Negro](https://www.rionegro.com.ar/sociedad/una-startup-usa-la-inteligencia-artificial-para-reducir-las-emisiones-de-carbono-en-el-procesamiento-del-acero-3261359/?amp=1)
- Context: Gerdau's target is 0.83 tCO2e per tonne of steel by 2031, against 0.93 in 2020 (scopes 1-2). — [Suno](https://www.suno.com.br/noticias/?p=227664)

**Schneider Electric and Siemens (LLM copilots)**
- Schneider launched an industrial gen-AI copilot with Microsoft in mid-2025. It runs on Azure AI Foundry inside EcoStruxure Automation Expert, and it generates and checks automation code and helps with troubleshooting and predictive maintenance. The sources frame it as an assistant, not an autonomous agent. — [Hydrocarbon Processing](https://hydrocarbonprocessing.com/news/2025/05/schneider-electric-unveils-industrial-gen-ai-copilot-in-collaboration-with-microsoft/); [ARC Advisory](https://www.arcweb.com/node/159941)
- Schneider customer case for "EcoStruxure Autonomous Production Advisor" (a pre-LLM AI production tool): 34% lower energy use and 13% more production. Vendor figure. — [Schneider Electric ZA](https://www.se.com/za/en/work/solutions/artificial-intelligence/solutions/)
- Siemens has said it envisions industrial AI agents that work alongside humans and handle routine processes on their own. I found no deployment metrics. — [Process Excellence Network](https://www.processexcellencenetwork.com/ai/news/siemens-unveils-ai-agents-for-industrial-automation/amp)

**Macro framing**
- The IEA's *Energy and AI* special report (16 April 2025) models AI's own electricity demand. It names demand-side flexibility and predictive maintenance as ways AI could change how the energy sector operates. I found no Africa-specific figure for AI-driven industrial savings. — [IEA](https://www.iea.org/reports/energy-and-ai); [ManagEnergy](https://managenergy.ec.europa.eu/publications/energy-ai-nexus-iea-report-explores-ais-growing-power-demand-and-energy-potential_en)

### Inferences
- The well-funded leaders (Phaidra, BrainBox/Trane) are moving towards hyperscale data centres and large retail chains. Phaidra's NVIDIA tie-up and Series B framing are AI-factory-centric. That pulls them away from mid-size, brownfield manufacturers in emerging markets.
- The real limit is physical control and integration, not intelligence. Closed-loop control needs a BMS/SCADA layer, reliable sub-metering and an owner willing to delegate setpoints. Many African factories (cement, steel rerolling, textiles, food processing) lack sub-metering and run on unreliable grid power with diesel backup. The first value there is probably advisory: anomaly detection, tariff and diesel-versus-grid scheduling, compressed-air leak identification. Autonomous control can come later.
- There is an obvious adjacency to CBAM for carbonTraceAI. The same meter and ERP data that feeds embedded-emissions calculations can feed an energy-optimisation advisor. That creates a "measure, then reduce" upsell where the CBAM cost saved (in €/t) becomes the ROI metric. Fero Labs' Gerdau result shows the pattern: recipe/alloy optimisation counts towards both cost and embedded emissions.
- Savings claims (10-30%) are hard to compare because baselines are not standardised. An agent that produces IPMVP-style measurement-and-verification baselines could be a product in its own right, and it would make savings bankable for energy-efficiency financing.

### Gaps
- I found no independent or peer-reviewed evaluation of Phaidra, BrainBox ARIA or the Siemens/Schneider copilots after 2024.
- Augury (machine health and process AI) returned no usable 2025-2026 results or numbers.
- Basetwo, ABB, and compressed-air or steam optimisation vendors were not covered for lack of tool budget.
- I found no evidence of any of these vendors deploying closed-loop agents in sub-Saharan African factories.

---

## 2. Grid and energy projects: interconnection, permitting, project development, mini-grid operations in Africa, demand response and DERs

### Takeaway
Two clusters are active. In the US, early-stage diligence and permitting agents (Paces and others) are cutting months of desk research for developers. In Africa, mini-grid operators and platforms (Husk, Odyssey) are adopting AI for demand forecasting and dispatch, and Husk explicitly describes "agentic models" re-optimising generation every 30 minutes. The African mini-grid side is driven by financing and subsidy flows (World Bank DARES, results-based finance), so agents that speed up disbursement and portfolio monitoring have a clear payer.

### Cited Findings
**Paces (US siting, interconnection and permitting diligence)**
- Raised an $11M Series A in 2025, led by Navitas Capital with Suffolk Technologies, MCJ Collective, Resolute Ventures, Soma Capital and Y Combinator. It planned expansion to Canada and other countries in 2025. — [ESG Today](https://www.esgtoday.com/energy-infrastructure-software-startup-paces-raises-11-million-to-accelerate-green-energy-development/)
- A later job posting cites "+$18M" raised in total, which I could not reconcile with the Series A figure. It also describes "Agentic AI that automates early-stage due diligence". — [Built In NYC](https://builtinnyc.com/job/development-manager-energy-infrastructure/8900520)
- The product aggregates data on environmental restrictions, moratoriums, prime farmland, soils and permitting requirements, and includes a "Permitting Predictor". The company claims due diligence goes from "months to minutes". — [pv magazine USA](https://pv-magazine-usa.com/?p=13437)
- CEO James McWalter says about 80% of projects never reach construction because of local opposition and interconnection problems, and that "the places with [the] most capacity on the grid… have the worst 'permittability'". — [Latitude Media](https://latitudemedia.com/news/can-ai-fueled-data-research-save-clean-energy-developers-precious-time); [ESG Today](https://www.esgtoday.com/energy-infrastructure-software-startup-paces-raises-11-million-to-accelerate-green-energy-development/)
- Customers include renewable and data-centre developers, real-estate firms and EV-charging companies. — [Built In LA](https://www.builtinla.com/company/paces)

**Husk Power (mini-grids in Nigeria and India, AI-driven DRE platform)**
- Husk launched an AI-driven distributed renewable energy platform meant to manage tens of thousands of mini-grids, rooftop solar, C&I systems and efficient appliances across several markets. AI forecasts demand at each mini-grid, and "agentic models optimize generation assets every 30 minutes". — [Husk Q4 2025 report](https://www.huskpowersystems.com/quater-reports/q4-report---2025); [The Machine Maker](https://themachinemaker.com/news/husk-unveils-ai-driven-distributed-energy-platform-to-bring-power-to-30-million-people/)
- In November 2025 (Rabat), Husk said it is seeking $400M to expand into up to six African countries, with Gambia next. It reported Series E interest of up to $235M. Its targets differ by source: 1 GW in Africa by 2030 (Ecofin) versus 2 GW across the Global South by 2030 (Husk). — [Ecofin Agency](https://www.ecofinagency.com/news-digital/2511-50822-india-based-husk-seeks-400-million-to-expand-ai-driven-decentralised-energy-across-africa); [Husk Q4 2025](https://www.huskpowersystems.com/quater-reports/q4-report---2025)
- Footprint figures conflict: 70 mini-grids in Nigeria (Ecofin) versus more than 200 across Nigeria and India (Techpoint). — [Ecofin](https://www.ecofinagency.com/news-digital/2511-50822-india-based-husk-seeks-400-million-to-expand-ai-driven-decentralised-energy-across-africa); [Techpoint Africa](https://techpoint.africa/news/husk-power-gets-103-million-seriesd/)
- In 2024, Husk's VP of engineering said AI is the only way to automate operations and reach the needed scale. Husk had pledged 2,500 projects in Africa by 2028. — [Latitude Media](https://www.latitudemedia.com/news/why-husk-power-believes-ai-is-key-to-electrifying-rural-communities)

**Odyssey Energy Solutions (mini-grid procurement, finance and data platform)**
- British International Investment and Odyssey launched a $7.5M facility for Nigerian mini-grids in 2025. It combines Odyssey's procurement platform with supply-chain credit, supports the World Bank-backed DARES programme (target: 17.5M Nigerians), and covers the gap between committed and disbursed connection subsidies, mainly upfront equipment costs and import duties. — [BII](https://www.bii.co.uk/en/news-insight/news/bii-and-odyssey-launch-facility-to-accelerate-mini-grid-deployment-in-nigeria/); [WeeTracker](https://weetracker.com/2025/09/15/odyssey-energy-7-5m-bii-nigeria-solar-mini-grids/)
- Odyssey hosts results-based financing windows on its platform, including DARES performance-based grants (Nigeria, Zambia) and CEI Africa. — [Odyssey](https://odysseyenergysolutions.com/news-insights/cei-africa-launches-a-call-for-applications-and-technical-assistance-window-on-odyssey)
- It added interconnected mini-grid modelling (via HOMER) for sizing, feed-in pricing and islanded-versus-interconnected decisions. — [Odyssey](https://odysseyenergysolutions.com/news-insights/now-modeling-interconnected-mini-grids)
- It reports more than $500M of mini-grid projects seeking investment on the platform. — [Odyssey](https://odysseyenergysolutions.com/news-insights/odyssey-announces-mini-grid-projects-seeking-investment-top-500-million)
- An earlier pilot with the Africa Minigrid Developers Association tested remote monitoring and control across four developers. — [Odyssey](https://odysseyenergysolutions.com/news-insights/odyssey-energy-solutions-and-the-african-minigrid-developers-association-pilot-remote-monitoring-and-control-technology)

### Inferences
- In African mini-grids, the binding constraint is capital disbursement, not engineering. Results-based finance needs verified connections, uptime and kWh data before money is paid. An agent that reconciles smart-meter data, field photos and subsidy rules (DARES, CEI Africa) into claim packages and verification files is a strong fit. Who pays: developers (faster cash), fund managers and DFIs (lower verification cost). Odyssey is the natural incumbent, so a new entrant would need to partner with it or focus on a niche such as C&I captive solar or productive-use appliances.
- US-style permitting agents do not transfer directly. African permitting runs through national regulators (for example NERC in Nigeria, EPRA in Kenya), document formats are less standardised, and there is little open GIS and regulatory data. The work is document-heavy, though, which suits LLMs: tariff applications, EIA scoping and licence renewals.
- Husk's "agentic dispatch every 30 minutes" is an operations-scale claim with no published performance metrics (fuel saved, uptime, curtailment). Treat it as positioning until data appears.

### Gaps
- PermitFlow, Atlas, and interconnection-queue agents (for example, tools that parse ISO/RTO queue studies) returned no usable results in my searches.
- I found no CrossBoundary or ENGIE Energy Access (formerly Equatorial) AI deployment details.
- I found no demand-response or DER-aggregation agent evidence specific to Africa.
- No independent performance data exists for AI dispatch on African mini-grids.

---

## 3. Carbon markets and MRV: digital MRV, remote sensing plus LLM agents, PDD drafting, registry workflows, Article 6, ACMI, clean-cooking integrity

### Takeaway
This domain moved in 2025-2026 from "ML on satellite data" to explicitly agentic certification and eligibility workflows. Isometric raised $40M in June 2026 for "agentic certification", and Kanop shipped methodology-eligibility agents. The integrity crisis, especially clean cooking with an estimated 9-10x over-crediting, makes measured, data-heavy MRV commercially valuable. High-rated credits sell at about 4x the price of low-rated ones.

### Cited Findings
**Isometric (registry/certifier moving to agentic certification)**
- Raised a $40M Series A on 22 June 2026, led by AVP (AXA as anchor) with Plural, Lowercarbon Capital, John Doerr and Walter Kortschak. — [Isometric](https://isometric.com/writing-articles/isometric-raises-40m-to-bring-agentic-certification-to-the-industrial-economy); [ESG Today](https://www.esgtoday.com/isometric-raises-40-million-to-expand-industrial-certification-platform-beyond-carbon-markets/)
- In its "Certify" platform, AI agents review sensor readings, satellite imagery, supply-chain records and lab results. They flag discrepancies and surface cases that need expert judgment. Isometric claims work that took months now takes hours; this is unverified. — [Pulse 2.0](https://pulse2.com/isometric-raises-40-million-to-expand-agentic-certification-platform/)
- Claims to be the largest certifier globally by volume, contracted for more than 16M tonnes. Customers include Microsoft, Anglo American, JPMorganChase and Boeing. It targets a $350B industrial certification market beyond carbon. — [ESG Today](https://www.esgtoday.com/isometric-raises-40-million-to-expand-industrial-certification-platform-beyond-carbon-markets/)
- Sources disagree on the founding year: 2022 (ESG Today) versus 2019 (Seedtable). — [Seedtable](https://seedtable.com/companies/isometric/funding-rounds/series-a-2026-06)
- Isometric partnered with Pachama for digital verification of reforestation credits (announced late 2024). Pachama provides geospatial and AI land-suitability mapping, leakage-risk estimates and baselines. — [Isometric](https://isometric.com/writing-articles/isometric-and-pachama-partner-on-digital-verification-for-reforestation-credits); [Carbon Herald](https://carbonherald.com/isometric-to-partner-with-pachama-on-digital-verification-for-reforestation-credits/)

**Kanop (nature-based MRV, with eligibility agents)**
- Kanop launched AI agents that it says compress weeks of analysis into hours. Its "Eligibility Assessment Agent" produces methodology-specific reports for Verra VM0047, Gold Standard ARR, the Isometric Reforestation Protocol, Equitable Earth M001 and others. It also released a redesigned deep-learning biomass model. Self-reported. — [Kanop 2025 review](https://www.kanop.io/blog/reflecting-on-2025-kanops-year-in-review)
- Price signal quoted by Kanop: A-AAA rated credits average $14.80/t versus $3.50/t for CCC-B credits. — [Kanop 2025 review](https://www.kanop.io/blog/reflecting-on-2025-kanops-year-in-review)

**Sylvera (ratings)**
- Sylvera uses AI, satellite data and its own frameworks to rate projects on additionality, permanence, co-benefits and data quality. The source is undated and uses older (2022) funding data, and I found no evidence of LLM agents. — [CarbonCredits.com](https://carboncredits.com/the-top-6-ai-powered-companies-and-how-they-transform-climate-nature-and-carbon-solutions/)

**Clean-cooking integrity (highly relevant to Africa, where most cookstove credits originate)**
- Gill-Wiehl, Kammen and Haya (Nature Sustainability, 2024) estimate cookstove offsets over-credit by 9.2x in a sample covering about 40% of credits, and by about 10.6x when extrapolated across five methodologies. The main drivers are inflated adoption and usage assumptions, underestimated continued use of old stoves ("stacking") and overstated fNRB. Gold Standard's Metered methodology was closest to the study's estimates, at about 1.5x. — [ScienceDaily](https://sciencedaily.com/releases/2024/01/240123122345.htm); [UC Berkeley News](https://news.berkeley.edu/2024/01/23/as-carbon-offsets-cookstove-emission-credits-are-greatly-overestimated)
- Developers pushed back in an open letter calling the study "misguided". The authors said a credit-selling cookstove company provided under 5% of the funding. — [Heatmap](https://heatmap.news/climate/offsets-study-clean-stoves)
- In March 2025, ICVCM approved Gold Standard's Metered & Measured Energy Cooking Devices methodology (v1-1.2) as CCP-eligible, with conditions: capped fNRB (market average 0.86, CCP typically below 0.5) and stricter baseline and usage monitoring. Two improved-cookstove and two household-biodigester methodologies were rejected for lacking rigorous fuel and usage measurement. — [ICVCM](https://icvcm.org/integrity-council-approves-three-cookstove-methodologies/); [Gold Standard](https://www.goldstandard.org/news/icvcm-confirms-gold-standards-clean-cooking-methodologies-as-core-carbon-principles-eligible)
- In June 2025, ICVCM approved Gold Standard TPDDTEC v2, v3 and v3.1 with conditions. — [Gold Standard](https://www.goldstandard.org/news/integrity-council-approves-adipic-acid-and-further-clean-cookstove-methodology-versions)
- At the March 2025 decision, more than 28M credits (about one-third) issued under older Gold Standard versions were still awaiting a ruling. — [Climate Home News](https://www.climatechangenews.com/?p=68503)

### Inferences
- The integrity shift (CCP labels, metered methodologies) turns MRV into a data-engineering problem: stove sensors, fuel sales, household surveys, satellite imagery. That is where agents add value. They can reconcile heterogeneous evidence, flag anomalies, and assemble monitoring reports and verification packages. Isometric's Certify is the incumbent model on the certifier side. On the developer side, especially African cookstove, biochar and ARR developers who must move from default factors to measured data, there is room for a "project-side MRV agent".
- PDD and monitoring-report drafting is a natural LLM task: long templated documents with methodology-specific calculations. Kanop's eligibility agent shows that methodology-specific reasoning can be productised. The liability sits with the VVB and registry, so agents are tolerated as preparers but not as approvers.
- The pattern is the same as carbonTraceAI's CBAM engine: a structured calculation engine, an evidence trail and a verifier-facing report. A CBAM team could move into Article 6 or CCP-grade MRV for African industrial or energy projects (for example, mini-grid diesel displacement, efficient motors). That would reuse the calculation, uncertainty and verification tooling.
- Downside: buyer demand for removal and avoidance credits stayed volatile in 2024-2026, and the integrity scandals hurt cookstove credit prices. A pure carbon-credit play carries market risk that a compliance-driven play (CBAM) does not.

### Gaps
- No usable data on Renoster, Verra or Gold Standard digital registry/API workflows, Article 6 Corresponding Adjustment operations, or ACMI's progress against its 300 Mt/year 2030 target. Searches were not run because of tool budget, so the report writer should not cite figures for these.
- No source confirmed LLM use at Sylvera or Pachama.
- I could not confirm the status of the 28M older Gold Standard cookstove credits after March 2025.

---

## 4. Agriculture and food: regenerative-ag MRV, smallholder advisory agents, EUDR traceability

### Takeaway
LLM advisory for smallholders is the most deployed agentic-style use case in Africa (Digital Green Farmer.Chat in Kenya, Ethiopia and elsewhere), but causal evidence on yields and income does not exist yet. The IFPRI RCT in Kenya runs until March 2027. EUDR has been delayed to 30 December 2026 (large operators) and 30 June 2027 (micro and small), and simplified smallholder routes were added. That creates a definite but softened traceability market, currently filled by vendor platforms with little independent evidence.

### Cited Findings
**Farmer.Chat (Digital Green)**
- An IFPRI-led cluster-RCT is registered in the AEA registry: "Improving smallholder agriculture with generative AI: The impact of Farmer.Chat in Kenya". It covers 600 villages in Nakuru County, crossed with a video intervention, over two seasons, from 1 September 2025 to 31 March 2027. Outcomes are knowledge, practice uptake, yields and income. — [AEA RCT Registry](https://www.socialscienceregistry.org/trials/17035)
- A 60 Decibels survey of 450 Kenyan users found most were new to digital advisory and trust the AI's guidance. This measures perception, not impact. — [60 Decibels](https://60decibels.com/insights/farmers-ai-recommendations/)
- An AICCRA working paper (Kiambu, Kakamega, Meru and Nakuru counties) documents shortcomings of AI-generated advisories on gender inclusivity and cultural relevance. — [CGSpace](https://cgspace.cgiar.org/items/43ae213e-e41e-4c18-b09b-b535e4b78380)
- Technical paper: more than 25,000 expert-reviewed Q&A pairs used for RLHF significantly improved response quality and cultural fit. Lessons from the AIEP initiative. — [arXiv 2601.11537](https://arxiv.org/html/2601.11537v1)
- FY25 annual report: 54% of users are women. Kenya is the testbed for local-language AI, photo-based crop diagnosis and behavioural nudges. Self-reported. — [Digital Green FY25 Annual Report](https://digitalgreen.org/wp-content/uploads/2025/07/Digital-Green-FY25-Annual-Report.pdf)

**EUDR**
- Application is postponed to 30 December 2026 for large operators and 30 June 2027 for micro and small operators, mainly because of worries about the readiness of the TRACES IT system. — [EY Tax News](https://taxnews.ey.com/news/2026-0237-eu-deforestation-regulation-application-postponed-to-30-december-2026); [Food Manufacture](https://www.foodmanufacture.co.uk/Article/2025/11/20/eu-council-backs-eudr-simplification-and-delay-what-should-businesses-do-now)
- Micro and small primary operators file a one-time simplified declaration, and in some cases address-level information can replace plot geolocation. — [VinciWorks](https://vinciworks.com/blog/eudr-delayed-again-what-changed-what-is-now-fixed-and-what-businesses-should-do-in-2026/)
- The Commission's May 2026 review reportedly includes further simplifications, with an estimated 75% cut in annual compliance costs. This is the Commission's own estimate. Sources disagree on whether the dates are now firm. — [StoneX](https://www.stonex.com/en/insights/eudr-enters-a-new-phase-as-coffee-industry-shifts-from-preparation-to-execution/); [CMS](https://cms.law/en/bel/legal-updates/eu-deforestation-regulation-eudr-proposed-delay-what-businesses-need-to-know)
- Coffee traceability usually relies on cooperatives, exporters and intermediaries rather than individual farmers. — [StoneX](https://www.stonex.com/en/insights/eudr-enters-a-new-phase-as-coffee-industry-shifts-from-preparation-to-execution/)
- IDH runs an "Accelerating EUDR readiness" programme. A cocoa pilot links physical authentication to a digital product passport ahead of EUDR. — [IDH](https://idh.org/resources/accelerating-eudr-readiness); [New Food Magazine](https://www.newfoodmagazine.com/news/cocoa-traceability-pilot-links-physical-authentication-to-digital-passport-ahead-of-eudr/2136391.article)

### Inferences
- Smallholder advisory is crowded with donor-funded players (Digital Green, among others) and has a weak payer. Farmers pay little, so the money comes from donors, governments, input companies and offtakers. A for-profit entrant would need a B2B2C model, for example advisory bundled with input credit or offtaker traceability.
- The EUDR opportunity sits with exporters, cooperatives and EU importers, not farmers. The work is reconciling GPS polygons, cooperative membership lists, purchase records and deforestation maps into due-diligence statements. It looks like CBAM (EU import regulation plus supplier data from emerging markets), and carbonTraceAI's supplier-data collection pattern could carry over. But many vendors are competing (Tracextech, osapiens and others), and the delays reduce urgency.
- I found no regenerative-ag MRV evidence specific to African smallholders. Plot sizes and soil-sampling costs make soil-carbon MRV uneconomic without remote-sensing proxies, and that is a known integrity weakness.

### Gaps
- No usable sources on Apollo Agriculture's AI use, Precision Development (PxD) outcomes, Ethiopia deployments (for example ATI/MoA chatbots), or regenerative-ag MRV vendors (Regrow, Agreena) in Africa. Searches were not run because of budget.
- No independent evidence that EUDR traceability platforms in Africa work as claimed.

---

## 5. Circular economy and waste: AI sorting, materials marketplaces, scrap traceability, e-waste

### Takeaway
AI waste sorting is a proven, funded category in OECD markets. AMP raised a $91M Series D and moved from selling robots to running whole facilities and charging per ton. I found no evidence of agentic or LLM layers or African deployments. Scrap traceability for steel and aluminium is the most relevant gap for a CBAM-adjacent founder, because scrap share drives embedded emissions, but I found no sourced deployments.

### Cited Findings
- AMP Robotics raised a $91M Series D (reported 5 December 2024), led by Congruent Ventures with Sequoia, XN, Blue Earth, Liberty Mutual, CalSTRS, Wellington and others, to deploy AMP ONE municipal-solid-waste sorting systems. A first-of-its-kind facility operates in Portsmouth, Virginia. — [Pulse 2.0](https://pulse2.com/amp-ai-based-waste-sortation-company-secures-91-million-series-d/); [Silicon UK](https://www.silicon.co.uk/press-release/amp-raises-91-million-in-series-d-funding-to-revolutionize-waste)
- AMP moved to operating whole facilities. It has about 400 robots deployed and three facilities, plus an agreement with Waste Connections to equip and operate a single-stream facility in Colorado. AMP charges per ton sorted, and the client handles waste sourcing and offtake. — [TechCrunch](https://techcrunch.com/?p=2926592)
- A reported later $55M round is unverified (undated blog source). — [GeekChamp](https://geekchamp.com/?p=812715)

### Inferences
- The business-model shift to "sorting-as-a-service" per ton shows that physical AI wins when the vendor owns the outcome, not just the software. In Africa, informal waste pickers dominate collection, so robotics capex is harder to justify. Software-only plays may fit better: AI-assisted material grading, buyer-seller matching for scrap and plastics, and EPR compliance documentation.
- Steel scrap: CBAM gives EU importers a reason to care about scrap-based (EAF) production versus BF-BOF. African rerolling mills that use local scrap could show lower embedded emissions if scrap origin and share are documented. A scrap traceability and grading agent that feeds CBAM calculations is a logical extension for carbonTraceAI. This is my inference, and I found no sourced market evidence for it.

### Gaps
- Greyparrot's 2025-2026 results and funding were not found (the CB Insights entry referred to a different company).
- No sourced data on materials marketplaces, aluminium or steel scrap traceability tools, or e-waste AI in Africa.

---

## 6. Water, climate adaptation, disaster response, climate risk for insurers and banks, nature/biodiversity (TNFD)

### Takeaway
I did not research this cluster in depth within the tool budget, so there are no sourced findings for it. It should be treated as an open gap for the report writer.

### Cited Findings
- None collected in this pass.

### Inferences
- Structurally, climate-risk analytics for insurers and banks (physical-risk scoring, parametric triggers) and TNFD nature assessments are closer to reporting and risk modelling than to operations. Agents would mostly assemble data and draft assessments, which overlaps with the compliance researchers' scope.
- In Africa, parametric insurance for smallholders and sovereign risk pools runs through donor and DFI channels. Agentic automation of claims triggers and beneficiary verification is plausible, but I have no evidence.

### Gaps
- No sourced evidence on water-utility optimisation agents (for example, leak detection or non-revenue water in African utilities), disaster-response agents, insurer or bank physical-risk agents, or TNFD-assessment agents. Targeted searches are needed (for example: "non-revenue water AI Africa utility", "parametric insurance Africa AI", "TNFD LEAP AI tool").

---

## 7. Green finance operations: green loan/bond eligibility, EU Taxonomy alignment, SLL KPI monitoring, climate-finance proposal drafting, DFIs

### Takeaway
Banks already run rule-based and gen-AI tools for EU Taxonomy eligibility and alignment (GAR/BTAR). I found no documented end-to-end agent for green-loan origination or sustainability-linked-loan (SLL) KPI monitoring. There is also no GCF/GEF proposal-drafting agent: the closest effort, by the NDC Partnership and WRI, is still at scoping. That makes climate-finance proposal preparation for developing-country entities a visible, unclaimed niche.

### Cited Findings
- GFT built a Taxonomy Alignment Tool for BPER that assigns eligibility and alignment to known-purpose loans, feeding Green Asset Ratio and BTAR disclosures. — [GFT](https://www.gft.com/it/it/about-us/newsroom/press-and-news/2024/press-releases/tassonomia-europea-gft-a-fianco-delle-banche-e-delle-imprese-per-la-valutazione-dei-progetti-en)
- Industry view (Amalthea): EU Taxonomy alignment is "emerging as one of the strongest use cases" for gen-AI in banks, and the CSRD extension to SMEs would make manual processing nearly impossible. — [IFRE](https://www.ifre.com/esg/2035348/banks-use-ai-for-eu-taxonomy-alignment)
- Greenomy and Temenos offer automated screening that links banking-book positions to counterparty taxonomy data for GAR computation (2022 partnership). — [Temenos](https://www.temenos.com/blog/greenomy-partners-with-temenos/)
- Climate-finance proposals: the Netherlands Climate Envoy, the NDC Partnership Support Unit and WRI are scoping an AI tool to check funding proposals against fund criteria and analyse climate, economic, geospatial and financial data. It is still at the user-needs stage, before any prototype. — [NDC Partnership](https://ndcpartnership.org/news/tech-good-leveraging-power-ai-unlock-climate-finance)
- The GCF Independent Evaluation Unit, the Adaptation Fund, CIF and GEF jointly commissioned a 2025 scoping study on AI in climate evaluations. It covers evaluation, not proposal drafting. — [GCF IEU](https://ieu.greenclimate.fund/document/scoping-study-ai-climate); [Adaptation Fund PDF](https://www.adaptation-fund.org/wp-content/uploads/2025/03/Scoping-Study-on-Use-of-AI-in-Evaluations-03.24.25v2.pdf)
- Generic grant-writing AI tools (Instrumentl, OpenGrants and others) exist, but none are GCF-specific. — [OpenGrants](https://opengrants.io/best-ai-for-grant-writing/)

### Inferences
- GCF and GEF proposals are long, templated and criteria-driven: theory of change, feasibility study, gender assessment, environmental and social safeguards, economic and financial analysis. Accredited entities and national designated authorities in Africa often lack capacity, and project-preparation money is scarce. An agent that drafts and checks proposals against fund criteria, possibly paid from readiness or project-preparation grants or on success fees, is a real gap. The NDC Partnership's scoping suggests demand, and no commercial player was visible in my searches.
- In the SLL market, KPI monitoring (data collection from borrowers, checking against sustainability performance targets, triggering margin ratchets) is operational and recurring. For African corporate borrowers with DFI or commercial-bank SLLs, an agent that pulls ERP and meter data into KPI evidence would reuse carbonTraceAI's data-ingestion stack (ERPNext and similar). Payers would be lenders (cheaper monitoring) or borrowers (lower cost of verification).
- EU Taxonomy eligibility for African exporters' EU-bank financing is a narrow niche. The bigger green-finance operations market in Africa is DFI-driven (IFC, BII, AfDB, FMO) with their own frameworks, such as the IFC Performance Standards.

### Gaps
- No sourced evidence of SLL KPI-monitoring automation or agents.
- No data on DFI internal AI use for ESG due diligence or portfolio monitoring.
- No information on GCF policy regarding AI-assisted submissions.

---

## 8. Cross-domain synthesis: what limits agents, and where is unclaimed scope in emerging markets/Africa?

### Takeaway
The pattern holds across domains. Well-funded agent companies target OECD hyperscale or enterprise buyers (AI data centres, US developers, EU banks, big retailers). In Africa, agentic AI has reached mini-grid operations (Husk) and smallholder advisory (Digital Green), but not industrial energy control, MRV preparation on the project side, results-based-finance verification, or climate-finance proposal preparation. The common limits are data access (no sub-metering, poor GIS and registry data), physical control and safety (owners will not delegate setpoints), and weak evidence (almost all results are vendor-reported).

### Cited Findings
- Evidence quality: most savings and speed claims are vendor-reported. Examples: Phaidra 10-30% ([Sacra](https://sacra.com/c/phaidra/)); BrainBox "up to 25%" ([SBIZ](https://sustainablebiz.ca/trane-to-acquire-montreals-brainbox-ai)); Isometric "months to hours" ([Pulse 2.0](https://pulse2.com/isometric-raises-40-million-to-expand-agentic-certification-platform/)); Kanop "weeks to hours" ([Kanop](https://www.kanop.io/blog/reflecting-on-2025-kanops-year-in-review)); Paces "months to minutes" ([pv magazine](https://pv-magazine-usa.com/?p=13437)).
- The only rigorous causal evaluation found, the Farmer.Chat RCT, will not report until after March 2027. — [AEA Registry](https://www.socialscienceregistry.org/trials/17035)
- Integrity regimes now reward measured data over default factors, with stricter fNRB and monitoring conditions under CCP. — [ICVCM](https://icvcm.org/integrity-council-approves-three-cookstove-methodologies/)
- African energy access is gated by subsidy disbursement (the DARES committed-versus-disbursed gap). — [Odyssey/BII](https://www.bii.co.uk/en/news-insight/news/bii-and-odyssey-launch-facility-to-accelerate-mini-grid-deployment-in-nigeria/)

### Inferences
These are ranked by fit with carbonTraceAI's existing assets: CBAM calculation engine, ERP ingestion, verifier-facing reports, and African manufacturer relationships.
1. **"Measure, then reduce" energy and emissions advisor for CBAM-exposed African manufacturers.** It reuses meter and ERP data already collected for CBAM and quantifies savings in € of avoided CBAM cost. It starts advisory-only, which avoids the physical-control and safety barrier. Low competition in Africa (inference).
2. **Project-side MRV and verification-package agent** for African carbon projects (cookstoves, mini-grid diesel displacement, biochar, efficient industrial equipment) moving to CCP-grade metered methodologies. It mirrors Isometric's certifier-side agents from the developer side.
3. **Results-based-finance claims agent for mini-grid and DRE developers** (DARES, CEI Africa and similar). It turns meter, photo and connection data into disbursement-ready claims. Incumbent risk: Odyssey.
4. **Climate-finance proposal agent (GCF, GEF, Adaptation Fund)** for African accredited entities and developers. Demand is signalled by NDC Partnership scoping, and I saw no commercial incumbent. Payer uncertainty: readiness grants or success fees.
5. **SLL and green-loan KPI evidence agent** for African corporates borrowing from DFIs or banks. It reuses the ERP-ingestion stack.
6. **Steel and aluminium scrap traceability agent** that feeds CBAM embedded-emissions calculations for EAF and rerolling mills. Speculative: no sourced market evidence.
- Common risk: when vendors own outcomes (AMP per-ton, Phaidra paid back from savings), physical AI is easier to buy than software-only advisory. For any Africa play, a shared-savings or success-fee pricing model may matter more than how sophisticated the agent is.

### Gaps
- No market-sizing data for any Africa-specific operational agent category.
- No independent benchmarks of agentic versus conventional ML or human workflows in any domain covered.
- Domain 6 (water, adaptation, insurance, TNFD) and several named companies (Augury, Basetwo, PermitFlow, Atlas, Renoster, Greyparrot, Apollo Agriculture, PxD, CrossBoundary, ENGIE Energy Access, ACMI) remain unresearched and need follow-up searches.
