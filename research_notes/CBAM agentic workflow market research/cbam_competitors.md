# Competitive Landscape of CBAM-Specific Compliance Software (as of Oct 2026)

Research date: 12 Oct 2026. Most vendor facts come from vendor websites (marketing claims, not verified) or from cbamguide.com, a third-party review site whose vendor data was checked in July 2026 (page updated 12 Oct 2026). Older items (2024-2025) are flagged. Several "ranking" pages are written by competitors (Coolset, The Sustainability Cloud, Carbmee, Zevero), so read them as marketing.

## Q1. Who are the CBAM-focused vendors, who do they serve, and what do they do (workflow, pricing, funding, AI)?

### Takeaway
The market splits into (a) CBAM-only specialists aimed mainly at **EU importers/declarants** (CBAMBOO, kolum, Dubrink, CbamTrack, CarbonChain), (b) broad ESG/carbon/supply-chain suites with a CBAM module (osapiens, IntegrityNext, Carbmee, Sphera, Assent, Coolset, Greenly, Normative, Zevero, VERSO), and (c) ERP giants (SAP, Siemens SiGREEN, Microsoft). Almost all are importer-first. Pricing is mostly quote-based. Only a few low-end tools publish prices (CbamTrack: €0/€79/€199 per month). None of the major vendors makes a credible, specific AI/LLM claim for CBAM. The only "AI" labels found are generic: CleanCarbon.ai, CASEM, Sinai and Assent.

### Cited Findings

**CBAM-only specialists (importer-first)**
- **CBAMBOO** (London, founded 2023 by Gabriel Rozenberg; around 6 listed staff). Reported pre-seed round of about £1M in Dec 2023, led by Pale Blue Dot. The primary announcement is no longer accessible, so this is unconfirmed. — [cbamguide CBAMBOO review](https://cbamguide.com/software/cbamboo/)
- CBAMBOO serves importers above 50 t and also non-EU suppliers. The supplier-side product covers embedded-emissions calculation under the EU methodology, upstream data integration, "verification-ready" reports and secure sharing with EU customers. Supplier access is reportedly free. — [cbamguide CBAMBOO review](https://cbamguide.com/software/cbamboo/)
- CBAMBOO Pro (8 Jul 2025) generates XML that is "compatible" with the EU CBAM registry. No direct registry API is documented, so declarants still file themselves. No AI features or verifier partnership are mentioned. Partners: AEB SE (customs software) and ASUENE (co-marketing, around Nov 2025). Case studies: Stainless Steel Services, Mustad. ISO 27001. — [cbamguide CBAMBOO review](https://cbamguide.com/software/cbamboo/)
- CBAMBOO pricing (third-party, unverified; not on CBAMBOO's own site): Basic €9,000/yr, Pro €19,000/yr (up to 1,000 t), Enterprise €31,000/yr. — [cbamguide CBAMBOO review](https://cbamguide.com/software/cbamboo/)
- **CarbonChain** (London/NY, founded 2019, YC S20). $10M Series A on 25 Apr 2023, co-led by Union Square Ventures and Voyager Ventures. — [CarbonChain blog](https://www.carbonchain.com/blog/carbonchain-raises-10m-series-a-to-accelerate-global-decarbonization-through-carbon-accounting); [ESG Today](https://www.esgtoday.com/carbon-accounting-startup-carbonchain-raises-10-million-to-build-out-supply-chain-emissions-tracking-platform/)
- CarbonChain funding totals differ: CB Insights lists $12.04M and Caplight $12.49M. — [CB Insights](https://www.cbinsights.com/company/carbonchain/financials)
- No CarbonChain funding round after 2023 was found.
- CarbonChain sells separate offerings for declarants and installations:
  - **Declarants:** automated supplier outreach, actual-emissions validation by an in-house team, benchmark and scenario modelling, audit trail, EU-template reporting, a CBAM calculator ("Try free").
  - **Installations:** installation-level modelling, verification-ready data packages, product carbon footprints (PCF) with an SGS-validated methodology.
  - **Supplier catalogue:** a public catalogue of steel and aluminium installations with free supplier risk ratings.
  - **Not mentioned:** XML, registry integration, ERP integration, AI. No pricing is shown.
  - **Logos:** Société Générale, IXM, Gunvor, ING, Ameropa, thyssenkrupp, Volvo.
  — [CarbonChain CBAM page](https://www.carbonchain.com/cbam)
- cbamguide classes CarbonChain as quote-based, enterprise and commodity-focused (iron, steel, aluminium, fertilizers), and says its registry submission and XML claims are vendor-described and "to be checked in a demo". — [cbamguide best CBAM software](https://cbamguide.com/software/best-cbam-software/)
- **kolum** (Berlin):
  - **Target:** German-speaking and EU mid-market industrial importers, including multi-entity groups.
  - **Workflow:** supplier invitations with standardized data requests (cbamguide says in 20+ languages), actual versus default values per CN code, "audit-ready" exports for the EU registry, automated quality assurance.
  - **Not mentioned:** AI, ERP integration, verifier.
  - **Pricing:** "Custom".
  — [kolum product page](https://www.kolum.earth/en/cbam/product); [cbamguide](https://cbamguide.com/software/best-cbam-software/)
- **Dubrink** (EU-based):
  - **Target:** EU importers, from small importers to enterprises.
  - **Features:** supplier connectivity, calculation engine, "direct integration with verification bodies", one-click EU-compliant XML, audit trails.
  - **Languages:** site in 15 EU languages, including French and Portuguese but not Arabic.
  - **Not mentioned:** AI. Prices are not shown on the importer page.
  — [Dubrink](https://www.dubrink.com/cbam-compliance-for-importers)
- **CbamTrack** publishes pricing, a rarity in this market:

  | Tier | Price | Products | Key inclusions |
  |---|---|---|---|
  | Free | €0 | 1 | 1 annual declaration, PDF export, Communication Sheet |
  | Starter | €79/mo | 6 | Declaration Filing Assistant |
  | Growth | €199/mo | 30 | Supplier portal, XML/Excel/JSON export, anomaly detection, what-if simulator, 3 seats |

  No verifier, ERP, API or language support is listed. — [CbamTrack pricing](https://cbamtrack.com/pricing)
- **CBAM Pulse** lists a Pro plan at €39/mo or €390/yr. It looks more like an information and tools site than a full compliance product. — [CBAM Pulse pricing](https://cbampulse.com/pricing)
- **Other small or newer CBAM-only tools** found but not profiled in depth: ClimEase (CBAM plus supply-chain emissions, certificate cost tracking), Laurisystems (built-in EU factors), CBAMgate (free exporter cost calculator), CBAMEase, Tanso, Inverto. — [Formist list](https://formist.ai/blog/best-cbam-reporting-software-2026); [Climease](https://climease.com/en/); [Laurisystems](https://www.laurisystems.com/); [CBAMgate](https://cbamgate.com/); [Notixit](https://notixit.com/blog/construction-cbam-cement-steel-reporting-software)

**Suites with a CBAM module**
- **osapiens HUB for CBAM** (Germany):
  - Connects import, procurement, supplier and regulatory data.
  - Guided supplier data collection plus eLearning.
  - Embedded-emissions and carbon-cost calculation, supplier benchmarking, "EU-compliant XML exports".
  - Covers all six CBAM goods groups. Modules can be activated independently, and CBAM data flows into its corporate and product carbon modules.
  - Quarterly product-update webinar on 8 Oct 2026 (product is actively maintained).
  — [osapiens CBAM](https://osapiens.com/en/solutions/carbon-management/cbam); [osapiens events](https://osapiens.com/en/events-overview)
- **IntegrityNext** launched a CBAM platform in Apr 2024 (dated). It covers supplier data collection, financial exposure against EU ETS prices, and XML for the EU Transitional Registry. Its roots are in supply-chain ESG and due diligence. — [IntegrityNext press](https://www.integritynext.com/about-us/press/detail/integritynext-introduces-platform-for-co-border-balancing-system-cbam)
- **Carbmee** (Berlin) expanded its CBAM module in Jul 2024 with an ingest API for CBAM transactions and LCA models for imported goods. A third-party roundup credits it with a Registry API integration and mid-market pricing. — [Carbmee press](https://www.carbmee.com/knowledge-insights/press/carbmee-enhances-cbam-capabilities-for-compliance); [Notixit](https://notixit.com/blog/construction-cbam-cement-steel-reporting-software)
- Carbmee joined EcoVadis's Carbon Data Network on 14 Apr 2026. This is a data partnership, not an EcoVadis CBAM module. — [EcoVadis](https://resources.ecovadis.com/news-press/ecovadis-accelerates-scope-3-transparency-adding-carbmee-to-rapidly-expanding-carbon-data-network)
- **Sphera** offers automated supply-chain data gathering, direct and indirect embedded-emissions calculation, compliance-ready templates, audit-ready storage and consulting. Its page does not mention XML, registry, verifier, ERP integration, AI or pricing. It targets importers and also non-EU exporters, for example in the UK. — [Sphera CBAM](https://sphera.com/solutions/supply-chain-risk-management/supplier-engagement-solution/comprehensive-compliance-for-the-eu-cbam/)
- **Assent** offers a built-in CBAM calculator and primary supplier data mapping per CN code and part. Coolset's Aug 2025 article claims "AI-driven supplier engagement". — [Assent](https://www.assent.com/solutions/esg-supply-chain/cbam/); [Coolset article, Aug 2025](https://www.coolset.com/academy/top-cbam-software-tools-7f11d)
- **Sinai** is marketed with "AI-powered transition planning" and is described as less focused on CN-code and customs-level reporting (Aug 2025). — [Coolset article](https://www.coolset.com/academy/top-cbam-software-tools-7f11d)
- **Coolset** (Amsterdam, founded 2022, formerly Greencast.io) is quote-based per module. By Jul 2026 its CBAM product page redirected to the homepage, so the module's status is unclear. — [cbamguide](https://cbamguide.com/software/best-cbam-software/)
- **Greenly** is carbon-accounting-first, with CBAM as one obligation among several, and quote-based. — [cbamguide](https://cbamguide.com/software/best-cbam-software/)
- **Normative** combines an emissions engine with consultancy-backed CBAM guidance and "may need customization to align with CBAM". — [Coolset article, Aug 2025](https://www.coolset.com/academy/top-cbam-software-tools-7f11d)
- **Zevero** pairs carbon software with a named climate expert and lists CBAM among its frameworks. It claims a TÜV SÜD evaluation against ISO/IEC 25051 (vendor blog). — [Zevero blog](https://www.zevero.earth/blog/plan-a-alternatives-for-carbon-management)
- **Sustamize** is a CO2e factor database and PCF vendor (Matcher and Assembler tools). It claims its datasets reduce importers' reliance on default values, which positions it as a data supplier rather than a filing tool. — [Sustamize](https://www.sustamize.com/carbon-glossary/what-tools-are-available-to-assist-with-cbam-and-csrd-compliance)
- **VERSO** (Germany) has a CBAM module inside a supply-chain hub: supplier requests, certificate cost forecasting, report generation. — [VERSO](https://verso.de/en/cbam/)
- **PwC Germany "Check Your Value Chain"** has a CBAM module. This shows Big Four firms productising CBAM. — [PwC store](https://store.pwc.de/en/products/check-your-value-chain/cbam-module)
- **Persefoni, Watershed, Sweep:** third-party comparisons list no CBAM among their frameworks. No CBAM module launch was found for any of them. Watershed is noted for AI product footprinting, which is relevant to goods-level data. — [onestopesg comparison](https://onestopesg.com/esg-resources/leading-carbon-accounting-software-companies); [Watershed UK profile](https://sustainabilityreportingstandards.co.uk/best-carbon-management-software-top-carbon-accounting-software/watershed); [cbamguide](https://cbamguide.com/software/best-cbam-software/)

**ERP and big-tech vendors**
- **SAP** announced an "end-to-end CBAM declarants solution" on 25 Jun 2026, built on SAP Sustainability Footprint Management and SAP Green Ledger.
  - **Available today:** Green Ledger recognition, valuation and revaluation of CBAM liabilities, with postings to accounts.
  - **"Coming soon":** certificate holdings, cash forecasting, product-level cost breakdown, Footprint Management data capture and calculation, a CBAM dashboard, and report generation.
  - **Supplier data:** comes in through Excel upload with "automated interpretation".
  - **Not mentioned:** XML or registry formats, verifier support.
  - **Scope:** declarant-only for now; "will later expand to support operator needs".
  — [SAP News](https://news.sap.com/2026/06/sap-introduces-cbam-declarants-solution/)
- SAP Green Ledger reached general availability on 16 Dec 2024. — [SAP News](https://news.sap.com/2024/12/sap-green-ledger-general-availability/)
- **Siemens SiGREEN** is a product carbon footprint (PCF) tool that uses real data rather than averages, with CBAM-related features. NTT DATA offers an accelerator connecting SiGREEN to SAP ERP (older article, date not confirmed). — [NTT DATA](https://nttdata-solutions.com/us/blog/empowering-green-futures-with-sap-sigreen/)
- Siemens and Shanghai Lin-gang run a pilot carbon and data-compliance oversight platform for steel, textile and chemical manufacturers in the Yangtze River Delta. — [Lin-gang](https://en.lingang.gov.cn/html/website/lg/English/News1630758253379031042/Updates/2074410207822282754.html)
- **Microsoft "EU CBAM Copilot"** is a carbon-fee estimator in Microsoft Sustainability Manager, with a Copilot Studio "EU CBAM Estimator" template. The documentation is archived and no longer updated (2024 wave 2 release plan). This is the only big-vendor LLM-branded CBAM feature found. — [Microsoft Learn](https://learn.microsoft.com/en-us/industry/release-plan/2024wave2/cloud-sustainability/estimate-carbon-fee-eu-cbam-copilot)

**Verifiers and testing bodies offering CBAM services**
- TÜV Rheinland South Africa offers CBAM services. — [TÜV](https://www.tuv.com/south-africa/en/lp/cbam-and-environmental-services/)
- SCS Global Services offers CBAM services for Africa. — [SCS Africa](https://www.scsglobalservices.com/africa/services/carbon-border-adjustment-mechanism-cbam)
- SGS validates CarbonChain's methodology. — [CarbonChain](https://www.carbonchain.com/cbam)
- SGS Morocco, Bureau Veritas Morocco and RINA-affiliated verifiers form virESG's local verifier network. — [virESG](https://viresg.com/en/cbam-morocco)

### Inferences
- The dominant workflow is the importer's: supplier request, then calculation, then XML. Supplier-side "installation" products (CBAMBOO supplier, CarbonChain installations, Sustrack) usually feed one importer's portal. None found ingests the producer's ERP natively at scale.
- AI is mostly branding. No major vendor documents LLM-based document extraction (for example invoices to activity data) or agentic filing. That leaves room to differentiate if it can be shown to verifiers.
- SAP's "coming soon" list suggests that even incumbents had no complete CBAM product as of mid-2026. ERP-native CBAM is still immature, and SAP is declarant-first.

### Gaps
- Not found or not verified as CBAM products: **Carboneer, CBAMly/CBAM.ly, Cumulus, ecoPlanet, Pledge, Avelios, DGrade, Climatiq (API), Emitwise, Manufacture 2030, Tracemission, "Ecocheck/CBAM Copilot" (as a standalone product), DPP-style tools**. Searches returned nothing CBAM-specific. Some may not exist under these names.
- **Vaayu** is a fashion PCF platform, not a CBAM tool. It was acquired by Carbonfact (see Q4).
- No CBAM-specific funding found for kolum, Dubrink, osapiens's CBAM line or the small self-serve tools.
- No public pricing for osapiens, Sphera, IntegrityNext, Carbmee, kolum, Dubrink (it has a pricing page that was not reviewed), CarbonChain, SAP or Siemens.
- No G2 or Capterra review evidence was gathered on CBAM-module quality.
- DNV and Bureau Veritas global CBAM service offerings were not individually researched.

## Q2. Regional tools: India, Türkiye, China, Africa (the producer/exporter side)

### Takeaway
Most producer-side competition is in **India and Türkiye**. Those vendors are often consultancies bundling software, managed services and verifier coordination. China has a few local platforms. **For Africa there is essentially one dedicated product found (virESG/virCBAM, for the Maghreb), plus Indian-built The Sustainability Cloud marketing country pages.** No South African, Kenyan, Nigerian or other Sub-Saharan CBAM software startup was found.

### Cited Findings
**India**
- **CleanCarbon.ai** was founded by IIM Ahmedabad alumni Nilesh and Rashmi Bhattad, with offices in Pune, Dubai and Silicon Valley. It combines consultation with an "AI-based software platform" for steel, aluminium, cement and fertilizer exporters. In Jul 2024 it claimed "hundreds of clients" and 100+ CBAM reports in six months (dated, self-reported). — [AlCircle, 21 Jul 2024](https://www.alcircle.com/news/cleancarbon-ai-simplifying-cbam-compliance-for-indian-aluminium-and-steel-exporters-111492)
- CleanCarbon.ai's own site now claims "200+ exporters compliant" (self-reported). — [CleanCarbon.ai](https://cleancarbon.ai/)
- **CarbonSettle** is a managed service. Exporters share electricity bills, fuel invoices and production logs, and CarbonSettle handles the EU XML report and verifier coordination. It offers a free first-quarter report. It targets MSMEs. — [CarbonSettle](https://carbonsettle.com/cbam-steel-exporters-india)
- **The Sustainability Cloud** (Logicladder, India) offers CBAM for exporters and importers, alongside Indian frameworks (BRSR, CCTS). Case studies: NTPC, LOGOS Asia, Pee Vee Impex. No pricing.
  - It publishes self-ranking "Best CBAM software in Egypt/Algeria/USA/Canada" pages, claiming verifier access and EU importer communication tools.
  — [TSC CBAM exporter](https://www.thesustainabilitycloud.com/products/cbam-exporter/); [TSC Egypt](https://www.thesustainabilitycloud.com/blog/cbam-software-in-egypt/); [TSC Algeria](https://www.thesustainabilitycloud.com/blog/best-cbam-software-in-algeria-2026/)
- Other Indian players: GreenSutra (consultancy), EnCarbonSys (assessment and verification coordination), cbam.in. — [GreenSutra](https://greensutra.in/services/cbam-solutions/); [EnCarbonSys](https://encarbonsys.com/cbam-blog/cbam-india-exporters-guide-2026.html); [cbam.in](https://cbam.in/)

**Türkiye**
- **Sustrack S-CBAM** (CSI Bilgi Teknolojileri A.Ş., Istanbul):
  - Producer-side: generates the Monitoring Plan, Operator Emissions Report and Summary Emissions Report from the manufacturer's own production data.
  - Supports multiple installations and products, actual-versus-default intensity comparison, and a supplier/precursor request flow.
  - Data comes in through the UI or bulk upload. System connections are a per-project service, so it is not ERP-native.
  - Languages: Turkish and English. No pricing, AI, XML or communication-template support is mentioned.
  — [Sustrack S-CBAM](https://sustrack.ai/products/s-cbam)
- **Karbonet** serves Turkish exporters and their EU buyers: installation records, per-good embedded emissions, default-versus-actual comparison, buyer-facing PDFs, read-only verifier access, and a Türkiye default-value table. — [Karbonet](https://karbonet.com/cbam-software)
- **QuickCarbon** has a Turkish SKDM module whose output is compatible with the EU Excel template. — [QuickCarbon](https://www.quickcarbon.com/tr/skdm/)
- **CimpactPro** sells tiered SKDM packages. — [CimpactPro](https://cimpactpro.com.tr/paketler)
- **CASEM/SUSTAINES** offers "AI-supported" SKDM software plus consultancy. CASEM itself notes that firms can report in-house with the EU Excel template. — [CASEM](https://www.casem.com.tr/cbam-skdm-yazilimi/)
- **netzero.com.tr** publishes a CBAM intelligence page for Turkish exporters. — [netzero.com.tr](https://netzero.com.tr/intelligence/cbam)
- Turkish financing support exists, such as VakıfBank and MEXT programmes for CBAM reporting. — [netzero.com.tr](https://netzero.com.tr/intelligence/cbam)

**China / Hong Kong**
- **Carbbit** (Shanghai Carbbit Digital Technology, founded 2022) offers exporter data collection, embedded-carbon calculation, tariff-exposure estimation and submission prep for steel, aluminium, fertilizer and cement. The source is a third-party directory. — [Net Zero Compare](https://netzerocompare.com/software/carbbit)
- The Federation of Hong Kong Industries and the University of Hong Kong offer a free CBAM assessment and liability tool. — [FHKI](https://industryhk.org/en/info/industry-news/cabon-tool)
- A 2024 China Daily commentary said Chinese firms "can only rely on foreign" carbon platforms for footprint management (dated). — [China Daily via PressReader](https://www.pressreader.com/hong-kong/china-daily/20240401/281749864365095)

**Africa**
- **virESG / virCBAM** offers "end-to-end CBAM compliance for Maghreb exporters" (Morocco, Tunisia, Algeria):
  - Data collection, XML for the EU registry, ONEE electricity-data integration, preloaded Moroccan grid factors.
  - A local verifier network (SGS Morocco, Bureau Veritas Morocco, RINA), claimed 40-50% cheaper than flying in EU verifiers.
  - **Interface and reports in English, French and Arabic.**
  - No HQ, pricing or named customers shown.
  — [virESG Morocco](https://viresg.com/en/cbam-morocco); [liners.com listing](https://liners.com/vircbam)
- **Tunisia: CarboTrack.io** is a carbon-footprint platform (GHG Protocol, ISO 14064), not a CBAM declaration tool (Aug 2025). — [La Presse](https://www.lapresse.tn/2025/08/31/%e2%81%a6carbotrack-io%e2%81%a9-une-plateforme-tunisienne-pour-democratiser-le-bilan-carbone/)
- **Morocco: Imanor** set up a GHG declaration verification and validation system covering CBAM. — [aujourdhui.ma](https://aujourdhui.ma/?p=444840)
- **South Africa:** only consultancies and certifiers were found: Anthesis ZA, TÜV Rheinland SA, SCS. — [Anthesis ZA](https://www.anthesisgroup.com/za/regulations/carbon-border-adjustment-mechanism-regulations-cbam/); [TÜV](https://www.tuv.com/south-africa/en/lp/cbam-and-environmental-services/)
- A TIPS study found South Africa's iron, steel and aluminium sector not ready financially or administratively, citing "incompatible infrastructure of accounting GHG emissions". — [TIPS](https://www.tips.org.za/research-archive/sustainable-growth/green-economy-2/item/4791-tips-south-africa-iron-steel-and-aluminium-industries-readiness-to-respond-to-cbam)
- **Exposure sizes:**
  - South Africa's iron and steel exports to the EU are estimated at about USD 5.7B. — [cbamguide countries](https://cbamguide.com/countries/)
  - African fertiliser exports exposed to CBAM total USD 2,923M (Egypt 1,247M, Morocco 719M, Algeria 684M). — [cbamguide countries](https://cbamguide.com/countries/)
  - African iron and steel exports exposed total USD 3,214M (South Africa 1,660M, Egypt 348M, Tunisia 270M). — [cbamguide countries](https://cbamguide.com/countries/)
- Morocco's CESE says only 3.7% of trade with the EU is concerned, 2.9% of it fertilisers. — [FNH](https://fnh.ma/article/developpement-durable/macf-union-europeenne-bilan-industriels-marocains)

### Inferences
- **virESG is the closest direct analogue to carbonTraceAI** (producer-side, Africa, French and Arabic, XML, local verifiers), but only for the Maghreb. Its maturity is unclear: no named customers and no HQ shown.
- The Sustainability Cloud is the most aggressive at SEO-targeting African countries. Its content strategy, not proven product depth, is the competitive threat.
- Indian and Turkish producer-side vendors lean on managed services (bills in, report out). That suggests SME producers buy outcomes, not software.

### Gaps
- No Sub-Saharan software vendor found: South Africa, Kenya, Nigeria, Ghana, Mozambique (aluminium, for example Mozal) or Egypt as a home base.
- No Portuguese-language producer-side tool found, which matters for Mozambique and Angola. Dubrink has a Portuguese site, but it is importer-side.
- No pricing found for any regional producer-side vendor except CarbonSettle's free first-quarter offer.
- Carbbit's and virESG's funding and team size are unknown.

## Q3. Free EU tools (Communication Template, Registry, O3CI portal, calculators) and how paid tools compete

### Takeaway
The Commission provides an **optional Excel Communication Template** for installations, which a third-party news site says is still v2.1 from Dec 2024. It also runs the **CBAM Registry**, including the **O3CI portal**, where non-EU operators upload installation data once and share it with all declarants, and where accredited verifiers issue reports. It does not offer an official cost calculator. Paid tools compete on supplier chasing at scale, validation and actual-versus-default optimisation, financial modelling, and audit trail. The O3CI portal directly erodes "share data with each importer" features.

### Cited Findings
- The Commission's page offers the CBAM Communication Template for installations, a video training module and worked examples (cement, aluminium, fertilisers, hydrogen, steel). The template is "not mandatory" and is meant as a guiding tool. — [EC CBAM Communication & FAQs](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-communication-and-faqs_en); [Bossard supplier helpsite](https://www.bossard.com/global-en/about-us/supplier-portal/cbam-helpcenter/)
- A third party says the current template is v2.1 (file dated 13 Dec 2024), written for the transitional period, with no newer version. This was not confirmed on the EC site. — [cbamfile news](https://cbamfile.com/cbam-news)
- The **CBAM Registry** has these parts:
  - **AMM:** authorised-declarant applications.
  - **DRMC:** monitoring of imports, emissions, certificates and penalties; also helps anticipate the 50% rule.
  - **Declarants portal:** user manual dated 21 Aug 2026.
  - **O3CI portal:** non-EU installation operators "upload installation and emissions data and share it with reporting declarants" instead of sending it to each declarant separately.
  - **Verifier access:** accredited verifiers register via their national competent authority (guidance dated 28 Aug 2026), connect with operators, review data and issue verification reports in O3CI.
  — [EC CBAM Registry](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry_en)
- Registry onboarding for non-EU companies:
  - Guidance on the access-request procedure was published 19 Feb 2026.
  - The O3CI registration guide followed on 24 Feb 2026.
  - Registration requires EU Login with two-factor authentication and a single PDF of documents, preferably in English.
  — [EC CBAM Registry](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry_en)
- The non-EU operator platform has been online since Jan 2025. — [Ashurst/SCS guidance summary](https://www.ashurst.com/en/insights/eu-cbam-a-guide-for-importers-and-third-country-producers/)
- The Registry page lists no Commission calculator. All calculators found are third-party: cbam-calculator.eu, CBAMgate, cbamguide tools, and vendor estimators from CarbonChain, kolum and Coolset. — [EC CBAM Registry](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry_en); [CBAMgate](https://cbamgate.com/); [cbamguide tools](https://cbamguide.com/tools/); [cbam-calculator.eu](https://cbam-calculator.eu/)
- Third-party calculators use default values from Implementing Regulation 2025/2621 and the CBAM factor phase-in schedule (2.5% in 2026, rising to 100% in 2034). — [CBAMgate](https://cbamgate.com/)
- Commission certificate prices:
  - Q2 2026 price cited as €75.28 by a calculator site (unverified). — [CBAMgate](https://cbamgate.com/)
  - Q3 2026 price cited as €82.32, published 5 Oct 2026. — [cbamguide](https://cbamguide.com/software/best-cbam-software/)
- A Turkish consultancy concedes that firms can calculate and report in-house with the SKDM (EU) Excel template, so consultancy is optional. — [CASEM](https://www.casem.com.tr/cbam-skdm-yazilimi/)
- Vendors price against the free template:
  - Some tools explicitly export a "Communication Sheet" (CbamTrack, all tiers). — [CbamTrack](https://cbamtrack.com/pricing)
  - QuickCarbon outputs in the EU Excel template format. — [QuickCarbon](https://www.quickcarbon.com/tr/skdm/)
  - One vendor sells pre-filled EU template packs for Indian and Indonesian production profiles. — [cbamfile](https://cbamfile.com/cbam-news)
- Indirect emissions are not mandatory in the definitive period from 1 Jan 2026 unless revised. — [Bossard helpsite](https://www.bossard.com/global-en/about-us/supplier-portal/cbam-helpcenter/)

### Inferences
- O3CI changes the producer-side value proposition. Software should help producers **prepare, verify and upload to O3CI** with a verifier-grade audit trail, not just email Excel files to importers. Tools built around per-importer sharing (CBAMBOO supplier sharing, importer supplier portals) may lose relevance as O3CI adoption grows.
- An official template that is unchanged since Dec 2024 (if accurate), while definitive-period rules and Aug 2026 verification guidance are new, leaves room for tools that track rule changes.
- Free tools are enough for simple single-installation producers who report on defaults. Paid tools win when actual values lower cost, which vendors claim saves 30-40% (unverified).

### Gaps
- Not confirmed whether the Commission publishes an official XSD or XML schema for declarations, or whether O3CI accepts bulk or API upload. The Registry page does not mention XML.
- No official Commission calculator found. Some may exist inside the Registry's DRMC module.
- The 24 Aug 2026 Commission verification guidance is cited only by a law firm. — [Kohen Avocats](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)

## Q4. Market consolidation signals (acquisitions, pivots, shutdowns) after the Omnibus 50-tonne threshold

### Takeaway
The Omnibus (Reg. (EU) 2025/2083) 50-tonne de minimis removed about 90% of importers (about 182,000) while keeping more than 99% of emissions in scope. That shrank the long-tail SMB importer market that many CBAM-only tools targeted. Consolidation is visible in the broader carbon-accounting market (Diginex/Plan A, reported Greenly/Normative, Carbonfact/Vaayu, Novisto/Minimum). Direct CBAM-only exits are weakly evidenced: one CBAM SaaS listed for sale on Acquire.com, and Coolset's CBAM page disappearing.

### Cited Findings
- **The Omnibus rule:**
  - A 50 t net-mass threshold per calendar year applies, aggregated across all CN codes (Art. 2a of Reg. 2023/956, as amended by 2025/2083).
  - It removes about 90% of importers (about 182,000) while more than 99% of embedded emissions stay covered.
  - Electricity and hydrogen are never exempt.
  — [cbamguide](https://cbamguide.com/software/best-cbam-software/); [ICAP](https://icapcarbonaction.com/en/news/eu-adopts-simplifications-cbam-rules-ahead-compliance-phase-starting-2026)
- A separate estimate puts the exempted emissions at 0.87% (Apr 2025-Mar 2026). — [CarbonChain Omnibus blog](https://www.carbonchain.com/blog/cbam-omnibus-new-rules-for-importers)
- The first annual declaration is due 30 Sep 2027 (for 2026). Authorised-declarant applications by 31 Mar 2026 allowed provisional importing. — [cbamguide](https://cbamguide.com/software/best-cbam-software/); [cbamdefaults](https://cbamdefaults.com/guides/authorised-declarant)
- **Diginex acquired Plan A** (Berlin) at about €55M valuation, mostly in shares, plus an earnout of up to €25M. It was agreed or finalised around 7 Jan 2026. Verdantix titled its analysis "Carbon Software Consolidation Will Continue In 2026". — [Dealroom](https://app.dealroom.co/news/note/lightspeed-backed-carbon-accounting-startup-plan-a-acquired-by-diginex-in-55m-deal); [Verdantix](https://www.verdantix.com/client-portal/blog/carbon-software-consolidation-will-continue-in-2026--diginex-acquires-plan-a)
- **Greenly reportedly acquired Normative** for just over €64M (reported Sep 2026). Neither company has confirmed it. Normative reportedly posted a 2024 loss of about SEK 165M on SEK 88M revenue. — [Clean the Sky](https://www.cleanthesky.com/innovation/climate-data-company)
- **Carbonfact acquired Vaayu** (Berlin, fashion PCF, $13M raised from Atomico and CapitalT) on 27-28 May 2026, price undisclosed. This is DPP/fashion-driven, not CBAM. — [ESG Today](https://www.esgtoday.com/carbonfact-acquires-fashion-sustainability-software-provider-vaayu/); [FashionUnited](https://fashionunited.uk/news/business/fashion-tech-platform-vaayu-acquired-by-carbonfact/2026052888297)
- **Other 2026 deals:**
  - Novisto acquired Minimum on 31 Mar 2026. — [ESG Today](https://www.esgtoday.com/novisto-acquires-carbon-accounting-software-provider-minimum/)
  - XeleratedFifty acquired Terrascope (Feb/Mar 2026). — [Sustainable Tech Partner M&A list](https://sustainabletechpartner.com/news/ma-list-whos-buying-carbon-accounting-and-sustainability-software-companies/)
  - Dcycle acquired ESG-X (Feb 2026). — [Sustainable Tech Partner M&A list](https://sustainabletechpartner.com/news/ma-list-whos-buying-carbon-accounting-and-sustainability-software-companies/)
  - Tracxn counts 3 carbon-accounting acquisitions through Mar 2026 and 5 in 2025. — [Tracxn](https://tracxn.com/d/sectors/carbon-accounting/__mFkGD1tJjaPu6-9HXIdMZy_K4xj6xjhNArigYisTRH4)
- Sustain.life was acquired by Workiva (date not given) and reportedly lacks CBAM-specific features. — [TSC USA blog (competitor-authored)](https://www.thesustainabilitycloud.com/blog/best-cbam-software-in-the-usa-2026/)
- **Possible CBAM-only exit:** an Acquire.com listing titled "EU CBAM Compliance SaaS — Mandatory Regulation, 100K+ Importers Need This Software". The page content could not be fetched, so no price, revenue or date was captured. Its "100K+ importers" pitch predates or ignores the Omnibus cut. — [Acquire.com listing](https://app.acquire.com/startup/4bnb0a1vfg-eu-cbam-compliance-saas-mandatory-regulation-100k-importers-need-this-software)
- **Pivot or retreat:** Coolset's CBAM product page redirected to its homepage by Jul 2026, status unclear. — [cbamguide](https://cbamguide.com/software/best-cbam-software/)
- **Incumbent entry:** SAP entered the market in Jun 2026, partly "coming soon". This increases enterprise competition. — [SAP News](https://news.sap.com/2026/06/sap-introduces-cbam-declarants-solution/)

### Inferences
- After the Omnibus, the importer market is about 10% of its former size by count but holds the bulk of the money. Remaining importers are larger and served by enterprise vendors (CarbonChain, osapiens, SAP, IntegrityNext). Self-serve SMB importer tools (CbamTrack, CBAM Pulse) look exposed.
- The **number of non-EU producers did not shrink**. They still face verification demands from the remaining large importers, so producer-side demand is more resilient than importer-side SMB demand.
- The general carbon-accounting market is consolidating. Generalists are unlikely to build deep producer-side CBAM for emerging markets soon.

### Gaps
- No confirmed shutdown or acquisition of a CBAM-only vendor (CBAMBOO, kolum, Dubrink, CarbonChain) was found.
- Funding news for CBAM-only startups in 2025-2026 is absent from search results.
- Carbon Pulse, Sifted and TechCrunch coverage was not directly accessed (paywalls and search limits).

## Q5. Evident gaps: Africa producers, ERP-native producer-side ingestion, multilingual (French/Arabic/Portuguese)

### Takeaway
Three gaps stand out:
1. **Sub-Saharan Africa** (South Africa, Mozambique, Egypt as a base, Kenya, Nigeria) has no dedicated CBAM software. Only consultancies, certifiers and foreign SEO pages serve it.
2. **ERP-native producer-side ingestion** is not offered. Producer tools use manual or bulk upload, project-based integrations or "send us your bills" services. SAP's ERP-native offering is declarant-side and partly unreleased.
3. **Arabic and Portuguese** support is rare. Only virESG offers French and Arabic (Maghreb only). Dubrink's Portuguese and French support is importer-side.

A verifier-grade audit trail aligned with the new O3CI verifier workflow (Aug 2026) is claimed loosely ("verification-ready") but rarely specified.

### Cited Findings
- **Producer-side ingestion:**
  - Sustrack: data entry through the UI or bulk upload, with system connections only "project-by-project". — [Sustrack](https://sustrack.ai/products/s-cbam)
  - CarbonSettle: exporters share electricity bills, fuel invoices and production logs as a managed service. — [CarbonSettle](https://carbonsettle.com/cbam-steel-exporters-india)
  - CarbonChain's installation offering does not mention ERP integration. — [CarbonChain](https://www.carbonchain.com/cbam)
- **SAP:** its CBAM solution is for declarants, with operator support "later". Supplier data arrives as Excel uploads. — [SAP News](https://news.sap.com/2026/06/sap-introduces-cbam-declarants-solution/)
- **Siemens SiGREEN:** an SAP ERP connection is offered via an NTT DATA accelerator (PCF-focused, aimed at large enterprises). — [NTT DATA](https://nttdata-solutions.com/us/blog/empowering-green-futures-with-sap-sigreen/)
- **Language support:**
  - virESG: English, French and Arabic UI and reports, with Moroccan grid factors and ONEE data integration. — [virESG](https://viresg.com/en/cbam-morocco)
  - Dubrink: 15 EU languages, including French and Portuguese, but no Arabic. — [Dubrink](https://www.dubrink.com/cbam-compliance-for-importers)
  - kolum: supplier requests in 20+ languages, per cbamguide. — [cbamguide](https://cbamguide.com/software/best-cbam-software/)
  - Sustrack: Turkish and English only. — [Sustrack](https://sustrack.ai/products/s-cbam)
- **Africa:** no South African, Kenyan or Nigerian CBAM software startup was found. Only services from TÜV Rheinland SA, SCS and Anthesis. — [TÜV SA](https://www.tuv.com/south-africa/en/lp/cbam-and-environmental-services/); [SCS Africa](https://www.scsglobalservices.com/africa/services/carbon-border-adjustment-mechanism-cbam); [Anthesis ZA](https://www.anthesisgroup.com/za/regulations/carbon-border-adjustment-mechanism-regulations-cbam/)
- **South Africa carbon tax:** the Carbon Tax Act (2019) means a carbon price may be deductible under Article 9 (status: potentially eligible, pending). Egypt and Morocco have no carbon pricing scheme. Software would need to handle carbon price paid as evidence. — [cbamguide countries](https://cbamguide.com/countries/)
- **Verification evidence:** a guidance summary says the verification file must preserve:
  - the production boundary
  - fuel and electricity records
  - input materials and output volumes
  - process emissions and allocation choices
  - default values used
  - carbon price paid in the third country

  This defines what an "audit trail" must hold. — [SCS Global blog](https://www.scsglobalservices.com/blog/what-eu-importers-and-non-eu-manufacturers-need-to-understand-about-cbam-verification)
- **Verifier workflow:** a verifier report is issued by an accredited verifier, not by software. Verifier registration in O3CI opened around late Aug 2026. — [EC CBAM Registry](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry_en); [Kohen Avocats](https://kohenavocats.com/en/eu-cbam-verification-guidance-french-importers-non-eu-producers-september-2026/)
- **AI:** no vendor documents LLM or agentic features specific to CBAM.
  - Generic "AI-based" or "AI-supported" claims come from CleanCarbon.ai and CASEM; Sinai and Assent are tagged "AI-powered" in third-party articles.
  - Microsoft's "EU CBAM Copilot" is an archived fee estimator.
  - A search for AI-agent CBAM startups in 2026 found none.
  — [AlCircle](https://www.alcircle.com/news/cleancarbon-ai-simplifying-cbam-compliance-for-indian-aluminium-and-steel-exporters-111492); [CASEM](https://www.casem.com.tr/cbam-skdm-yazilimi/); [Microsoft Learn](https://learn.microsoft.com/en-us/industry/release-plan/2024wave2/cloud-sustainability/estimate-carbon-fee-eu-cbam-copilot)
- **Cost of verification:** virESG claims local verifiers cost 40-50% less than flying in EU verifiers. A local verifier network is therefore a cost differentiator in Africa. — [virESG](https://viresg.com/en/cbam-morocco)

### Inferences
- carbonTraceAI's wedge appears open: producer-side, ERP-native ingestion (for example ERPNext and Sage, common among emerging-market mid-caps), an O3CI-ready output, a verifier-grade evidence trail, French, Arabic and Portuguese, and Sub-Saharan plus North African coverage.
- **Nearest threats:**
  - virESG, which could expand south.
  - The Sustainability Cloud (Indian, low-cost, SEO-heavy across African countries).
  - CarbonChain's installation product and supplier catalogue, which could reach producers through their importers.
  - Importer-paid supplier portals (osapiens, CBAMBOO), which push producers into the importer's tool for free.
- **Competitive risk:** importer portals make the supplier side free, and Indian vendors compete on managed-service price. A producer-side SaaS must show a cost saving (actual versus default values) and verifier acceptance, not just software features.

### Gaps
- No independent evidence (reviews, verifier statements) that any vendor's XML or "verification-ready" outputs were accepted by NCAs or verifiers.
- No data on how many African installations have registered in O3CI.
- Not verified whether Sage, Odoo, ERPNext or SAP Business One have any CBAM plugins in the market. Not searched within the tool budget.
- No pricing benchmarks for producer-side SaaS outside India, so a willingness-to-pay estimate for African producers is not grounded.
