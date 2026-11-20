# Is an Agentic AI Workflow Necessary for CBAM Compliance Software? A Skeptical, Evidence-Based Assessment

Research date: 2026-10-12. Scope: the critical case for and against adding LLM agents to carbonTraceAI. The product already has deterministic ERP ingestion, a canonical store, a CBAM calc engine, EU XML rendering, raw_ref provenance and OCR. Items marked **[SPECULATIVE]** are my inference and have no direct source.

---

## 1. What do CBAM verifiers and regulators require, and is there any rule on AI-generated or automatically estimated data?

### Takeaway
The CBAM verification framework does not mention AI at all. The Commission's 141-page verification guidance (24 Aug 2026) has no reference to artificial intelligence, machine learning or LLMs. It is still hostile, by structure, to unexplained numbers. Verifiers work at "reasonable assurance" with a 5% materiality level per CN code. They treat complex or opaque data systems as inherent risk, they need primary source data and a full audit trail, and they issue a negative statement or a "limitation of scope" when evidence can't be traced. An LLM-produced number with no deterministic, documented method behind it would most likely be treated as a misstatement, a data gap or a non-conformity. It would not count as evidence.

### Cited Findings
**Legal stack**
- CBAM verification rests on four acts:
  - the "Methodology Act", Implementing Regulation (EU) 2025/2547;
  - the "Verification Principles Act", Implementing Regulation (EU) 2025/2546;
  - the accreditation Delegated Regulation (EU) 2025/2551 (AVR-DA);
  - the "Default Values Act", Implementing Regulation (EU) 2025/2621.

  The AVR-DA mirrors the EU ETS AVR, Regulation 2018/2067. — [Commission Guidance on CBAM verification and accreditation, 24 Aug 2026 (copy hosted by Eurometal)](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)
- Verification is needed only when actual emissions are declared, not when default values are used. Verifiers must be accredited by an EU national accreditation body. — [DEKRA](https://sustainability.dekra.com/en/cbam-verification-the-accreditation-framework-takes-shape/); [The Trade Hub](https://www.thetradehub.eu/en/guides/cbam/verification)
- Accreditation standards are ISO/IEC 17029:2022 and ISO 14065:2022. — [Accredia technical circular DC 19/2026 (3 June 2026)](https://accredia.it/wp-content/uploads/2026/05/Circolare_tecnica_DC_19-2026_ENG-Accreditation-of-VVBs-for-CBAM-scheme.pdf)

**No AI-specific rule**
- I extracted the full text of the Commission guidance and searched it for "artificial", "machine learning", "LLM" and "AI". The only hit was "artificially coloured" in a CN-code description of white Portland cement. — [Commission Guidance, 24 Aug 2026](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf) (my text search of the PDF)

**Materiality and assurance**
- The Verification Principles Act (Art. 5) sets materiality at 5% of total specific embedded emissions per tonne of good, for every good specified by its CN code. For other parameters the verifier uses expert judgement. Qualitative factors can make smaller misstatements material, and "materiality is not a tolerance band": every identified misstatement must be corrected. — Commission Guidance §3.5, §6.2 (same source)
- The verifier must obtain a "reasonable level of assurance", meaning high but not absolute assurance. — Commission Guidance §3.4

**Professional scepticism**
- The verifier "should not automatically accept the evidence obtained" and must analyse it thoroughly (professional scepticism under ISO 14065 and Annex VI of the CBAM Regulation). — Commission Guidance §3.3

**What verifiers flag as risk**
- Inherent risks named by the guidance:
  - complex data management systems;
  - manual transfers between logs, spreadsheets, IT systems and templates;
  - incorrect use of emission factors and incorrect identification of precursors;
  - unit conversions;
  - IT system failure.
- Control risks named by the guidance:
  - automated controls in IT systems that are missing or not functioning;
  - missing separation of data input from data checking (no segregation of duties).

  — Commission Guidance, risk analysis section (~p.52)
- The control activities checked include "quality assurance of information technology systems". Systems must be "designed, documented, tested, implemented, controlled and maintained" so they process reliable, accurate and timely data. — Commission Guidance (~p.55), referencing Annex II A.5 of the Methodology Act

**Estimation and data gaps**
- Estimation methods are allowed only where defined in the monitoring plan (MP). If a method was not in the MP, the verifier must check that emissions are not underestimated, which means estimates must be conservative. Data gaps count as misstatements and must be closed with surrogate data even if they are below materiality. — Commission Guidance §4.8
- Default values are "the very last resort". Verifiers must check that the correct default value was selected. — Commission Guidance §2 and §1.1

**Grounds for rejection**
- A negative statement follows from uncorrected material misstatements or from material non-conformities.
- A "limitation of scope" (another form of negative statement) arises when:
  - primary source data is missing, e.g. only aggregated data is available;
  - the MP does not describe the methodology clearly;
  - the operator fails to provide the information the verifier needs.

  — Commission Guidance §4.15, Table 6
- The verifier's internal documentation must give "the full audit trail" proving that only evidence-based decisions led to the opinion. — Commission Guidance, Annex I
- The Commission supplies an Excel template that automatically calculates embedded emissions. This is the regulator's own "deterministic calculator" baseline. — Commission Guidance §1.3

**Verifier practice (practitioner sources)**
- TÜV NORD's CBAM service description covers four checks:
  - data flow activities and the systems used to calculate embedded emissions;
  - the validity of the data;
  - a sampling plan for primary data;
  - an independent review.

  — [TÜV NORD CERT CBAM Leistungsbeschreibung](https://www.tuev-nord.de/fileadmin/Sites/TUEV_NORD/Dienstleistungen/Certification/Files/Leistungsbeschreibungen/tuev-nord-cert-CBAM-leistungsbeschreibung.pdf)
- SGS (May 2026) promotes "pre-verification" and advises producers to have assumptions challenged early. This is marketing from a firm that sells the service. — [SGS](https://www.sgs.com/news/2026/05/cbam-pre-verification-changing-the-narrative)

### Inferences
- **What verifiers will probably reject:**
  - an emission value, EF choice or allocation produced by an LLM with no documented, repeatable method in the monitoring plan;
  - any number whose source documents can't be sampled;
  - non-deterministic outputs: a re-run gives a different answer, so the verifier can't re-perform it;
  - an LLM that both enters and "checks" data, which breaks segregation of duties;
  - LLM-picked default values that aren't disclosed.
- **Implication for carbonTraceAI:** the existing raw_ref provenance chain and deterministic engine are the verifier-facing asset. Agents should only produce candidates that pass through a deterministic, logged, human-approved step before entering the canonical store.
- An AI layer probably raises the inherent-risk rating ("complex data management systems"), and with it the sampling effort and verification cost. It does not lower them, unless it comes with documented IT quality assurance (tests, versioning, eval results). **[SPECULATIVE; no verifier has published a position]**
- Who gets verified matters for product design. Verification attaches to the third-country operator's (installation's) emissions report. The African manufacturer, not the EU importer, is the one whose data flows and IT systems get audited.

### Gaps
- I found no published position from TÜV, DNV, BV or SGS on accepting AI-extracted or AI-estimated data. Search returned nothing specific. Only primary engagement with verifiers would answer this.
- I did not read the full text of Implementing Regulation 2025/2546 on EUR-Lex. Findings rely on the Commission guidance's description of it.
- I did not check EA (European co-operation for Accreditation) CBAM-specific guidance documents, if any exist.

---

## 2. EU AI Act implications: is a CBAM agent high-risk? Transparency obligations? Timeline?

### Takeaway
A CBAM data-extraction or classification agent is very unlikely to be "high-risk" under the AI Act. Annex III lists biometrics, critical infrastructure safety, education, employment, essential services and credit, law enforcement, migration and justice, and emissions reporting fits none of them. The Digital Omnibus (Reg. (EU) 2026/1744, in force 27 July 2026) also pushed Annex III obligations to 2 Dec 2027. The Article 50 transparency duties have applied since 2 Aug 2026, though. A user-facing chat assistant must disclose that it is AI. The AI Act is a minor cost here. Verifier acceptance and GDPR-style data-transfer rules are the real constraints.

### Cited Findings
- **Omnibus status:** Parliament adopted the Digital Omnibus on AI on 16 June 2026 and the Council approved it on 29 June. It was published in the OJ on 24 July 2026 as Regulation (EU) 2026/1744 and entered into force on 27 July 2026. — [Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/eu-digital-omnibus-on-ai-enters-into-force); [FASI](https://fasi.eu/en/articles/news/29051-digital-omnibus-package.html); [Mondaq](https://www.mondaq.com/uk/new-technology/1823160/the-digital-omnibus-on-ai-enters-into-force-today)
- **New dates:**
  - stand-alone Annex III high-risk obligations move to 2 Dec 2027;
  - Annex I (product-embedded) obligations move to 2 Aug 2028;
  - Art. 50(2) watermarking for providers moves to 2 Dec 2026;
  - the other Art. 50 transparency obligations, including deployer duties, still apply from 2 Aug 2026.

  — [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/); [Hogan Lovells](https://www.hoganlovells.com/en/publications/eu-legislators-agree-to-delay-for-highrisk-ai-rules)
- **Art. 50 content (from the regulation text; I could not re-fetch it in this session):**
  - Art. 50(1): providers must ensure AI systems that interact directly with people tell them they are dealing with AI.
  - Art. 50(4): deployers must disclose AI-generated text published to inform the public on matters of public interest, unless it has had human review and someone holds editorial responsibility.

  — [AI Act Art. 50](https://artificialintelligenceact.eu/article/50/); [Regulation (EU) 2024/1689 on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

### Inferences
- **Classification:** extracting supplier documents, suggesting CN codes, and drafting evidence packs is not an Annex III use case, so the system would be "limited/minimal risk". **[Inference from Annex III scope; no legal opinion found that addresses CBAM tools specifically]**
- **Article 50 duties:** a chat assistant explaining results needs an "you are interacting with AI" disclosure. AI-drafted text placed in verifier packs is not "published to inform the public", so 50(4) probably doesn't apply. Labelling AI-drafted content inside the product is still good practice for verifier trust.
- **Real regulatory risk:** this sits outside the AI Act.
  - CBAM verification (section 1) needs explainability.
  - Personal-data transfer rules in African jurisdictions apply (section 5).
  - The customer's own liability is at stake: the EU declarant carries penalties for incorrect declarations.
- **GPAI obligations:** these fall on model providers (e.g., Anthropic, OpenAI), not on carbonTraceAI as a downstream deployer/integrator. **[Inference]**

### Gaps
- I did not verify the final OJ text of 2026/1744 myself. Dates come from law-firm summaries, which agree with each other.
- I found no Commission guidance or legal commentary specifically classifying ESG or emissions-reporting AI under the AI Act.

---

## 3. Evidence on LLM reliability for the relevant subtasks

### Takeaway
The evidence splits cleanly by task.
- **Numeric calculation:** LLMs should never do it. Performance is fragile when numbers change, and the deterministic engine already exists.
- **HS/CN classification:** state-of-the-art LLMs are weak at 10-digit codes (≈25–40%) and moderate at 6-digit codes (≈30–58%). Suggestions need constraints and human confirmation.
- **Emission-factor matching:** this is the strongest documented LLM use case (Parakeet ≈87–88% top-1, 93% top-10). Note that this is LCA/Scope 3 spend-to-EF matching, not CBAM, where defaults are fixed by law.
- **Document extraction:** LLMs/VLMs score about 85–91 on composite key-field benchmarks. Line-item tables are much worse. No neutral head-to-head with OCR+rules exists.
- **Regulatory Q&A:** even commercial RAG legal tools hallucinate 17–33% of the time.

### Cited Findings
**Numeric reasoning**
- Apple's GSM-Symbolic (Oct 2024, 25 models) found that LLMs are "very sensitive to changes in numerical values". Adding one irrelevant but plausible clause caused accuracy drops of up to 65% across state-of-the-art models. — [arXiv 2410.05229](https://arxiv.org/html/2410.05229v2)
- Caveat: this predates the latest reasoning models, and the authors' "no genuine reasoning" claim is a hypothesis. Press coverage gives drop ranges (0.3–9.2% and 17.5–65.7%) that I could not verify against the paper. — [TechRadar](https://www.techradar.com/computing/artificial-intelligence/apples-latest-study-proves-that-ai-cant-even-solve-basic-grade-school-math-problems)

**HS code classification**
- The ATLAS benchmark (NeurIPS 2025) has 18,731 US CROSS rulings and 2,992 codes. A fine-tuned LLaMA-3.3-70B reached about 40% fully correct 10-digit and 57.5% correct 6-digit classifications. That was 15 points above GPT-5-Thinking and 27.5 points above Gemini-2.5-Pro-Thinking. The fine-tuned model was about 5× cheaper than GPT-5-Thinking and could be self-hosted. — [arXiv 2509.18400](https://arxiv.org/abs/2509.18400); [NeurIPS](https://neurips.cc/virtual/2025/129845)
- A 2026 paper argues that end-to-end LLM prompting fails at HS classification and proposes a "deterministic agentic workflow" with rule reasoning. It also found that a non-trivial share of HSCodeComp benchmark labels deviate from HS general rules, so the benchmarks themselves are noisy. — [arXiv 2605.14857](https://arxiv.org/pdf/2605.14857)
- HSGraphAgent (ACL 2026) notes that unconstrained LLMs often produce codes that don't exist or are hierarchically inconsistent. It constrains the model with an HS knowledge graph. — [ACL Anthology](https://preview.aclanthology.org/ingest-acl/2026.acl-long.2072/)

**Emission-factor matching**
- Amazon's Parakeet (NeurIPS 2024 CCAI workshop) reported average Precision@1 of 88.4%. The later Amazon Science version reports 86.9% top-1 in fully automated mode and 93.1% for the correct EF appearing in the top 10, with human-readable justifications for expert review. — [Climate Change AI](https://www.climatechange.ai/papers/neurips2024/52); [Amazon Science](https://www.amazon.science/publications/parakeet-emission-factor-recommendation-for-carbon-footprinting-with-generative-ai)
- Watershed (vendor, self-reported) claims 98.9% "defensible mappings" on the Parakeet dataset of 275 mostly food items. It also says its scientists found errors in the benchmark's answer key. — [Watershed blog](https://watershed.com/blog/how-we-benchmark-and-measure-the-accuracy-of-watershed-ai-for-emissions-factor-mapping)
- Not verified this session: Amazon's earlier CaML and Flamingo papers (zero-shot semantic matching for LCA). Searches returned nothing on them; see Gaps.

**Document extraction**
- Nanonets' IDP Leaderboard (a vendor benchmark) gives the top key-information-extraction (KIE) score as 91.10 (Gemini-3-Flash). It does not break out traditional OCR engines such as Textract or Azure. — [Nanonets IDP Leaderboard](https://nanonets.com/blog/idp-leaderboard-1-5/); [benchmarking.nanonets.com](https://benchmarking.nanonets.com/)
- A single-author test found one tool at 83.8% accuracy without line items, falling to 68.1% with tables. — [HackerNoon](https://hackernoon.com/can-your-llm-handle-an-invoice-i-tested-5heres-the-truth)
- Vendor claims conflict:
  - one says LLM extraction costs $0.10–$0.50 per document at 90–97% accuracy, against 85–92% for OCR on known formats ([RaftLabs](https://raftlabs.com/blog/ocr-vs-llm-invoice-processing));
  - another claims 85–95% for OCR against 97–99% for LLMs ([invoicedataextraction.com](https://invoicedataextraction.com/blog/invoice-ocr-accuracy-developer-guide)).

  Neither publishes its data.

**Regulatory/legal Q&A**
- Stanford RegLab/HAI ("Hallucination-Free?", 2024/2025) found commercial RAG legal tools hallucinating 17% (Lexis+ AI) to 33% (Westlaw AI-Assisted Research) of the time, against about 43% for GPT-4 without retrieval. Incomplete answers ran 18%, 25% and 62% across the tools. The vendors dispute the error taxonomy. The researchers say the rates are not population estimates; their point was that RAG has not eliminated hallucination. — [Stanford HAI](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-queries); [Stanford RegLab](https://reglab.stanford.edu/?p=3154); [LLRX](https://www.llrx.com/2026/02/what-the-science-says-about-hallucinations-in-legal-research/)

### Inferences
- **Error budget against materiality:** a 5% materiality level per CN code is tight. A 1-in-10 extraction error on a fuel invoice or electricity bill, if it isn't caught, can easily breach 5% of specific embedded emissions for a good. LLM extraction is acceptable only when each field is validated: cross-footing totals, unit checks, comparing against ERP quantities, and a human confirming low-confidence fields.
- **CN mapping:** with 6-digit accuracy around 40–60%, autonomous CN assignment is unacceptable. A "top-k suggestions + rationale + human confirm" UX is reasonable. The CBAM scope list (Annex I goods) is a small, closed set of CN codes, which makes a constrained classifier much easier than open HS classification. **[SPECULATIVE; I found no CBAM-specific benchmark]**
- **EF matching:** this is the most-cited AI success story in carbon accounting, but CBAM leaves less room for it than Scope 3. EFs and defaults come from the Methodology Act and Default Values Act, with priority rules the calc engine already encodes. The agent's value is mapping messy ERP item names to the right material/precursor category. The factor value itself must not be chosen by the agent.
- **Regulatory Q&A:** a 17–33% hallucination rate in a mature RAG legal product is disqualifying for authoritative compliance answers. Use it only with verbatim citations to EUR-Lex articles, and show the citation, not the paraphrase.

### Gaps
- I found no neutral benchmark of LLM vs OCR+rules on utility bills, fuel invoices or mill test certificates of the kind found in African manufacturing (scanned, multilingual, stamped). carbonTraceAI must build its own labelled eval set.
- I did not retrieve the CaML/Flamingo papers or Climatiq's published accuracy figures.
- I found no CBAM-scoped CN-classification benchmark.

---

## 4. Enterprise adoption reality: do agent projects deliver value?

### Takeaway
The best available evidence says most agentic and GenAI projects do not yet deliver measurable P&L value.
- Gartner predicts more than 40% of agentic AI projects will be cancelled by end-2027.
- McKinsey finds only 39% of firms report any enterprise-level EBIT impact from AI, and most of those put it under 5%.
- MIT NANDA's "95% get no return" headline is methodologically weak, but it is directionally consistent with the others.

The common failure pattern is hype-driven, misapplied agents with escalating costs and inadequate risk controls. That warns specifically against "agentifying" a workflow that deterministic code already handles.

### Cited Findings
**Gartner**
- Gartner (press release, 25 June 2025) predicts more than 40% of agentic AI projects will be cancelled by end of 2027 due to "escalating costs, unclear business value or inadequate risk controls". Analyst Anushree Verma called most projects early-stage experiments "mostly driven by hype" and "often misapplied". — [Gartner newsroom](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)
- Gartner estimates only about 130 of the thousands of "agentic AI" vendors are real. The rest is "agent washing", i.e. rebranded RPA, chatbots and assistants. In a January 2025 poll of 3,412 webinar attendees, 19% had made significant agentic investments and 42% conservative ones. — [Gartner newsroom](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)

**McKinsey**
- In McKinsey's State of AI 2025, 88% of respondents report regular AI use in at least one function, but only 39% report any enterprise-level EBIT impact, and most of those say it is under 5% of EBIT. 62% are at least experimenting with agents. — [McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-state-of-ai-2025)
- A secondary summary says 23% are scaling agentic AI somewhere and no more than 10% in any single function. I could not verify this on McKinsey's page (the fetch timed out). — [rajnandan.com summary](https://rajnandan.com/posts/mckinsey-state-of-ai-2025-analysis/)
- About one-third of all respondents have begun scaling AI. That rises to nearly half in firms with revenue above $5bn, against 29% in firms with revenue below $100m. Small firms lag. — [McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-state-of-ai-2025)

**MIT NANDA**
- MIT NANDA's "GenAI Divide" (July/Aug 2025) claims 95% of organisations see no measurable P&L return from $30–40bn of GenAI spend. — [Virtualization Review](https://virtualizationreview.com/Articles/2025/08/19/MIT-Report-Finds-Most-AI-Business-Investments-Fail-Reveals-GenAI-Divide.aspx)
- Critics say the 95% figure is unsupported: a small sample (52 organisations interviewed, 153 survey responses from conferences), no disclosure of who those organisations are, and "no P&L impact" treated as failure. — [critique mirror](https://neonvagabond.xyz/mirrors/mit-report-lacks-evidence.html); [Rob Lee Substack](https://robtlee73.substack.com/p/the-genai-divide-report-a-masterclass)

**Anthropic engineering guidance**
- "Building effective agents" (19 Dec 2024) recommends "finding the simplest solution possible, and only increasing complexity when needed". It says many tasks need only a single LLM call with retrieval. It also warns that agent autonomy brings higher costs and "the potential for compounding errors". The guidance draws this line:
  - workflows (predefined code paths) suit well-defined tasks where predictability matters;
  - agents suit open-ended problems.

  — [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)

### Inferences
- **Anthropic's taxonomy applied to CBAM:** CBAM compliance is mostly a well-defined, predictable task: ingest, calculate per legally fixed formulas, render the XML schema. That is the "workflow" or "no LLM" case. True open-ended agent loops fit only the parts with unpredictable steps, such as chasing suppliers for missing precursor data.
- **Fundraising and positioning risk:** "agentic" is now a credibility risk with sophisticated buyers and investors, given Gartner's "agent washing" framing. Positioning on "verifiable, deterministic, audit-ready, with AI assist for data capture" is likely stronger. **[SPECULATIVE]**

### Gaps
- I found no data on agent project success rates for compliance/ESG software specifically, or for SMEs in emerging markets.
- The McKinsey 2026 edition was not checked.

---

## 5. The buyer perspective of SMEs in emerging markets

### Takeaway
Evidence is thin, but structurally it points against "AI-first" as the selling point. SME buyers need cheap, verifier-accepted outputs. Sending ERP and invoice data to US LLM APIs raises cross-border data-transfer questions under Nigerian, Kenyan and South African law, and Nigeria is actively enforcing. Smaller firms also lag in scaling AI. The value proposition that survives is "less manual data entry and supplier chasing", delivered with optional or self-hostable models.

### Cited Findings
- **Nigeria:**
  - The NDPC fined MultiChoice Nigeria NGN 766,242,500 (2024), partly for unlawful cross-border transfers, and imposed a USD 32.8m remedial fee on Meta.
  - Nigeria has no published adequacy list under the GAID 2025 regime, so transfers are assessed case by case.
  - Sector rules (e.g., central bank) can be stricter.

  — [Mondaq (Nigeria)](https://www.mondaq.com/nigeria/privacy-protection/1798234/cross-border-data-transfers-and-international-compliance-legal-opportunities-in-global-tech-transactions)
- **Kenya:** Kenya's Data Protection Act (2021 General Regulations, reg. 40) allows transfers on appropriate safeguards, adequacy, necessity or consent. — [Mondaq / secondary](https://www.mondaq.com/nigeria/privacy-protection/1798234/cross-border-data-transfers-and-international-compliance-legal-opportunities-in-global-tech-transactions)
- **South Africa:** POPIA allows transfers to jurisdictions with substantively similar protection, with consent, or where necessary for a contract. — [BBD Software](https://bbdsoftware.com/article/data-residency-sovereignty-what-african-and-eu-firms-must-know/)
- **Regional view:** African states are not rejecting cross-border flows but want them on "sovereignty-preserving terms". Frameworks increasingly reference adequacy, SCCs and BCRs. — [Future of Privacy Forum](https://fpf.org/blog/cross-border-data-flows-in-africa-examining-policy-approaches-and-pathways-to-regulatory-interoperability/)
- **Cost and hosting:** a fine-tuned open model for HS classification was about 5–8× cheaper than frontier reasoning models and self-hostable "for data privacy". — [ATLAS arXiv 2509.18400](https://arxiv.org/abs/2509.18400)
- **LLM extraction cost:** a vendor estimate puts it at $0.10–$0.50 per document (unverified vendor claim). — [RaftLabs](https://raftlabs.com/blog/ocr-vs-llm-invoice-processing)
- **Firm size:** smaller firms (revenue under $100m) scale AI less often than large firms (29% vs nearly half). — [McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-state-of-ai-2025)

### Inferences
- **Personal data:** most CBAM data (fuel, electricity, tonnage, precursors) is not personal data. Invoices and supplier correspondence contain names and contacts, though, and ERP exports may too. A design that redacts or pseudonymises before any external LLM call, or offers a regional or self-hosted model, removes a sales objection. **[Inference]**
- **Commercial secrecy:** installation-level emissions and production volumes are commercially sensitive. Buyers may fear their data being used for model training even where the law allows the transfer. Contractual zero-retention is necessary. **[SPECULATIVE; no SME survey found]**
- **Unit economics:** the volume is small; a typical SME exporter has perhaps tens to hundreds of CBAM-relevant documents per quarter. Inference cost is therefore not the binding constraint. Engineering and eval maintenance cost, and verifier friction, are. **[SPECULATIVE; no volume data found]**
- **Connectivity and languages:** French, Arabic and Portuguese invoices, and scanned or stamped documents, are where VLM extraction may beat Tesseract plus rules. That is a concrete, testable reason to add an LLM extraction step. **[SPECULATIVE; test on own data]**

### Gaps
- I found no survey of African or emerging-market SME trust in AI for compliance.
- I found no CBAM SaaS price-point benchmarks for this segment.
- I found no data on connectivity constraints affecting cloud-LLM features.
- Nigeria National Cloud Policy (Oct 2025) residency claims could not be verified from primary sources.

---

## 6. Where agents plausibly add value vs. where they must not be used

### Takeaway
LLMs help at the messy, unstructured edges: getting data in, mapping it, chasing it, and explaining it. They hurt anywhere in the regulated core, which covers calculation, factor/default selection, allocation, reconciliation, and the final XML or declaration. Most of the value is in bounded LLM steps inside deterministic workflows, not autonomous agents. A genuine multi-step agent is justified only for supplier data collection and chasing.

### Cited Findings
- Verifier risk factors (manual transfers, complex data systems, incorrect EF use, incorrect precursor identification, missing segregation of duties) show where errors arise today and where automation can either help or add risk. — [Commission Guidance, risk analysis](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)
- When precursor producers do not supply data, operators fall back to default values as the "very last resort". Supplier non-response is therefore a direct driver of worse (default-based, often penalising) outcomes. — [Commission Guidance §2](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)
- EF and category matching with human-reviewable ranked lists and justifications is the best-evidenced AI use in carbon accounting (Parakeet: 93% top-10). — [Amazon Science](https://www.amazon.science/publications/parakeet-emission-factor-recommendation-for-carbon-footprinting-with-generative-ai)
- Classification gets substantially better when deterministic rules or knowledge graphs constrain the LLM, compared with free generation. — [arXiv 2605.14857](https://arxiv.org/pdf/2605.14857); [HSGraphAgent](https://preview.aclanthology.org/ingest-acl/2026.acl-long.2072/)

### Inferences
The framework below is my synthesis. Value and risk ratings are judgement calls based on the evidence above.

| Task | Use LLM? | Pattern | Rationale |
|---|---|---|---|
| Supplier data request, chasing and follow-up (emails/WhatsApp in local languages, parsing replies) | **Yes: the one true agent case** | Agent drafts; human approves sends (sending messages needs consent); replies parsed into candidate records | Open-ended, multi-turn, unpredictable steps. Non-response drives costly defaults. Low regulatory risk if parsed values are human-confirmed |
| Unstructured document extraction (utility bills, fuel invoices, mill certs, multilingual scans) | **Yes, as a bounded step** | VLM extraction → schema validation → deterministic cross-checks (totals, units, ERP match) → human confirms low-confidence fields; raw_ref to page/bbox | Benchmarks show high but imperfect accuracy, with table/line-item weakness. The 5% materiality level demands validation |
| Mapping messy ERP item masters to CN codes and CBAM goods/precursor categories | **Yes, as suggestions** | Constrained to the closed CBAM Annex I CN list; top-k + rationale; human confirms; mapping table versioned, then reused deterministically | Best ATLAS model reaches only ~40% at 10-digit and ~58% at 6-digit. A constrained closed set helps. Mapping is one-time, reusable master data |
| Regulatory change tracking (EUR-Lex, Commission FAQ/guidance updates) | **Maybe** | Deterministic feed/diff watcher; LLM summarises the diff with verbatim citations; human reviews before any rule/engine change | Hallucination rates of 17–33% in legal RAG mean summaries are pointers only. Engine changes stay code-reviewed |
| Drafting verifier evidence packs and monitoring-plan narrative | **Yes, as drafts** | LLM assembles narrative from provenance graph and calc logs; every number pulled by tool from the store, never generated; human signs off | Saves consultant time. Numbers stay deterministic |
| Explaining results to users ("why is my SEE 2.3 t/t?") | **Yes** | Explanation grounded in calc trace; Art. 50 AI disclosure | Low risk if it is read-only over deterministic outputs |
| Anomaly triage (outliers, YoY swings, ERP vs invoice mismatch) | **Hybrid** | Deterministic statistical/rule detection; LLM only proposes explanations or next actions | Verifiers look for exactly these outliers. Detection must be reproducible |
| Emission calculation, uncertainty, allocation, reconciliation | **No** | Existing deterministic engine | LLM numeric fragility; verifier must be able to re-perform |
| Selecting EF/default values or the methodology tier | **No (suggest at most, with disclosure)** | Priority rules in code per the Methodology Act and Default Values Act | Verifiers must check that the correct default was selected. Undisclosed AI choice is a non-conformity risk |
| Final XML/declaration submission to the CBAM Registry | **No** | Deterministic renderer + human approval | Irreversible, legally attributable act |

- **Estimated agent share of the product: about 10%.** I estimate that ~80–90% of carbonTraceAI's verifier-facing value already sits in the deterministic stack. Marginal LLM value is concentrated in data capture, which is the stated bottleneck for SMEs. **[SPECULATIVE]**
- **Don't-build list:** a "CBAM copilot" that answers regulatory questions or computes emissions conversationally. It adds hallucination liability without reducing verifier workload.

### Gaps
- I found no quantified data on how much time CBAM operators spend on supplier chasing compared with document extraction, which would size each opportunity. Other researchers' pain-point notes in this folder may cover it.

---

## 7. Design patterns for safe agents in regulated workflows

### Takeaway
The defensible pattern is simple: deterministic workflow first, with LLM calls as narrow, tool-constrained steps that emit *candidates*, never committed facts. Required pieces are human approval gates, confidence thresholds with abstention, immutable logs of model, prompt and version, reproducibility via stored outputs, and a domain eval set re-run on every model change. These map directly onto what the Commission guidance says verifiers check: IT system QA, segregation of duties, audit trail, and conservative gap-filling.

### Cited Findings
- Anthropic's guidance covers five practices:
  - prefer workflows with predefined code paths for well-defined tasks;
  - give agents "ground truth" from the environment (tool results) at each step;
  - add human checkpoints;
  - set stopping conditions;
  - test extensively in sandboxes with guardrails.

  — [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Verifiers check that IT systems are "designed, documented, tested, implemented, controlled and maintained". They also check for segregation of data input from data checking, and for functioning automated controls. — [Commission Guidance (~pp.52–55)](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)
- Data gaps must be closed with conservative estimates that don't underestimate emissions. Estimation methods should be pre-defined in the monitoring plan. — [Commission Guidance §4.8](https://eurometal.net/wp-content/uploads/Guidance-on-CBAM-verification-and-accreditation-for-verifiers-and-national-accreditation-bodies.pdf)
- A "deterministic agentic workflow" with interpretable rule-based decisions beat end-to-end LLM prompting on HS classification. — [arXiv 2605.14857](https://arxiv.org/pdf/2605.14857)

### Inferences
Concrete pattern for carbonTraceAI:
1. **Candidate/commit separation.** LLM outputs land in a `candidates` table with status `proposed`. Only a human action, or a deterministic validator above threshold for low-risk fields, promotes them to the canonical store. The human approver is a different role from the uploader, which preserves segregation of duties.
2. **Provenance extension.** Extend raw_ref to record:
   - source doc hash, page and bbox;
   - model ID and version, and the prompt template version;
   - the raw model output;
   - confidence;
   - approver and timestamp.

   Records are append-only. Never re-run a model to "reproduce": the stored output is the evidence.
3. **Tools for all numbers.** Agents call the calc engine, EF lookup and validators as tools and never emit numbers themselves. Evidence-pack drafts embed values by reference (template variables), not as generated text.
4. **Confidence thresholds and abstention.** Below threshold, a field is routed to a human. Missing data is never filled by an LLM guess. It goes to supplier chasing or to a documented conservative default, flagged as such in the XML/report.
5. **Disclosure.** Mark AI-assisted fields in the verifier evidence pack, so the verifier can target sampling. This turns AI from a hidden risk into a documented control.
6. **Eval set as product asset.** Build a labelled set of real customer document types, for example 200–500 utility bills, invoices, mill certificates and ERP item lines. Track field-level accuracy, CN top-k accuracy and abstention rate. Re-run it on every model or prompt change and include the results in IT-QA documentation for verifiers. **[Sizes are my suggestion]**
7. **Data minimisation.** Redact personal data before external API calls. Keep a self-hosted or regional model fallback for clients with sovereignty requirements, and use zero-retention contracts.
8. **Kill criteria.** If the LLM step doesn't beat the existing pdfplumber+Tesseract+rules pipeline on the eval set by a pre-agreed margin, considering both field accuracy and human review time, don't ship it. This is the direct antidote to the Gartner failure modes of "unclear business value" and "escalating costs".

### Gaps
- I found no published verifier or NAB acceptance criteria for AI-assisted data capture, so whether disclosure-plus-HITL is enough is untested. Recommended action: run a pre-verification dry-run with one accredited verifier (e.g., via SGS/TÜV pre-verification offers) before building agent features.
- I found no case studies of CBAM or EU ETS operators whose AI-assisted data passed or failed verification.
