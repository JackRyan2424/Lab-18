from pathlib import Path
import json
import re
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
SKILL = ROOT
sys.path.insert(0, str(SKILL))
from edgar import fetch, table, METRICS, numeric, unsupported_numbers

OUTPUT = Path(__file__).resolve().parent
OUTPUT.mkdir(exist_ok=True)
st.set_page_config(page_title="Buffett business screen", layout="wide")
st.title("Buffett business screen")
st.caption("data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
with st.form("company"):
    ticker = st.text_input("Ticker", "COST").strip().upper()
    contact_name = st.text_input("Name", "Jack Ryan")
    contact_email = st.text_input("Email", "ryan307@purdue.edu")
    user_agent = f"{contact_name.strip()} {contact_email.strip()}"
    refresh = st.form_submit_button("Download latest SEC facts")
    st.form_submit_button("View saved report")
if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,14}", ticker):
    st.error("Enter a valid ticker.")
    st.stop()

@st.cache_data(ttl=3600, max_entries=20)
def load_sec(symbol, agent):
    return fetch(symbol, agent, OUTPUT)

if refresh:
    try:
        load_sec.clear()
        with st.spinner("Reading SEC EDGAR…"):
            load_sec(ticker, user_agent)
    except Exception as exc:
        st.error(f"SEC download failed: {exc}")
        st.stop()
report_path = OUTPUT / f"{ticker}-report.json"
if not report_path.exists():
    st.info("Enter your name and email, then download SEC facts. No estimates or substitute data are used.")
    st.stop()
report = json.loads(report_path.read_text(encoding="utf-8"))
st.subheader(report["company"])
st.caption(f"Saved SEC snapshot retrieved {report['retrieved_at']}. Download to refresh. USD millions unless indicated.")
chart = pd.DataFrame([{ "Fiscal year end": r["fiscal_year_end"],
    **{m.replace("_", " ").title(): r[m]["value"] / 1_000_000 if numeric(r[m]["value"]) else None
       for m in ("owner_earnings", "net_income")}} for r in report["rows"]])
st.line_chart(chart, x="Fiscal year end", y=["Owner Earnings", "Net Income"], y_label="USD millions", alt="Owner earnings and net income by fiscal-year-end date")
st.dataframe(pd.DataFrame(table(report)), hide_index=True, alt="Annual financial metrics; missing values remain explicit")
st.subheader("Buffett’s checks")
st.table(pd.DataFrame(report["checks"].items(), columns=["Check", "Result"]), hide_index=True, alt="Three code-computed Buffett checks")
with st.expander("XBRL tags and filing provenance"):
    provenance = [{"Fiscal year end": r["fiscal_year_end"], "Metric": m, **r[m]} for r in report["rows"] for m in METRICS]
    st.dataframe(pd.DataFrame(provenance).astype(str), hide_index=True, alt="Selected tags, periods, filing dates and accession numbers")
st.caption("Owner earnings = operating cash flow − capital spending. ROE uses year-end equity. These checks do not establish moat, management quality or a fair stock price.")
st.subheader("AI memo — Buffett-inspired simulation")
memo_path = OUTPUT / f"{ticker}-memo.md"
source_path = OUTPUT / f"{ticker}-memo-source.txt"
saved = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
if saved and (not source_path.exists() or source_path.read_text().strip() != report["facts_sha256"]):
    st.warning("This memo is not bound to the current SEC snapshot. Ask the AI to review it using the skill.")
if not saved:
    st.info(f"Ask your AI: Use $buffett-edgar on {ticker}, read its printed report, and save the memo.")
memo = st.text_area("Memo editor — try adding 40.0%", saved, height=220, key=f"memo-{ticker}-{report['facts_sha256']}")
flags = unsupported_numbers(memo, report)
if flags:
    st.error("Numbers the script did not print: " + "; ".join(f"{f['number']} (line {f['line']})" for f in flags))
elif memo:
    st.success("Every numeric token appears in the script’s displayed financial output. This checks presence, not meaning.")
st.markdown(memo)
decision_path = OUTPUT / f"{ticker}-decision.md"
decision = st.text_input("Your decision: Do you trust the verdict, and why?", decision_path.read_text(encoding="utf-8") if decision_path.exists() else "", key=f"decision-{ticker}")
if st.button("Save memo and my decision"):
    memo_path.write_text(memo, encoding="utf-8")
    decision_path.write_text(decision, encoding="utf-8")
    st.success("Saved. Any unsupported numbers remain flagged above.")
st.download_button("Download memo", memo + "\n\nMy decision: " + decision, file_name=f"{ticker}-memo.md", mime="text/markdown")
