# Scope 3 Supplier Data Exchange, Product Carbon Footprints and Decarbonisation Action: Opportunities for an Agentic-AI Carbon Startup (as of Oct 2026)

Research note scope: supplier-side data exchange, PCFs/EPDs, and decarbonisation execution. Carbon accounting platforms (Watershed, Sweep, Persefoni, Greenly/Normative) are covered in earlier reports in `reports/` and are not repeated here. About 22 search/fetch calls were made. Many findings come from vendor or secondary sources; caveats are noted inline.

## 1. Data exchange standards and networks: how many suppliers get requests, and how well do SMEs respond?

### Takeaway
Supplier data requests now come through overlapping channels: CDP Supply Chain (about 45,000 suppliers requested in 2025), EcoVadis (100k to 150k+ suppliers claimed), PACT (48+ software implementers), Catena-X (now part of OEM procurement) and TfS/SiGREEN. These channels are consolidating fast. Makersite bought SiGREEN in April 2026, and EcoVadis is connecting to Workiva and CO2 AI. Response quality from SMEs is still weak. The best available proxy is that about 10,900 SMEs disclosed via CDP against about 45,000 suppliers requested. The interoperability layer (PACT, Catena-X, TfS) is a standards play, and the remaining opening is the supplier-side "answer once, publish everywhere" step.

### Cited Findings
**WBCSD PACT (formerly Pathfinder)**
- PACT Methodology V3 is a harmonised cradle-to-gate PCF framework with new coverage of land-sector emissions, electricity accounting and service businesses. V2 is withdrawn, but V2 PCFs computed before V3 stay valid for three years. The WBCSD page gives conflicting dates: a June 2, 2026 publication date and a 30 April 2025 release. — [WBCSD PACT Methodology V3](https://www.wbcsd.org/resources/pact-methodology-version-3/)
- More than 48 software providers implement the PACT Technical Specifications. 5,000+ companies reportedly use PACT-conformant methods, and the network has "supported millions of PCFs" (undated aggregator figures, unverified). — [Net Zero Compare](https://netzerocompare.com/policies/pact-methodology)
- Conformance is voluntary and is tested at monthly "Connectathons". WBCSD encourages listing in the PACT Online Catalog whatever the conformance status. — [PACT Conformance Testing deck, SINE Foundation](https://pidx.org/wp-content/uploads/2024/11/PACT-Conformance-Testing-Process-Overview-Prasad-Tilloo-Technical-Project-Manager-SINE-Foundation.pptx.pdf)
- Conformant examples include Dassault Systèmes 3DEXPERIENCE (Oct 2024) and Fujitsu ESG Management Platform (Nov 2024). — [Digital Engineering 24/7](https://www.digitalengineering247.com/article/dassault-systemes-3dexperience-platform-recognized-as-pact-conformant/news); [WBCSD Fujitsu case](https://www.wbcsd.org/news/a-journey-of-change-how-fujitsu-uses-pact-to-partner-with-suppliers-and-drive-value-chain-decarbonization/)
- Makersite documents a PACT network connection setup. — [Makersite support: PACT configuration](https://support.makersite.io/network-connections/pact-configuration)

**Catena-X (automotive)**
- Catena-X PCF Rulebook v4 was published in September 2025. ISO 14067 plus Catena-X metrics become mandatory for exchange after a transition phase that ends in 2027. A Data Quality Rating (DQR) becomes mandatory from end-2027. — [Tanso blog](https://www.tanso.de/en/blog/what-is-catena-x-and-why-do-automotive-suppliers-need-to-act-now); [Tanso ISO 14067 checklist](https://www.tanso.de/en/blog/from-iso-14067-to-catena-x-pcfs)
- Since April 2025, Catena-X registration has been an official part of BMW's procurement process, and VW, Mercedes-Benz and Ford are reportedly following (vendor blog, not confirmed with OEMs). — [Tanso blog](https://www.tanso.de/en/blog/what-is-catena-x-and-why-do-automotive-suppliers-need-to-act-now)
- In a multi-tier pilot, Ford (OEM), Flex (Tier 1) and Micron (Tier 2) exchange primary PCF data. Micron sends to Flex, which enriches the data and passes it to Ford. — [Catena-X success story](https://catena-x.net/success-stories/how-ford-oem-flex-tier1-and-micron-tier2-lower-costs-and-reduce-emissions-with-pcf-reporting/)
- Flex's pilot reached Level 2 certification under the Catena-X/TfS PCF Verification and Program Certification Framework v2.0, which shows TfS and Catena-X now share a verification scheme. — [Flex](https://flex.com/resources/flex-pilots-catena-x-based-data-exchange-for-global-automakers)
- In July 2026 the first Asian multi-company PCF exchange ran on Cofinity-X, involving KG Mobility, LG Electronics VS and several Korean suppliers. — [Cofinity-X](https://www.cofinity-x.com/blog/asias-first-multi-tier-pcf-data-exchange-runs-on-cofinity-x-infrastructure)
- LG notes that many suppliers "still lack the systems, experience or internal standards" to manage and exchange product-level carbon data. — [LG Electronics](https://www.lg.com/global/business/insights/mobility/blog/20260605-lg-catena-x-pcf-declaration/)

**TfS (chemicals) and Siemens SiGREEN/Estainium**
- The TfS PCF Exchange runs on SiGREEN. — [TfS PCF exchange solution](https://www.tfs-initiative.com/pcf-exchange-solution)
- Makersite acquired SiGREEN from Siemens (announced 14 April 2026, effective 1 June 2026). The companies claim SiGREEN is the only platform natively connecting TfS, Catena-X and PACT. No user or supplier counts were disclosed. — [ESG Today](https://www.esgtoday.com/makersite-acquires-product-carbon-footprint-platform-sigreen-from-siemens/); [Makersite press](https://makersite.io/press/makersite-acquires-sigreen/)
- SiGREEN has reportedly been renamed "MatterMaps" (single third-party directory, unconfirmed). — [KI-Syndikat](https://www.ki-syndikat.de/tools/mattermaps/)
- Siemens started the open, cross-industry Estainium network for trustworthy PCF exchange. — [Supply Chain Digital](https://supplychaindigital.com/sustainability/siemens-tool-exchange-supply-chain-emission-data)

**EcoVadis**
- EcoVadis launched a Carbon Data Network in 2025 as a verified supplier primary-data exchange. Its PCF Data Exchange uses PACT, and it offers a free supplier PCF Calculator, now inside Carbon Action Manager, which it says reaches 150,000+ suppliers. The 2023 launch cited 100,000. — [EcoVadis PCF Calculator](https://ecovadis.com/solutions/pcf-calculator/); [EcoVadis 2023 release](https://www.businesswire.com/news/home/20230926785949/en/EcoVadis-Unveils-Product-Carbon-Footprint-Data-Exchange-to-Transform-Collaborative-Decarbonization-Efforts-Across-the-Value-Chain); [Net Zero Compare CAM](https://netzerocompare.com/software/ecovadis-carbon-action-manager)
- EcoVadis expanded its Carbon Data Network to Workiva in May 2026. In September 2026 it partnered with CO2 AI so that supplier corporate data and PCFs collected in EcoVadis flow straight into CO2 AI. — [PR Newswire Workiva](https://www.prnewswire.com/news-releases/ecovadis-continues-expansion-of-carbon-data-network-with-workiva-302769118.html); [PR Newswire CO2 AI](https://www.prnewswire.com/news-releases/ecovadis-and-co2-ai-partner-to-advance-scope-3-transparency-with-primary-data-precision-302868501.html)

**CDP Supply Chain: volume and response**
- In 2025, 270+ buyers requested data from about 45,000 suppliers through CDP Supply Chain. — [ESG Today](https://www.esgtoday.com/cdp-reports-70-jump-in-companies-receiving-top-sustainability-reporting-scores/)
- In 2025, 23,100+ organisations disclosed through CDP, including 10,900+ SMEs using the dedicated SME questionnaire. — [CDP Why Disclose](https://www.cdp.net/en/disclose/why-disclose)
- Requested suppliers who do not respond are marked "Did not disclose", which is visible to the customer. Responding is not legally required. — [CSRD Pro SME guide](https://www.csrdpro.com/en/cdp-supply-chain-request-sme-guide/)
- Sources disagree on SME questionnaire eligibility. A third party says ≤1,000 employees and ≤US$250m revenue, while CDP's June 2025 webinar recommends <500 employees and <US$250m. — [CSRD Pro](https://www.csrdpro.com/en/cdp-supply-chain-request-sme-guide/); [CDP SME webinar June 2025](https://assets.ctfassets.net/v7uy4j80khf8/2o6jX1NDKjkcPNhEJRuNKb/6cd79cc12031dd8feed74eb423436c5e/SC_Supplier_Series_SME_Questionnaire_24_June_APAC_.pdf)
- Historical response rates were about 51% (4,005 of 7,879) in a 2016-era report and 27% (634 of 2,318) in an earlier year. A 2018 single-buyer example gave 85% against a peer average of 47%. — [3BL Media](https://back.3blmedia.com/node/5566); [SDCExec](https://www.sdcexec.com/safety-security/risk-compliance/press-release/12163757/cdp-cdp-report-finds-companies-blind-to-climate-risks-in-half-of-their-supply-chains)
- Practitioner view: a direct request from a category manager through an existing relationship "will consistently outperform an automated survey from an unfamiliar platform". — [Terrnix 2026](https://terrnix.com/sustainability-intelligence/2026/06/scope-3-supplier-engagement-2026/)

### Inferences
- The networks are becoming interoperable. PACT is the common API and data model, Catena-X and TfS are sector rulebooks, and SiGREEN/Makersite and EcoVadis are the aggregation hubs. A new "network" would be a weak play. Being a conformant node (PACT plus Catena-X EDC connector) that does the supplier-side work is the stronger one.
- 10,900 SME disclosers against about 45,000 requests is not a true response rate. It still suggests that well over half of requested suppliers either do not respond at all or respond with low-quality, spend-based data.
- Consolidation matters for go-to-market. Makersite now owns the PCF calculation tool (LCA) and a leading exchange (SiGREEN), and EcoVadis is wiring its supplier base into accounting platforms (Workiva, CO2 AI). Incumbents are capturing the buyer side. The underserved segment is suppliers that hold 5 to 50 different buyer requests and have no LCA staff.

### Gaps
- No official 2025 CDP Supply Chain response rate was found. CDP's annual supply chain report was not retrieved.
- No current count of PACT-conformant solutions (as opposed to implementers) or PCFs exchanged in 2026 was found. The PACT Online Catalog was not fetched.
- No 2025-26 data was found for SAP Sustainability Data Exchange (SDX) or Manufacture 2030 (supplier counts, PACT status, pricing).
- No current TfS PCF Guideline version or TfS member PCF volume was retrieved.
- No source gave the number of distinct buyer requests a typical SME supplier receives.

## 2. PCF / LCA / EPD automation players and regulatory drivers (ISO 14067, PEF, EU Battery Regulation, steel/aluminium, construction EPDs)

### Takeaway
Funding is concentrating in a few PCF/LCA platforms. Makersite raised €60m in its Series B (Jul 2025) and then bought SiGREEN. Carbonfact raised a $15m Series A for fashion (2024). Most other players (Carbon Maps, CarbonBright and similar) are small seed-stage companies. On regulation, the EU Battery Regulation carbon-footprint delegated act was still not adopted as of late September 2026, so a hard deadline has slipped. Catena-X makes ISO 14067 PCFs effectively mandatory in automotive by end-2027. In construction, EPD "generators" from One Click LCA and EPD Hub already claim to cut EPD preparation costs to less than one-tenth of traditional costs, which makes that a crowded niche.

### Cited Findings
**PCF/LCA automation players**
- Makersite (Stuttgart) raised a €60m Series B in July 2025, co-led by Lightrock and Partech with SE Ventures. Reported total funding ranges from €78.3m to €85m depending on the source. Its product is an AI/graph-based product digital twin. Vendor claims: Microsoft cut the Surface Pro 10 footprint by up to 28% in two years, and Schneider Electric is deploying it across 200,000+ SKUs. — [Tech.eu](https://tech.eu/2025/07/22/makersite-raises-eur60m-to-boost-product-development-with-ai-lifecycle-tools/); [Verdantix](https://verdantix.com/vantage/blog/makersite-secures-60-million-for-ai-driven-product-lifecycle-intelligence); [Pulse 2.0](https://pulse2.com/makersite-e60-million-raised-for-product-lifecycle-intelligence-platform)
- Siemens Teamcenter integrated Makersite for LCA, which embeds PCFs in PLM. — [Makersite](https://makersite.io/?p=8647)
- Carbonfact (fashion) raised a $15m Series A in April 2024 (Alven, Headline) and claims 150+ apparel and footwear brands onboarded. Tracxn reports $17.1m total over 4 rounds. — [ESG Today](https://www.esgtoday.com/carbonfact-raises-15-million-for-emissions-reporting-solution-for-fashion-industry/); [Tracxn](https://tracxn.com/d/companies/carbonfact/__V_DZ0h8o0WnVWMTX0EUDWTLSU-HGncMBgizxP8LuNUc)
- Carbon Maps (Paris, food and beverage) raised a $3.2m seed led by Daphni (Dec 2023) after a $4.3m pre-seed. CB Insights puts the total at $9.43m. Its 2026 blog targets SBTi V2 Scope 3 requirements for food companies. — [Crustdata](https://profiles.crustdata.com/company/carbon-maps); [CB Insights](https://www.cbinsights.com/company/carbon-maps); [Carbon Maps blog](https://www.carbonmaps.io/blog/sbti-net-zero-v2-new-scope-3-requirements-for-food-companies)
- CarbonBright (London, founded 2022) shows only $20k of Techstars funding on Tracxn. — [Tracxn](https://tracxn.com/d/companies/carbonbright/__96goScvuAGgW7MWNbr4J7IZOzM-Jdmf5XPBVGiqhVyo)

**EU Battery Regulation**
- The carbon-footprint methodology delegated act was due by February 2025 and had not been adopted as of 26 September 2026. It was reportedly stuck on a political decision about how electricity is modelled. — [Traceable Digital](https://traceable.digital/resources/blog/battery-carbon-footprint-declaration-deadline-not-started/); [Cleo Labs](https://www.cleolabs.co/en/blog/eu-battery-carbon-footprint-class-2026)
- The EV battery declaration now applies 12 months after the delegated act enters into force (per SGS, via secondary source). Commission guidance of 15 Aug 2026 reportedly treats the carbon-footprint fields of the battery passport as "not to be filled/displayed as of February 2027". The battery passport itself is still due 18 Feb 2027. — [Insum Energy](https://www.insumenergy.com/eu-battery-carbon-footprint-declaration-2026-guide/); [Environment+Energy Leader](https://environmentenergyleader.com/stories/battery-passport-becomes-mandatory-february-18-2027,142747)
- JRC published draft rules for industrial-battery carbon footprints (CFB-IND) in April 2025. — [Cleo Labs](https://www.cleolabs.co/en/blog/eu-battery-carbon-footprint-class-2026)

**Construction EPDs**
- One Click LCA EPD generators cover concrete, luminaires, pre-verified EPDs and others. Pricing is custom and needs a demo. The vendor claims costs are "over 10 times lower than standard EPD prices" and "below one tenth of traditional costs". — [One Click LCA Concrete EPD Generator](https://oneclicklca.com/software/manufacturing/concrete-epd-generator); [One Click LCA pricing](https://oneclicklca.com/pricing/product-lca-and-epd-pricing); [Toolradar](https://toolradar.com/tools/oneclicklca)
- EPD cost breakdown (study cited by One Click LCA): 51% LCA and EPD preparation, 29% verification, 20% publishing and registration. Automation addresses only the first slice. — [One Click LCA software overview](https://oneclicklca.com/en/resources/articles/top-epd-software-overview)
- One Click LCA's integration with EPD Hub claims verification in as little as two weeks, and an HVAC EPD tool is "coming soon" (Aug 2026). — [One Click LCA what's new Aug 2026](https://help.oneclicklca.com/en/articles/796024-what-s-new-in-one-click-lca-in-august-2026)
- One Click LCA maintains a country-by-country guide to EPD requirements. — [One Click LCA](https://oneclicklca.com/en/resources/articles/guide-to-global-epd-requirements-by-country)

**ISO 14067 in practice**
- Vendor guidance treats ISO 14067 as the base standard and layers on PACT, Catena-X and verification. Third-party PCF verification is an emerging requirement. — [ASUENE ISO 14067 guide](https://asuene.com/uk/blog/product-carbon-footprint-under-iso-14067-2026-compliance-guide); [Projet Celsius PCF verification](https://projetcelsius.com/en/blog/product-carbon-footprint-verification/)

### Inferences
- PCF demand that is actually enforced in 2026-27 comes from buyer procurement rules: Catena-X/BMW registration, TfS in chemicals, and CBAM-adjacent steel and aluminium. Regulation is lagging (the Battery Regulation act has slipped). A startup should sell into buyer-mandated supplier PCFs rather than wait on EU timelines.
- In construction EPDs, One Click LCA and EPD Hub already combine generator, verification and publishing, so a newcomer has little room in Europe. Verification (29%) and publishing (20%) are fixed costs that an AI agent cannot remove.
- Funding is thin outside Makersite and Carbonfact. That suggests either limited VC appetite for vertical PCF tools or a market where each vertical supports only one or two winners.

### Gaps
- No 2025-26 funding or traction data was found for Sustamize, Ecochain, Dayrize, Vaayu, Altruistiq, Tracemission, 2050 Materials or EPD Hub. These names were not searched individually because of the call budget.
- PEF/PEFCR status (Green Claims Directive withdrawal and its effect on PEF) was not researched.
- ResponsibleSteel and ASI certification volumes, green-steel and green-aluminium premium levels, and US Buy Clean / EU CPR EPD mandates in 2026 were not researched.
- No independent price benchmark per PCF or per EPD (traditional or automated) was found.

## 3. Decarbonisation execution: abatement planning, energy procurement, PPAs, fuel switching, and agentic "measure to action" products

### Takeaway
No credible 2026 agentic product closing the loop from measurement to verified abatement turned up in these searches. PwC reports that 60% of companies use AI for operational decarbonisation but fewer than 1% have quantified reductions. PPA marketplaces (LevelTen with 8+ GW facilitated, Edison, Reel, Zeigo) are mature, but corporate PPA volumes fell 19% in the US and Europe in 2025, and 2026 growth is driven by hyperscalers rather than the mid-market. Execution agents are an open but unproven space, and "evidence of reductions" is the weakest link across the market.

### Cited Findings
- 60% of companies use AI for operational decarbonisation, but fewer than 1% have quantified emissions reductions. Contracted PPA volume in the US and Europe fell 19% and deal count fell 26% in 2025, and the 2026 uptick is driven almost entirely by data centres. The page's dating is uncertain (it carries an older age stamp but cites 2025 data). — [PwC State of Decarbonization](https://www.pwc.com/us/en/services/esg/library/decarbonization-strategic-plan.html)
- LevelTen runs marketplaces for PPAs, projects and tax-credit transfers, has facilitated 8+ GW, and offers automated RFP creation and bid comparison. Verdantix names competitors Edison Energy, Reel Energy and Zeigo Power. Buyer aggregation is the stated route to mid-market access (third-party description). — [Verdantix on LevelTen Series D](https://www.verdantix.com/client-portal/blog/levelten-energy-raises-65-million-dollars-in-series-d-funding-to-fuel-growth-in-new-regions); [SoftwareOne listing](https://platform.softwareone.com/product/levelten-energy/PCP-9527-0829)
- LevelTen's index showed North American solar PPA prices up about 3.2% in Q4 2025, while European prices fell for a third straight quarter (down 1% year on year). — [Techleap / LevelTen profile](https://finder.techleap.nl/companies/levelten_energy)
- Hyperscaler deals dominate. Google and TotalEnergies signed a 15-year, 1 GW solar PPA (Feb 2026), and Meta and Vistra agreed up to 6.6 GW of nuclear. — [EnkiAI](https://enkiai.com/solar/gigawatt-ppas-how-ai-redefined-hyperscaler-energy-in-2026/)
- Adjacent agents: Metris Renewables AI automates clean-power asset operations, not buyer-side abatement. Coupa is launching autonomous sourcing agents in source-to-pay, a possible channel for embedding carbon criteria. — [AI Agent Store news](https://aiagentstore.ai/ai-agent-news/topic/startups); [PR Newswire Coupa](https://www.prnewswire.com/news-releases/coupa-launches-new-ai-agents-to-accelerate-source-to-pay-roi-featuring-autonomous-sourcing-collaboration-and-orchestration-302618137.html)
- Makersite's Surface Pro 10 claim (up to 28% footprint cut in two years) is one of the few named reduction outcomes, and it is a vendor claim. — [Pulse 2.0](https://pulse2.com/makersite-e60-million-raised-for-product-lifecycle-intelligence-platform)

### Inferences
- Measurement vendors talk about "action", but the evidence of delivered reductions is close to nil. An agent that turns utility, meter and ERP data into ranked, costed abatement projects (a MACC) and then tracks realised savings against baselines would differentiate on evidence. The deterministic calculation engine and provenance trail suit this well.
- In emerging markets, the decarbonisation lever is usually on-site solar or captive and open-access renewables, boiler fuel switching and efficiency, not virtual PPAs. US/EU PPA marketplaces do not serve this segment.

### Gaps
- Pexapark's 2026 products and any AI-agent features from LevelTen or Pexapark were not found.
- No data was found on abatement-planning tools (Carbon Trust tools, Normative's reduction module, MACC software) or on industrial heat and fuel-switch advisory platforms.
- No independent evidence was found of measured reductions from any agentic decarbonisation product.

## 4. GHG Protocol, ISO and SBTi revision timing: windows that force tool changes

### Takeaway
Three revision cycles overlap. (1) Scope 2: consultation ran from Oct 2025 to 31 Jan 2026 and drew strong pushback on hourly matching, with only 12% of companies in support. (2) Consolidated GHG Protocol + ISO 14064-1 corporate standard (partnership announced Sep 2025): an integrated consultation is reportedly planned for Q2 2027, with finalisation likely in 2027-28, and existing standards stay in force until then. (3) SBTi Corporate Net-Zero Standard V2.0, published 11 June 2026 with validation from early 2027, which adds supplier/customer alignment targets as a Scope 3 route. The SBTi window is the nearest forced change, and it directly creates demand for supplier engagement tracking.

### Cited Findings
**GHG Protocol / ISO**
- In September 2025, GHG Protocol and ISO announced a partnership to co-develop a consolidated corporate standard harmonising Scope 1, 2 and 3, AMI and ISO 14064-1. — [GHG Protocol FAQ](https://ghgprotocol.org/blog/iso-ghg-protocol-partnership-frequently-asked-questions); [Verdantix](https://www.verdantix.com/insights/blog/one-standard-to-rule-them-all--what-the-ghg-protocol-iso-unification-means-for-organizations-and-carbon-management-software)
- GHG Protocol's official update page sets no publication or effective dates. Transition periods will be decided "over the coming months", existing standards remain in effect, and readers are directed to a 29 July 2026 press release, FAQ and Standard Development Plan for current status. Those were not retrieved. — [GHG Protocol update process](https://ghgprotocol.org/ghg-protocol-standards-and-guidance-update-process)
- The Scope 2 public consultation opened 20 Oct 2025 and closed 31 Jan 2026 after an extension. — [STX Group](https://stxgroup.com/blogs/ghg-protocol-scope-2-revision-stakeholders-call-for-greater-accuracy-but-not-at-any-cost/)
- Consultation results: on hourly matching, 70% of 909 respondents gave little or no support and 22% were in favour. 76% supported an exemption and 59% opposed the deliverability revision. A public consultation on an integrated corporate standard is planned for Q2 2027. — [Argus Media](https://www.argusmedia.com/en/news-and-insights/latest-market-news/2858486-ghg-protocol-faces-pushback-on-scope-2-reforms)
- Among companies only, 12% support hourly matching, 82% give low or no support, and 84% want it to be optional ("may" rather than "shall"). — [ESG Today](https://www.esgtoday.com/vast-majority-of-companies-oppose-tougher-ghg-protocol-scope-2-reporting-proposals/)
- Secondary sources give conflicting Scope 3 timelines: "final revised versions by 2027", or a draft in mid-2026 with a final in late 2027. One summary says the unified GHG Protocol/ISO format is not expected before 2028. — [Zevero](https://www.zevero.earth/blog/ghg-protocol-scope-3-standard-revision); [Seneca ESG](https://senecaesg.com/insights/ghg-protocol-in-2025-consolidation-coherence-and-the-road-to-a-unified-global-language-for-carbon-accounting); [OneStopESG](https://onestopesg.com/esg-resources/ghg-protocol-scope-2-revision)

**SBTi CNZS V2.0**
- The final standard was published 11 June 2026 (secondary sources). It takes effect around 1 Feb 2027, with formal validation opening in early 2027. — [ESG Today](https://www.esgtoday.com/sbti-releases-finalized-new-corporate-net-zero-standard/); [ClimatePartner](https://www.climatepartner.com/en/knowledge/blog/sbti-net-zero-standard-v2); [Carbon Maps](https://www.carbonmaps.io/blog/sbti-net-zero-standard-v2-0-is-final-what-changed-since-the-november-2025-draft)
- There are three near-term Scope 3 options: an absolute reduction target, supplier/customer alignment targets (a growing share of tier-1 suppliers and customers setting and progressing science-based targets), or category/activity-specific targets. All Scope 3 categories at ≥5% of total must be covered, replacing the 67% rule and capturing more than 90% of Scope 3 by SBTi's estimate. Only Category A companies must set near-term Scope 3 targets. — [OneStopESG](https://onestopesg.com/esg-resources/sbti-corporate-net-zero-standard-v2); [EcoPrism](https://ecoprism.com/resources/insights/sbti-corporate-net-zero-standard-v2-changes); [Patch](https://www.patch.io/downloads/sbti-cnzs-v2-guide-2026)
- Conflict: a file labelled "Net-Zero Standard Version 1.3.1 April 2026" still carries the 67% rule. It is likely the legacy standard, still valid during transition. — [SBTi PDF](https://files.sciencebasedtargets.org/production/files/Net-Zero-Standard.pdf)

### Inferences
- The near-term forced change is the SBTi V2 supplier-alignment pathway (validation in 2027). Buyers choosing it must track which tier-1 suppliers have set and are progressing SBTs, which is a recurring monitoring and chasing workflow that suits agents.
- The heavy opposition makes hourly Scope 2 matching likely to end up optional. Do not build a product thesis on mandatory 24/7 matching before 2028.
- The GHG Protocol + ISO consolidation (2027-28+) will force methodology updates in every calculation engine. A deterministic, versioned factor and method library with provenance is an advantage when rule sets change.

### Gaps
- The 29 July 2026 GHG Protocol press release and Standard Development Plan were not read, so official dates for the Scope 3 and Corporate Standard drafts are unconfirmed.
- SBTi V2 supplier-engagement target thresholds (percentages and dates) were not verified on SBTi's own site.

## 5. Where agents fit: concrete agent tasks and competition density

### Takeaway
The best-defined agent tasks are: (1) a supplier-side "answer once" agent that fills CDP, EcoVadis, PACT, Catena-X and buyer questionnaires from one ERP-derived dataset; (2) PCF generation from ERP plus BOM, with emission-factor matching and a Data Quality Rating, exported in PACT/Catena-X format; (3) buyer-side supplier chasing and SBTi supplier-alignment tracking; and (4) abatement opportunity identification from utility and meter data. The buyer side (3) is crowded with incumbents such as EcoVadis, Makersite/SiGREEN, Gravity, SINAI and Normative. Supplier-side (1)-(2) in emerging markets and verified abatement tracking (4) are the least contested.

### Cited Findings
- Existing buyer-side automation: Gravity automates requests, extracts data from supplier documents with AI and scores data quality. SINAI flags high-impact suppliers and sends pre-filled forms through a no-code portal. Normative automates requests, tracking and validation. — [Gravity](https://www.gravityplatform.com/glossary/supplier-engagement); [SINAI](https://www.sinai.com/post/scope-3-supplier-engagement-manufacturing); [Normative](https://normative.io/insight/scope-3-supplier-engagement/)
- A common practitioner tiering: top-20% suppliers provide product-level PCFs from primary data, and the rest go via CDP or a GHG Protocol-aligned survey. — [Terrnix](https://terrnix.com/sustainability-intelligence/2026/06/scope-3-supplier-engagement-2026/)
- Free supplier tools reduce willingness to pay. EcoVadis offers a free PCF Calculator to its supplier base. — [EcoVadis PCF Calculator](https://ecovadis.com/solutions/pcf-calculator/)
- Catena-X requires ISO 14067 PCFs plus a DQR by end-2027, which is a defined output spec an agent can target. — [Tanso](https://www.tanso.de/en/blog/from-iso-14067-to-catena-x-pcfs)
- No specific "AI agent for Scope 3 supplier engagement" launch in 2026 was found. Search results instead covered procurement agents in general (Coupa) and comparison listicles. — [Rework procurement agents 2026](https://resources.rework.com/tools/ai-agents/best-ai-agents-for-procurement-2026); [EmissionTwin comparison](https://www.emissiontwin.com/blog/scope-3-emissions-data-automation-software/)

### Inferences
- The buyer-side chasing agent conflicts with the finding that relationship-based requests outperform platform surveys, and incumbents own the buyer relationship. A stronger angle is to sit with the supplier, or with the buyer's procurement team in their source-to-pay tools (Coupa, SAP Ariba), rather than in another portal.
- The agent tasks that need deterministic auditability (factor matching, allocation, PCF calculation, CBAM embedded emissions) match carbonTraceAI's existing engine. The LLM layer is best used for document extraction, questionnaire mapping and supplier conversations, not for the numbers.

### Gaps
- No data was found on time and cost per supplier questionnaire or per PCF for SMEs, which would be needed to size the ROI of an "answer once" agent.

## 6. Payers and pricing: who pays, and at what price points?

### Takeaway
The evidence points to buyers paying for the network and request tooling (CDP Supply Chain membership, EcoVadis, Catena-X OEM programmes), suppliers paying to be listed or rated (EcoVadis ratings, Catena-X onboarding), and manufacturers paying for EPDs. Supplier PCF calculators are increasingly free (EcoVadis), which pushes supplier-side pricing down. Hard price points could not be verified in this research window.

### Cited Findings
- EcoVadis gives its PCF Calculator to suppliers free. — [EcoVadis](https://ecovadis.com/solutions/pcf-calculator/)
- One Click LCA EPD pricing is custom (Business, Expert Pack and Power Pack tiers, with unlimited project EPDs in Power Pack) and not public. — [One Click LCA pricing](https://oneclicklca.com/pricing/product-lca-and-epd-pricing); [Toolradar](https://toolradar.com/tools/oneclicklca)
- 29% of EPD cost goes to verifiers and 20% to publishing and registration, which are fixed third-party costs the manufacturer pays. — [One Click LCA](https://oneclicklca.com/en/resources/articles/top-epd-software-overview)
- In automotive, the OEM makes the supplier responsible for Catena-X registration (BMW from April 2025), so the supplier pays to comply. — [Tanso](https://www.tanso.de/en/blog/what-is-catena-x-and-why-do-automotive-suppliers-need-to-act-now)

### Inferences
- Emerging-market suppliers have a weak willingness to pay. It improves only when a buyer mandate is tied to order volume (CBAM pass-through, Catena-X registration) or when the buyer subsidises the tool. A buyer-sponsored, supplier-used model (the buyer pays per onboarded supplier) is probably the most workable for African and Indian suppliers.

### Gaps
- Price points for CDP Supply Chain membership, EcoVadis supplier subscriptions, Catena-X/Cofinity-X onboarding, PCF software (Makersite, Carbonfact, Carbon Maps) and per-EPD fees were not found in this research window. They need direct vendor pricing pages or analyst reports (Verdantix).

## 7. Emerging-market supplier angle (African, Indian and Southeast Asian suppliers to EU/US/Japanese buyers)

### Takeaway
Pressure on emerging-market suppliers is rising through CBAM (definitive regime from Jan 2026), EU buyer contract clauses and OEM networks (Catena-X expanding into Korea). Domestic systems (India's draft carbon market, Vietnam's narrow pilot) give suppliers little verified data to reuse, so buyers will need primary supplier data. Evidence on capability is mostly advisory-firm estimates, not surveys.

### Cited Findings
- European buyers are negotiating carbon costs alongside Indian steel quotes and seeking clauses that pass CBAM costs back to mills. — [SMM](https://news.metal.com/newscontent/104160201-smm-analysis-cbam-costs-and-emissions-data-reshape-european-procurement-of-indian-steel)
- ICRIER (June 2026) estimates Indian iron and steel exports to the EU could fall 23.94% at $86.01/tCO2. — [Down To Earth](https://www.downtoearth.org.in/economy/eus-carbon-rules-enter-implementation-phase-putting-indian-msmes-under-pressure)
- Up to 70% of Indian exporters to the EU are "unprepared" (unverified consultancy estimate). — [Clearhead Consultants](https://clearheadconsultants.com/eu-sustainability-standards-for-indian-exporters/)
- India's carbon market is largely still in draft, so buyers should expect to commission primary supplier data. Vietnam's 2025-26 pilot ETS covers only 34 thermal power plants, 25 steel facilities and 51 cement plants. — [Mind Trust](https://www.mind-trust.co/insights/supplier-carbon-data-china-vietnam-india/)
- Vietnamese SME guidance says export emissions data must now be verified by an accredited third party, not just self-declared. — [Stivina](https://stivina.com/en/moving-toward-green-exports-checklist-that-vietnamese-smes-need-to-be-aware-of-before-january-2026)
- European buyers now expect African exporters to deliver data sets "comparable to a carbon footprint", driven by CBAM and EUDR. — [Capmad](https://www.capmad.com/post/cbam-and-eudr-why-european-buyers-now-demand-carbon-footprints-from-african-exporters)
- Catena-X's first Asian multi-tier PCF exchange (Korea, July 2026) shows OEM networks extending to Asian tiers. — [Cofinity-X](https://www.cofinity-x.com/blog/asias-first-multi-tier-pcf-data-exchange-runs-on-cofinity-x-infrastructure)

### Inferences
- The overlap of CBAM embedded-emissions data and PCF data (same plant-level energy and material inputs) is a natural wedge for carbonTraceAI. One ERP-linked plant dataset can yield CBAM reports, a PACT/Catena-X-format PCF and CDP/EcoVadis answers. That is the "answer once" agent aimed at suppliers no incumbent targets.
- Third-party verification is becoming a requirement (Vietnam guidance, Catena-X/TfS certification levels). An immutable provenance and audit trail lowers verification cost, which is where the residual cost sits.

### Gaps
- No rigorous 2025-26 survey (EC, GIZ, UNCTAD, ITC) of emerging-market SME supplier carbon-data capability or response rates was found.
- No data was found on Japanese buyer programmes (for example the GX League or Japanese OEM supplier requests) targeting Southeast Asian suppliers.
- African evidence is especially thin. One figure (South African steel and aluminium CBAM exposure of about 6% of EU volumes, about €1.2bn per year) came from an unsourced search summary and is not included as a cited finding.
