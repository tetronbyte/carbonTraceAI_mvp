# Carbon-related finance (banks, insurers, investors, DFIs, trade finance) as a channel for an agentic-AI carbon startup — status as of Oct 2026

Scope note: research done 21 Oct 2026, about 40 search and fetch calls. Several primary regulator pages (ECB, EBA, RBI, CBE) and some vendor pages could not be fetched (403/429). Where a finding rests only on a secondary summary (law firm, consultancy, trade press), the note says so. The prior report's hypothesis was that "banks [will be] paying for verified emissions data from borrowers" (scored 8/12, no demand evidence). The verdict on it is in the last section.

## 1. Regulatory drivers in 2026: is borrower-level carbon data mandatory?

### Takeaway
Supervision is real and enforced in the EU. The ECB has fined two banks over climate-risk materiality failures, and the EBA ESG-risk guidelines have applied since Jan 2026. But the disclosure layer has been cut back in 2025-26: the GAR and BTAR templates were dropped, the Basel framework is voluntary, the IFRS S2 financed-emissions relief applies from 2027, CSRD scope was cut and NZBA closed. As a result, the pull on banks is mainly *risk management of counterparties* (transition plans, materiality, CBAM exposure), not *precise financed-emissions numbers*. In emerging markets, rules are arriving (South Africa, Kenya, Egypt, India, Singapore), but most are guidance or phased, with mandatory metrics in 2027-2029.

### Cited Findings
**EU / ECB / EBA**
- First published ECB climate penalty: in Nov 2025 the ECB imposed periodic penalty payments of €187,650 on ABANCA. The bank missed the deadline for a climate and environmental (C&E) materiality assessment on 65 days in 2024. Amounts are set by materiality, duration and daily turnover — [ECB/Banque de France press release](https://www.banque-france.fr/en/press-release/ecb-imposes-periodic-penalty-payments-abanca-failing-sufficiently-identify-climate-risks); [ECB PR 10 Nov 2025](https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/ssm.pr251110~3e0b6f579e.da.html)
- Second penalty: in Feb 2026 the ECB fined Crédit Agricole €7.55m for missing a C&E materiality-assessment deadline by 75 days in 2024 — [CeFPro](https://connect.cefpro.com/article/view/ecb-imposes-climate-risk-fine-on-crdit-agricole); [Mishcon de Reya](https://www.mishcon.com/news/ecb-fines-crdit-agricole-over-climate-risk-failures-what-happened-why-it-matters-and-what-comes-next); [ECB PR 13 Feb 2026](https://www.bankingsupervision.europa.eu/press/pr/date/2026/html/ssm.pr260213~d0ac373293.ga.html)
- The ECB's 2026-2028 supervisory priorities include resilience to climate risk alongside geopolitical and ICT risk — [A&L Goodbody](https://www.algoodbody.com/insights-publications/ecb-supervisory-priorities-for-2026-2028-focus-on-resilience-to-geopolitical-climate-and-ict-risks); [Jones Day](https://trendingnowinesg.jonesday.com/post/102m1yz/ecb-climate-related-enforcement-legal-and-supervisory-implications-for-the-2026)
- Note: both fines concern *process* failures (materiality assessment deadlines), not poor financed-emissions data quality. This is my reading of the press releases above.
- EBA Guidelines on the management of ESG risks apply from 11 Jan 2026 for large institutions and by 11 Jan 2027 for small and non-complex ones. They require prudential transition plans and annual ESG materiality assessments — [EBA final report PDF](https://www.eba.europa.eu/sites/default/files/2025-01/fb22982a-d69d-42cc-9d62-1023497ad58a/Final%20Guidelines%20on%20the%20management%20of%20ESG%20risks.pdf)
- Per BDO's reading, banks are expected to ask high-emitting clients for forward-looking transition plans. Large institutions must assess portfolio alignment at sector *and counterparty* level — [BDO](https://www.bdo.de/en-gb/insights/financial-services/final-eba-guidelines-on-esg-risk-management-implications-for-governance-and-risk-management). Institutions must build "robust data collection processes" using internal and external ESG data — [ESG News](https://esgnews.com/eba-issues-final-esg-risk-guidelines-mandating-financial-institutions-compliance-by-2026) (secondary).
- Pillar 3 ESG (CRR3): the final draft ITS (EBA/ITS/2026/02) *removes* the GAR, BTAR and "top-20 carbon-intensive counterparties" templates compared with the consultation. It cuts ESG data points for large institutions by 37% and adds a three-tier, size-based model. Small and non-complex institutions file one simplified quantitative template from 31 Dec 2027. The revised rules apply from the 31 Dec 2026 reference date, pending Commission adoption — [Management Solutions](https://www.managementsolutions.com/index.php/en/node/4275); [PwC DE](https://blogs.pwc.de/en/regulatory/article/255706/eba-finalises-its-disclosure-package/?func=pdf)
- Earlier, on 6 Aug 2025, the EBA issued a no-action letter telling authorities not to prioritise enforcing GAR and taxonomy templates — [EBA](https://www.eba.europa.eu/node/18424); [CMS](https://cms.law/en/int/legal-updates/european-banking-authority-proposes-streamlined-esg-disclosure-rules-for-banks)
- At the same time, ESG disclosure scope widens to large non-listed institutions, small and non-complex institutions and large subsidiaries — [CMS](https://cms.law/en/int/legal-updates/european-banking-authority-proposes-streamlined-esg-disclosure-rules-for-banks)
- CSRD Omnibus I (agreed Dec 2025): CSRD now applies only to EU companies with more than 1,000 employees and more than €450m turnover, from FY2027 (previously 250 employees / €50m / €25m) — [Morrison Foerster](https://www.mofo.com/resources/insights/251222-eu-sustainability-omnibus-i-detailed-omnibus); [Cooley](https://www.cooley.com/news/insight/2025/2025-12-10-eu-reaches-agreement-on-omnibus-i-impacting-csrd-and-csddd-compliance-for-us-companies). This sharply cuts the number of borrowers that will *self-report* audited emissions. That leaves banks needing either proxies or bank-collected data for the mid-market.

**Global standard setters**
- Basel Committee (13 Jun 2025): the climate disclosure framework was made **voluntary** after US pressure. Its templates include financed emissions by sector with credit quality and maturity, and it explicitly allows "flexibility" on data quality — [ESG Today](https://www.esgtoday.com/basel-committee-releases-voluntary-framework-for-banks-disclosure-of-climate-risks/); [Linklaters](https://sustainablefutures.linklaters.com/post/102kgiq/basel-committee-publishes-international-voluntary-climate-risk-disclosure-framewo); [Public Citizen critique](https://www.citizen.org/news/voluntary-disclosure-of-climate-risks-falls-short-of-protecting-financial-system/)
- ISSB amendments to IFRS S2 (issued around 11 Dec 2025, effective 1 Jan 2027):
  - Category 15 reporting can be limited to financed emissions.
  - The GICS requirement for disaggregation is dropped.
  - Jurisdictional relief from the GHG Protocol is allowed.
  - IPCC global-warming-potential relief is granted.
  - Sources: [EY](https://www.ey.com/en_gl/technical/ifrs-technical-resources/issb-issues-targeted-amendments-to-ifrs-s2); [XBRL](https://www.xbrl.org/news/issb-trims-and-tunes-ifrs-s2-on-financed-emissions/). Euromoney describes this as having "narrowed the scope of mandatory financed-emissions reporting for financial institutions" — [Euromoney, Mar 2026](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- NZBA voted to cease operations in Oct 2025. It had peaked at about 140-150 banks; US, Canadian, Japanese and several European majors (JPM, GS, MS, Citi, HSBC, UBS) left first — [BNN Bloomberg / CP](https://www.bnnbloomberg.ca/business/2025/10/03/mark-carney-launched-net-zero-banking-alliance-votes-to-shut-down); [Finextra](https://www.finextra.com/newsarticle/46713/net-zero-banking-alliance-shuts-down)
- UK: the PRA's SS5/25 replaces SS3/19. It has 140 paragraphs versus 32 before, a dedicated **data** chapter, quantitative risk-appetite metrics and scenario analysis. It came with PS25/25 — [Milliman, Jan 2026](https://www.milliman.com/en/insight/ss-5-25-banks-insurers-climate-risks); [Management Solutions](https://www.managementsolutions.com/en/node/4532). Publication date not confirmed from primary source.
- Singapore: MAS issued final transition-planning guidelines for banks, insurers and asset managers on 5 Mar 2026, effective Sept 2027 after an 18-month transition. The disclosure expectations were removed from the final text. FIs are expected to engage customers to understand climate risks and avoid "indiscriminate withdrawal of credit" — [MAS](https://www.mas.gov.sg/news/media-releases/2026/guidelines-on-transition-planning); [Rajah & Tann](https://www.rajahtannasia.com/viewpoints/mas-issues-transition-planning-guidelines-on-climate-risk-management-for-banks-insurers-and-asset-managers-effective-september-2027/)
- US: regulators, including the Fed, have de-emphasised climate risk under the second Trump administration — [Mintz, Mar 2026](https://www.mintz.com/insights-center/viewpoints/2026-03-16-european-central-bank-plans-fine-banks-failures-address)

**Emerging markets (carbonTraceAI focus)**
- South Africa: the Prudential Authority issued updated climate disclosure guidance (G3/2025, Oct-Nov 2025). It replaces the 2024 notes for banks and insurers, is built on IFRS S1/S2 and Basel, and has **no assurance requirement yet**, but firms should prepare for it — [Acts Online](https://acts.co.za/news/blog/2025/10/banks-climate-disclosure-guidance-replaced); [Webber Wentzel](https://www.webberwentzel.com/News/Pages/south-africas-prudential-authority-issues-updated-climate-related-disclosure-guidance-for-banks-and-insurers.aspx). It is guidance, not a directive.
- Kenya: in Apr 2025 the CBK issued the Kenya Green Finance Taxonomy and a Climate Risk Disclosure Framework, aligned to IFRS S2 and Basel and developed with EIB support — [TechCabal](https://techcabal.com/2025/04/07/kenya-central-bank-18-month-climate/); [Khusoko](https://khusoko.com/2025/04/12/cbk-unveils-green-finance-tools-for-banking-sector/). Timelines conflict: an 18-month window (around Oct 2026) per [Business Daily](https://www.businessdailyafrica.com/bd/corporate/companies/banks-have-18-months-to-enforce-climate-risk-disclosure-rule-4992934), versus a later draft that is voluntary from Jan 2027 and mandatory two years later per [Business Daily](https://www.businessdailyafrica.com/bd/corporate/companies/banks-face-mandatory-climate-risk-disclosures-in-cbk-push-4768012)
- Nigeria: the Nigerian Sustainable Banking Principles (2012) are mandatory for banks and DFIs. In Dec 2023 the CBN said it was "mulling" a climate-risk regulation — [CBN NSBP](https://www.cbn.gov.ng/Out/2014/CCD/SUSTAINABLE%20BANKING%20PRINCIPLES.pdf); [ThisDay](https://www.thisdaylive.com/2023/12/20/cbn-mulls-regulations-against-climate-risks-to-drive-sustainable-banking-principles/). No evidence found that it was issued in 2025-26.
- Egypt (the most relevant EM finding for carbonTraceAI): the CBE issued binding sustainable-finance regulations in 2022 (sustainability unit, quarterly and annual reporting) — [climate-laws.org](https://climate-laws.org/document/central-bank-of-egypt-mandatory-regulations_69c0). It later issued a **2025 CBAM directive**:
  - Banks must give the CBE a list of exporting clients and support them in meeting EU and UK CBAM standards.
  - Banks must assess CBAM impact on their portfolios, especially steel, aluminium, cement, fertiliser and hydrogen.
  - Banks must file **semi-annual reports to the CBE sustainability department starting H2 2026**.
  - Sources: [Zawya](https://www.zawya.com/en/economy/north-africa/egypt-cbe-directs-banks-to-back-exporters-in-meeting-international-sustainability-standards-awo3hb2t); [Amwal Al Ghad](https://en.amwalalghad.com/?p=208168); [RegAlert digest](https://regalert.today/document/21f4de03-72ce-43dd-b122-992eee9ef835) (secondary; circular text not obtained). The Governor cited the directive in Feb 2026 — [Daily News Egypt](https://www.dailynewsegypt.com/2026/02/16/cbe-catalyses-banking-sectors-shift-toward-sustainable-finance-governor-abdalla/)
  - The CBE also requires an Environmental and Social Risk Management System by Jan 2028 — [Daily News Egypt](https://www.dailynewsegypt.com/?p=850565)
  - Separately, Egypt's FRA Decision 36/2026 requires non-bank FIs with more than EGP 100m capital to report verified Scope 1 and 2 emissions and offset about 20% — [ESG News](https://esgnews.com/?p=42178)
- India: the RBI draft disclosure framework (Feb 2024) covered Scope 1, 2 and 3. Governance, strategy and risk disclosures were due FY2025-26 and metrics and targets FY2027-28 for scheduled commercial banks and large NBFCs — [Cyril Amarchand/BDO summaries](https://www.bdo.global/en-gb/news/ifrs-news/india%E2%80%99s-central-bank-publishes-draft-disclosure-framework-on-climate-related-financial-risks). Later reports say the start was pushed back (voluntary FY2026-27, mandatory FY2027-28) — [KS&K](https://ksandk.com/newsletter/rbis-climate-risk-disclosure-regime-a-green-turn-for-indian-banking/). Final 2025 "directions on climate finance and climate risk management" are referenced by [Uniqus, Jan 2026](https://uniqus.com/wp-content/uploads/2026/01/Building-Credibility-in-Green-Finance-Interpreting-RBIs-New-Directions-on-Climate-Finance.pdf). The final disclosure timeline was not confirmed from the RBI.

### Inferences
- The binding obligation in 2026 is "know your counterparties' transition risk and materiality" (EBA guidelines, ECB, PRA, MAS, CBE CBAM directive). It is not "report score-1 financed emissions". That favours an *agentic counterparty assessment / transition-plan review* product over a pure "data quality upgrade" product.
- Disclosure deregulation (GAR/BTAR removal, IFRS S2 relief, voluntary Basel, Omnibus) lowers the regulatory reward for better financed-emissions numbers. It weakens the "banks will pay for score 1-2 data" thesis in the EU and globally.
- Egypt's CBE CBAM directive is the clearest EM regulator-driven, bank-side demand for *client-level product emissions*, which is exactly carbonTraceAI's CBAM engine. Banks must report CBAM exposure of exporting clients semi-annually from H2 2026. This is a concrete wedge to test.

### Gaps
- Primary text of the CBE CBAM directive (number, exact data fields) was not retrieved.
- Bank Al-Maghrib climate guidance was not found in this search pass.
- Whether a third ECB penalty has been imposed since Feb 2026 was not found.
- Final RBI disclosure directions (exact Scope 3 / financed-emissions requirement and dates) are unconfirmed.
- No NGFS 2025-26 document reviewed in this pass.

## 2. PCAF adoption and data quality: is there evidence banks will pay for better borrower data?

### Takeaway
PCAF is the de facto standard (719 institutions, about $100tn in assets), and most corporate and SME exposures are still measured with sector-average proxies (score 4-5). But I found **no direct evidence of banks paying borrowers or third parties specifically to obtain score 1-2 borrower data at scale**. The commercial evidence that does exist has three forms:
- banks *co-investing* in SME data-sharing platforms (FourTwoThree);
- banks offering *free* SME carbon tools as relationship products (NatWest/Cogo);
- banks buying *proxy-improving* asset-level data (Climate TRACE-based tool in Egypt; S&P/MSCI).

### Cited Findings
- PCAF had 719 financial institutions in its community and added 151 signatories in 2025, covering about $100tn in assets across 85+ countries — [PCAF 2025 Impact Report](https://www.carbonaccountingfinancials.com/files/1775053892_Annual-Report-Final-v2.pdf); [PCAF news](https://carbonaccountingfinancials.com/en/newsitem/pcaf-annual-impact-report). It passed 600 in May 2025 — [Thommessen](https://www.thommessen.no/en/sustainability/database/initiative/partnership-for-carbon-accounting-financials-pcaf)
- A PwC benchmark of 57 FIs (38 banks, 19 insurers and asset managers) found 96% use PCAF methodology and 42% restated their financed emissions — [PwC UK](https://www.pwc.co.uk/services/consulting/insights/financed-emissions-pwc-benchmarking.html) (via search summary; page returned 403). The frequent restatements are a sign of data instability.
- The PCAF data-quality scale runs from 1 (audited or verified borrower data) to 5 (outstanding amount × sector factor). Score 2 is unverified counterparty-reported emissions or metered energy, and score 4 is revenue-based — [DitchCarbon guide](https://ditchcarbon.com/resources/guides/pcaf-data-quality-by-asset-class); [Euromoney](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- Example of proxy reliance: a Greek cooperative bank's 2025 PCAF report estimates its corporate and SME loans (88% of the loan book) by assigning *average sectoral emissions* in proportion to outstanding loans — [PCAF institution download](https://www.carbonaccountingfinancials.com/files/institutions_downloads/CBK2025.pdf)
- Africa: more than 80% of African banks do not disclose portfolio emissions (WWF SUSBA 2025). SA and Kenyan banks lead; Standard Bank and Absa disclose, partly on PCAF; Ecobank, Access and CRDB have only made commitments — [Africa Sustainability Matters](https://africasustainabilitymatters.com/financed-emissions-as-the-next-esg-disclosure-frontier-for-africas-financial-sector/); [Euromoney](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- BII (UK DFI) says "the even bigger challenge is availability of Scope 3 data". It engages investees and fills gaps with modelled data. Standards are evolving to *accept* proxies as stopgaps — [Euromoney, Mar 2026](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- The UNEP FI runs a programme helping African and Middle Eastern banks adopt PCAF (donor and TA-funded, not commercial) — [Euromoney](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- **Bank-side money into borrower data (closest evidence):**
  - FourTwoThree launched in June 2025 with strategic investment from NatWest, NAB and SC Ventures (Standard Chartered). It is a platform for banks, enterprises and SME value chains to share primary emissions data — [NatWest Group PR](https://www.natwestgroup.com/news-and-insights/news-room/press-releases/enterprise/2025/jun/fourtwothree-launches-t-osupport-sustainable-transition-for-mill.html); [ESG News](https://esgnews.com/natwest-nab-sc-ventures-launches-sme-climate-transition-platform-fourtwothree)
  - Sage Carbon Measurement API is positioned for banks to move SME financed emissions from PCAF 5 toward PCAF 2 using accounting-ledger data (launch date unconfirmed) — [search summary via Fintech Times](https://thefintechtimes.com/?p=117794). This is the same thesis as carbonTraceAI's ERP ingestion, already pursued by an accounting-software incumbent.
  - NatWest and Cogo: a free SME carbon tracker and toolkit plus the free NatWest Carbon Planner. Cogo claims 8m bank customers have access to its product. Banks pay; SMEs get it free — [Finextra](https://www.finextra.com/pressarticle/99734/natwest-and-cogo-create-carbon-toolkit-for-smes); [Cogo for banks](https://cogo.co/products/for-banks)
  - Egypt: Climate Risk Services built a "Financed Emissions Tool" on Climate TRACE asset-level data. It estimated financed emissions for more than 80% of a leading Egyptian bank's corporate book under PCAF and improved its data-quality scores. The bank is unnamed and cost and driver are undisclosed (June 2025) — [Climate TRACE](https://climatetrace.org/news/how-a-leading-egyptian-bank-gained-visibility-into-its)
  - Barclays executive: AI let the bank roughly quintuple the credit limits covered by client transition assessments in 2025 versus 2024, with a fourfold time reduction — [LinkedIn post via search](https://uk.linkedin.com/in/voxvishal) (single-person claim, unverified).

### Inferences
- Demand for *better* data is real: PCAF ubiquity, restatements and proxy-heavy books all show it. But willingness to pay goes to (a) tools that make the bank's own process cheaper, or (b) platforms banks can give to SMEs as a relationship product. It does not go to "verified borrower data" as a priced commodity. The pattern is "bank pays for the pipe, borrower supplies data for free."
- Asset-level and satellite proxies (Climate TRACE, S&P, MSCI) are a cheaper substitute for borrower-reported data for large emitters. Borrower-reported data matters most for SMEs and mid-caps, where banks have the least budget per counterparty.
- Regulators are signalling that proxies are acceptable (Basel "flexibility", the ISSB relief), so the score 4→2 upgrade is a "nice-to-have" in most jurisdictions in 2026.

### Gaps
- No aggregate statistic was found on the share of bank financed emissions at score 4-5 versus 1-2. The PwC benchmark full text was blocked. Large-bank weighted DQS figures (often around 3-4 for business loans in my prior knowledge) could not be verified, so I did not include them.
- No evidence was found of a bank paying a per-borrower fee for verified data, or offering an explicit margin discount solely for emissions *disclosure*, outside SLLs and CarbonChain claims (see section 4).

## 3. Products and players serving FIs: where agentic workflows fit

### Takeaway
The FI financed-emissions stack is crowded and incumbents are already shipping AI agents (S&P Sustainable1 in Jul 2026, Watershed Finance in Oct 2026, Workiva). A startup cannot win on "PCAF calculator for banks". The open spaces are:
- counterparty-side primary-data capture (ERP/ledger → PCAF score 2, CBAM product-level);
- commodity and trade-finance flows (CarbonChain is the incumbent);
- EM banks underserved by global vendors' coverage.

### Cited Findings
- S&P Global Sustainable1 (Jul 2026) launched four AI agents including a "Transition Finance" agent. It says agentic AI is moving "from pilot to production" in banks and lets banks plug S&P climate data into their own agents via MCP — [S&P Sustainable1 blog](https://www.spglobal.com/sustainable1/en/insights/blogs/from-hype-impact-ai-agents-for-banks) (via search summary; fetch 403)
- Watershed Finance: an Oct 2026 webinar on new AI agents in its PCAF-aligned financed-emissions platform for data cleaning and analysis — [Watershed](https://watershed.com/events/watershed-finance-demo-october)
- Workiva launched an AI agent for sustainability disclosure analysis (Jun 2026). SAP showcased sustainability agents at Sapphire 2026 — [ESG Post](https://esgpost.com/tag/national-bank-of-kuwait/); [SAP](https://www.sap.com/assetdetail/2026/06/68e57168-587f-0010-bca6-c68f7e60039b.html)
- Persefoni: one of the first PCAF-accredited SaaS vendors (2023), with a financed-emissions module for banks, asset managers and insurers. Last disclosed raise was a $50m Series C-1 in 2023 (Persefoni GPT) — [Persefoni](https://persefoni.com/fr/blog/persefoni-recognized-among-first-pcaf-accredited-saas-vendors); [Jones Day](https://m.jonesday.com/en/practices/experience/2023/08/eneos-innovation-partners-invests-in-persefoni-ai). No 2025-26 funding found.
- CarbonChain: carbon accounting for commodity traders and their trade-finance banks (ING, Société Générale, Rabobank). SocGen ran year-long pilots with metal traders Concord and IXM tying loan terms to emissions. Rabobank uses it for Scope 3 data on its commodity trade-finance book. Vendor claims rate discounts of up to 5bp (or up to 10bp in another vendor post) — [CarbonChain banks](https://www.carbonchain.com/banks); [ING case](https://www.carbonchain.com/case-study/how-ing-aims-to-support-the-decarbonization-of-its-trade-finance-clients); [SocGen](https://wholesale.banking.societegenerale.com/en/news-insights/all-news-insights/news-details/news/innovating-help-trade-commodity-clients-reduce-their-carbon-emissions/). Bank announcements date from 2022-23; no new 2025 deals were found.
- Cogo: a bank-embedded carbon product (NatWest retail and SME) — [Cogo](https://cogo.co/products/for-banks)
- FourTwoThree (NatWest, NAB, SC Ventures): an SME value-chain data platform — [NatWest](https://www.natwestgroup.com/news-and-insights/news-room/press-releases/enterprise/2025/jun/fourtwothree-launches-t-osupport-sustainable-transition-for-mill.html)
- EM-native players:
  - Climate Risk Services: Climate TRACE-based tool, Egyptian bank — [Climate TRACE](https://climatetrace.org/news/how-a-leading-egyptian-bank-gained-visibility-into-its)
  - CarbonScope360 (Nigeria): founder claims "institutional uptake" for financed emissions; no bank named — [Vanguard, Feb 2026](https://www.vanguardngr.com/2026/02/nigerian-climate-tech-platform-advances-enterprise-carbon-accounting/amp/)
  - Melanin Kapital (Kenya): a "carbon neobank" offering SaaS for FIs to track carbon portfolios (self-described) — [Climate Finance Lab](https://www.climatefinancelab.org/wp-content/uploads/2025/10/Carbon-Neobank_Vehicle-Analysis.pdf)
- No bank in Kenya, Nigeria or Egypt was found formally contracting a carbon-accounting startup for SME financed emissions — (search-based negative finding, see [Climate TRACE](https://climatetrace.org/news/how-a-leading-egyptian-bank-gained-visibility-into-its) for the only concrete EM bank deployment)

### Inferences
- Agent-fit tasks for banks, ranked by evidence of pain:
  1. Counterparty transition-plan and materiality assessment at scale (EBA, PRA, MAS mandates; the Barclays 5x claim).
  2. CBAM exposure screening of exporting borrowers (CBE directive; ICC view, section 5).
  3. Borrower data collection and chasing, plus PCAF score upgrade, for SME and mid-market clients (FourTwoThree, Sage).
  4. SLL KPI evidence packs (section 4).
- carbonTraceAI's differentiator (deterministic calc engine, ERP ingestion, provenance/audit trail) fits what incumbents' LLM agents lack: auditable, borrower-side primary data. The natural distribution, though, is via the bank to its borrowers (B2B2B), not bank-as-direct-data-buyer.

### Gaps
- MSCI, ISS, Moody's, Trucost, Clarity AI, Carbon4 Finance, Greenomy and Novata bank-specific 2025-26 developments were not researched in this pass.
- "Util", "Sprout", "Ecobio", "Intergen" and "Profitable Climate" were not verified as real FI-carbon players. I found nothing on them and do not assert their existence.
- No African or Indian bank vendor-selection disclosures were found.

## 4. Sustainability-linked loans and bonds: market size, KPI verification, agent tasks

### Takeaway
The SLL market shrank sharply in 2025 (roughly -18% to -52% depending on source and period) amid credibility scrutiny and US politics. The March 2025 LMA principles make post-signing independent verification of SPT performance mandatory where it drives a margin ratchet. So there is a recurring, compliance-grade verification workload, but on a shrinking deal count.

### Cited Findings
- Labelled loan volumes fell 52% year on year in H1 2025 (Moody's citing Environmental Finance Data). SLL issuance held around $80bn per quarter in Q1-Q2 2025 — [Environmental Finance, Sept 2025](https://www.environmental-finance.com/content/market-insight/a-labelled-loan-market-in-transition.html)
- Full-year 2025 sustainable loan volumes were about 18% lower after a record 2024. SLLs remain "the main drag" into 2026, and Asia's share is rising — [Environmental Finance, Sept 2026](https://www.environmental-finance.com/content/market-insight/sustainable-loans-face-a-reset-as-digital-infrastructure-and-transition-finance-take-hold.html)
- Bloomberg: through early Nov 2025, SLLs were down about 30% and green loans down 27% — [Bloomberg Law](https://news.bloomberglaw.com/esg/global-esg-bond-issuance-stalls-for-first-time-since-2022)
- LSEG LPC: global syndicated sustainable loans fell 30% in H1 2025 to $327bn, with the Americas weakest — [LMA Horizons](https://horizons.lma.eu.com/q3-september2025/market-outlook)
- Sources conflict on magnitude (definitions and periods differ) — compare the above with [Africa Sustainability Matters](https://africasustainabilitymatters.com/sustainable-loans-insight-2025-key-findings-from-environmental-finances-report/) (H1 -18%).
- LMA/APLMA/LSTA SLL Principles (26 Mar 2025):
  - Language is clarified into mandatory, recommended and optional.
  - Post-signing independent verification of SPT performance is **required** where it can trigger a margin adjustment.
  - A pre-signing external review is recommended.
  - Grandfathering is removed.
  - Sources: [LMA PDF](https://lma.eu.com/application/files/6317/4298/0865/Sustainability-Linked_Loan_Principles_-_26_March_2025.pdf); [Slaughter and May](https://slaughterandmay.com/media/ufhjnnmo/2025-updates-to-the-sustainability-linked-loan-principles.pdf); [Devonshires](https://insights.devonshires.com/post/102k72e/lma-publishes-new-edition-of-the-sustainability-linked-loan-principles)
- The drivers of the decline include investor scrutiny of target ambition and borrower caution on KPI materiality — [Environmental Finance](https://www.environmental-finance.com/content/market-insight/a-labelled-loan-market-in-transition.html)

### Inferences
- Agent tasks with clear specs are KPI baseline recalculation, annual SPT evidence packs, verifier-ready audit trails, and recalculation after methodology or perimeter changes. They map well to carbonTraceAI's provenance/audit trail. The buyer is the *borrower* (who pays the verifier) or the verifier itself, not the bank.
- A shrinking SLL market plus a margin ratchet of only a few bp means a limited budget per deal. This is better as a feature than a standalone product.

### Gaps
- No 2025-26 data was found on SLL volumes in Africa or India specifically, on typical margin-ratchet size, or on verification fees.
- ICMA SLB principle 2025-26 changes were not reviewed.

## 5. Trade finance and CBAM; insurers (PCAF Part C)

### Takeaway
CBAM's definitive phase (from 1 Jan 2026) is turning carbon into a credit and liquidity issue for EM exporters and their banks. There is early, concrete bank and DFI money: the Turk Eximbank €1bn CBAM loan and Egypt's CBE directive. There is no evidence yet of systematic carbon-adjusted trade-finance pricing. Insurer demand is nascent: PCAF Part C v2 was published Dec 2025, with low disclosure rates.

### Cited Findings
- ICC (Feb 2026): CBAM is moving from compliance to a balance-sheet and liquidity concern. Documentary credits, supply-chain finance and receivables discounting "increasingly require carbon-cost sensitivity in credit assessment". EM exporters often lack product-level emissions data, which pushes default values and conservative charges onto them — [ICC Trade Finance Bulletin](https://library.iccwbo.org/content/tfb/news/dcwn_02February2026101213.htm) (via search summary; paywalled)
- Turk Eximbank: a €1bn, 10-year loan (signed 7 May) from Deutsche Bank, Standard Chartered, BNP Paribas and ING with a €600m IBRD first-loss guarantee, to finance exporters adjusting to CBAM, partly for SMEs — [GTR](https://www.gtreview.com/news/europe/turk-eximbank-gets-e1bn-loan-to-help-exporters-adjust-to-cbam/)
- India: iron and steel were 78% of CBAM-covered exports to the EU in 2023 (more than €5bn), with aluminium at €1.4bn. GTRI estimates exporters may need to cut prices 15-22% — [Trade Finance Global](https://www.tradefinanceglobal.com/posts/the-price-cbam-by-2050-who-will-pay-how-much-when/); [OneStopESG](https://onestopesg.com/esg-news/eu-cbam-2026-exporter-guide-carbon-border-tax)
- Egypt CBE CBAM directive: see section 1 (banks list exporting clients, assess CBAM portfolio impact, semi-annual reports from H2 2026) — [Zawya](https://www.zawya.com/en/economy/north-africa/egypt-cbe-directs-banks-to-back-exporters-in-meeting-international-sustainability-standards-awo3hb2t)
- Afreximbank: the trade-finance gap is $80-120bn a year, with $17.5bn disbursed in 2024 and a target to double intra-African trade finance by 2026 — [Trade Finance Global](https://www.tradefinanceglobal.com/posts/afreximbank-doubles-intra-african-trade-finance-to-40bn-by-2026/). No Afreximbank CBAM-specific programme was found.
- CarbonChain trade-finance banks (ING, SocGen, Rabobank): see section 3.
- Insurers: PCAF Part C 2nd edition (2 Dec 2025) adds treaty reinsurance and project insurance methods — [PCAF Part C exec summary](https://carbonaccountingfinancials.com/files/standard-launch-2025/PartC-PCAF-V2-Executive-Summary-Clean.pdf); [EY](https://www.ey.com/en_gl/technical/ifrs-technical-resources/pcaf-updates-financed-and-insurance-associated-emissions-standards). About two years after the 2022 standard, only a third of 29 initial insurance signatories had disclosed insurance-associated emissions. Canada's OSFI mandates including them in Scope 3 — [Moody's](https://www.moodys.com/web/en/us/insights/insurance/will-2025-be-a-pivotal-year-to-accelerate-insurance-associated-emissions-disclosures.html)

### Inferences
- CBAM is the strongest bridge between carbonTraceAI's existing CBAM engine and finance buyers. Three buyers stand out:
  - EM banks required to screen exporters (Egypt now; plausibly Turkey, India, Morocco, South Africa next);
  - ECAs and DFIs funding CBAM-adjustment lines (Turk Eximbank/World Bank model);
  - exporters seeking to replace EU default values with verified actuals, which have direct € value.
- Here the borrower has its own monetary reason to produce verified data (it lowers CBAM certificate cost), which solves the "who pays" problem better than PCAF does.
- Insurers are a low-priority segment for an early-stage EM startup in 2026.

### Gaps
- No evidence was found of carbon-adjusted credit pricing in trade finance beyond vendor bp claims.
- IFC Global Trade Finance Program carbon criteria were not found.
- The Morocco (Bank Al-Maghrib) CBAM response was not found.

## 6. DFI ESG due diligence (IFC PS3, EIB, AfDB, BII)

### Takeaway
DFIs have hard, long-standing GHG quantification requirements for large projects: IFC PS3 requires Scope 1 and 2 quantification for projects expected to emit more than 25 ktCO2e a year. They also push data demands down to EM banks and investees (BII, IFC loans to Banque Misr). However, I found no quantified evidence of DFI spend on GHG tooling. DFI work is TA- and consultant-delivered, which suggests grant/TA-funded pilots rather than SaaS ACVs.

### Cited Findings
- IFC PS3: projects expected to emit more than 25 ktCO2e a year must quantify Scope 1 and 2 using recognised methods. The threshold was previously 100kt. Clients must implement technically and financially feasible reduction options — [E3G](https://www.e3g.org/bank-metrics/greenhouse-gas-accounting-at-project-and-portfolio-level/); [WRI (history)](https://tools.wri.org/blog/2009/11/review-ifc-performance-standards-and-sustainability-policy-overview-key-issues)
- The CAO (IFC/MIGA ombudsman) advisory recommends lowering the threshold to 10 ktCO2e and adding Scope 3. This is a recommendation, not adopted — [CAO](https://cao-ombudsman.org/news/new-cao-advisory-report-strengthening-greenhouse-gas-mitigation-ifc-financed-projects)
- IFC's $150m sustainability loan to Banque Misr requires allocation to climate-eligible assets and portfolio reporting "in line with IFC climate eligibility criteria", plus data-governance TA for EBank — [Daily News Egypt, Feb 2026](https://www.dailynewsegypt.com/2026/02/16/cbe-catalyses-banking-sectors-shift-toward-sustainable-finance-governor-abdalla/)
- BII engages investees on data and fills gaps with modelled data — [Euromoney](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- The CBK framework was developed with EIB technical support — [Khusoko](https://khusoko.com/2025/04/12/cbk-unveils-green-finance-tools-for-banking-sector/)

### Inferences
- DFIs are a credible *channel and co-funder* for EM pilots (TA budgets, credit-line conditions that require partner banks to report). They are less credible as direct SaaS buyers. A wedge is getting written into a DFI credit line's reporting requirements, so partner banks and their borrowers adopt the tool.

### Gaps
- No data was found on DFI GHG due-diligence cost per project, or on EIB, AfDB or BII project GHG thresholds in their 2025-26 versions. My recollection of an EIB 20 kt threshold could not be verified in this pass.

## 7. Payer reality: budgets, ACVs, procurement — and the verdict on "banks pay for verified borrower emissions data"

### Takeaway
Large banks do budget for climate data and tech: typically $250-500k a year on ESG tech per a 2024 Chartis survey, with carbon-accounting software ACVs of about $20-160k (Watershed median about $70k). But that budget goes to incumbents and data vendors. **The hard evidence does not support banks paying for verified borrower-level data as a standalone product, especially in emerging markets.** The better-evidenced variants are:
- (a) regulator-forced counterparty screening (CBAM in Egypt, EBA transition plans);
- (b) bank-funded SME platforms where the bank pays for the pipe;
- (c) borrower-paid verification where the borrower has its own € incentive (CBAM actuals, SLL ratchets).

### Cited Findings
- Chartis/BCT Digital (Jul 2024, 77 practitioners): more than 72% of FIs plan to spend up to $500k or more on ESG technology. Most spend about $250-500k a year, with North American and European banks more likely above $500k. Top climate-risk challenges are stress-testing expectations (67%) and accurate GHG accounting (56%) — [IBS Intelligence](https://ibsintelligence.com/?p=560199); [ESG News](https://esgnews.com/bct-digital-survey-reveals-over-72-financial-institutions-to-invest-heavily-in-esg-technology-amid-record-esg-and-anti-esg-proposals-in-2024)
- Verdantix forecast: FI spend on carbon-accounting software of $256m by 2027, up from $51m in 2021, about a fifth of $1.49bn total carbon-management spend — [IFRE](https://www.ifre.com/esg/566014/financial-institutions-investing-in-carbon-tracking-software) (an older forecast, likely made before the 2025 deregulation).
- Watershed contract values (Vendr buyer data, all sectors, not bank-specific): median about $70k a year, range about $21-158k. Implementation is $10-50k+ — [Vendr](https://www.vendr.com/marketplace/watershed); [rfp.wiki](https://www.rfp.wiki/sustainability-esg/carbon-accounting-and-management-software/watershed/persefoni)
- Banks giving SME carbon tools away free (NatWest/Cogo) shows banks treat borrower carbon data as a *relationship and cost* item, not a revenue line — [Finextra](https://www.finextra.com/pressarticle/99734/natwest-and-cogo-create-carbon-toolkit-for-smes)
- EM: more than 80% of African banks do not yet disclose portfolio emissions. PCAF adoption in Africa and the Middle East is supported by the UNEP FI programme rather than commercial procurement — [Euromoney](https://www.euromoney.com/article/7ti9tf94di80c0o44ss4ko4ks/african-banks-face-a-long-road-to-lower-financed-emissions/)
- SA PA guidance has no assurance requirement yet — [Acts Online](https://acts.co.za/news/blog/2025/10/banks-climate-disclosure-guidance-replaced). Kenya's mandatory phase is possibly 2027-2029 — [Business Daily](https://www.businessdailyafrica.com/bd/corporate/companies/banks-face-mandatory-climate-risk-disclosures-in-cbk-push-4768012). India metrics are around FY2027-28 — [KS&K](https://ksandk.com/newsletter/rbis-climate-risk-disclosure-regime-a-green-turn-for-indian-banking/)
- Political headwinds: NZBA dissolved in Oct 2025 — [Finextra](https://www.finextra.com/newsarticle/46713/net-zero-banking-alliance-shuts-down). The Basel framework is voluntary — [ESG Today](https://www.esgtoday.com/basel-committee-releases-voluntary-framework-for-banks-disclosure-of-climate-risks/)

### Inferences
- Verdict on the prior report's 8/12 hypothesis: **downgrade as stated (bank as payer for verified borrower data), upgrade a reframed version.**
  - Against:
    - no observed per-borrower data payments;
    - the disclosure regime is loosening (GAR/BTAR gone, IFRS S2 relief, voluntary Basel, CSRD scope cut, NZBA closed);
    - regulators accept proxies;
    - asset-level and satellite datasets substitute for large emitters;
    - EM bank mandates are mostly 2027-29 and unassured;
    - incumbents (S&P, Watershed) already sell agents into bank budgets.
  - For:
    - ECB fines and EBA guidelines create non-optional counterparty-assessment work;
    - CBE's CBAM directive creates bank reporting on exporters from H2 2026;
    - banks are co-investing in SME data platforms (FourTwoThree) and paying for embedded SME tools (Cogo);
    - DFIs condition credit lines on reporting.
- Reframed wedge (best-evidenced): a "CBAM and transition-exposure screening agent for EM banks' exporter books". The bank pays a modest platform fee (regulator-driven, e.g. CBE). Exporter borrowers are onboarded via ERP ingestion and get verified product-level CBAM actuals (borrower-side € incentive). Provenance packs then serve as PCAF score 2 data and SLL/DFI evidence as by-products. Start with Egypt, then Turkey, Morocco, India and South Africa, with DFI or TA co-funding for pilots.
- Expect EM bank pilots to be small (likely tens of $k, often TA-funded) and slow (12-18 month procurement). This is my inference from the absence of observed EM commercial deals. No direct EM ACV data was found.

### Gaps
- No bank-specific ACVs for financed-emissions tools (MSCI, Persefoni, S&P) or EM bank climate-tech budgets were found.
- No 2025-26 survey of bank climate-data spend was found (the Chartis data is 2024).
- No procurement-cycle data was found for African or Indian banks.
- Whether any EM bank has paid (rather than received TA) for a borrower-data platform is unverified.
