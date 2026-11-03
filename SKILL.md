---
name: buffett-edgar
description: Evaluate a US ticker's business using a repeatable Buffett-inspired SEC 10-K screen, code-computed financials and an audited Markdown memo. Use for Buffett business-quality analysis without stock prices or valuation.
---

# Buffett business screen

Run the bundled `edgar.py`; never compute, estimate, fill, or transcribe financial values yourself. Use SEC EDGAR only, keyless. Do not install FAskills or use its providers. Require a real name and email in SEC_USER_AGENT before requesting SEC data.

From the project directory run:
`python <this-skill>/edgar.py COST --output .`
Replace COST with the requested ticker. Read the printed output and saved numbers file before judging. Preserve the raw facts, report JSON, and numbers Markdown for reproducibility. On network failure report the error; do not replace SEC with another provider. A saved snapshot can be used only if clearly identified as such.

The script selects only 10-K facts, annual flow periods including 52/53-week years, and the latest five annual fiscal-year-end dates. Do not label comparative data using the SEC fact's `fy`. Within each year's preferred tag the most recently filed fact wins. Revenue tags: RevenueFromContractWithCustomerExcludingAssessedTax, then Revenues. Net income: NetIncomeLoss. Operating cash flow: NetCashProvidedByUsedInOperatingActivities. Capital spending: PaymentsToAcquirePropertyPlantAndEquipment, then PaymentsToAcquireProductiveAssets. Equity: StockholdersEquity. No substitutions outside these priorities.

ROE is net income divided by year-end equity; owner earnings is operating cash flow minus capital spending. This is the assignment's proxy, not an estimate of maintenance capital expenditure. Missing source values and owner earnings print `not found`. Ratios with missing inputs or nonpositive equity print `not known`. All checks with missing required inputs print `not known`. Code tests ROE at least 15% each year, positive owner earnings each year, and last owner earnings greater than first. The growth check is not a requirement for monotonic annual growth.

Write `./<TICKER>-memo.md` in a concise Buffett-inspired first-person voice, explicitly identified as an AI simulation, never an authentic Buffett statement. Choose **own the business**, **watch it**, or **pass**, judging business quality only. Use only financial numbers literally printed in the report, including its units and dates; perform no additional arithmetic or forecasts. Avoid numeric scores, numbered lists, price data, target prices, valuation and margin-of-safety calculations. Explain what the checks support and what they cannot establish about moat, management or debt. Do not invent qualitative company facts; distinguish hypotheses from demonstrated evidence. If owner earnings are missing, say explicitly that you cannot judge owner earnings.

Use the qualitative philosophy from [FAskills Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): understandable businesses, durable advantages, trustworthy capital allocation and cash generation. Its valuation, prediction, data-provider and installation directions do not apply. The user's SEC rules supersede its owner-earnings formula.

Audit the memo:
`python <this-skill>/edgar.py COST --output . --audit-memo ./COST-memo.md`
Fix every flagged number. The checker validates numeric presence and units, not whether a number describes the correct metric; review that association yourself. Bind the memo to the report by saving the report's `facts_sha256` in `<TICKER>-memo-source.txt`. Never silently present an old memo against refreshed facts.

Ask the learner to add their own one-line trust decision below the memo; do not attribute an AI opinion to them. Run the Streamlit app with `python -m streamlit run app.py`. It displays saved reports, can fetch a new ticker, and audits editable memo text. A new ticker requires an AI-authored memo through this skill; the app does not turn the numeric checks into an automatic investment verdict.

Sources: [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills), [Streamlit](https://docs.streamlit.io/).
