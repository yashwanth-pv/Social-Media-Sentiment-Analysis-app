import re
import json
import os
from typing import Optional, Tuple

import pandas as pd
import streamlit as st
import plotly.express as px


def _ensure_vader() -> None:
    """
    Ensure VADER lexicon is available. This may download once on first run.
    """
    import nltk

    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


@st.cache_resource
def _get_analyzer():
    _ensure_vader()
    from nltk.sentiment import SentimentIntensityAnalyzer

    return SentimentIntensityAnalyzer()


def _clean_text(text: str) -> str:
    # Light cleaning suited for social media: normalize whitespace, keep emojis,
    # remove repeated spaces, strip.
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text


def predict_sentiment(text: str) -> Tuple[str, float]:
    """
    Returns (label, compound_score)
    label: positive/neutral/negative
    """
    analyzer = _get_analyzer()
    cleaned = _clean_text(text)
    scores = analyzer.polarity_scores(cleaned)
    compound = float(scores["compound"])

    # Common VADER thresholds
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, compound


def analyze_dataframe(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    out = df.copy()
    out[text_col] = out[text_col].astype(str).fillna("")
    preds = out[text_col].apply(predict_sentiment)
    out["sentiment"] = preds.apply(lambda x: x[0])
    out["sentiment_score"] = preds.apply(lambda x: x[1])
    return out


def pick_text_column(df: pd.DataFrame) -> Optional[str]:
    if df.empty:
        return None
    # Prefer common names
    preferred = ["text", "tweet", "post", "content", "message", "comment", "body"]
    cols = [c for c in df.columns if df[c].dtype == "object" or str(df[c].dtype).startswith("string")]
    for p in preferred:
        for c in cols:
            if c.lower() == p:
                return c
    return cols[0] if cols else None


def render_charts(result: pd.DataFrame) -> None:
    """
    Render multiple charts for sentiment outputs.
    Expects columns: sentiment, sentiment_score
    Optional: tries to detect a date/time column for trend chart.
    """
    if result.empty:
        st.warning("No rows to chart.")
        return

    # Plotly charts are more interactive (zoom/pan, hover, legend toggles).
    # Ensure types
    df = result.copy()
    df["sentiment_score"] = pd.to_numeric(df.get("sentiment_score"), errors="coerce")

    # --- Filters (interactive) ---
    with st.expander("Filters", expanded=False):
        sentiment_options = [s for s in ["positive", "neutral", "negative"] if s in df["sentiment"].unique()]
        selected_sentiments = st.multiselect(
            "Sentiments",
            options=sentiment_options,
            default=sentiment_options,
        )

        score_min = float(df["sentiment_score"].min()) if df["sentiment_score"].notna().any() else -1.0
        score_max = float(df["sentiment_score"].max()) if df["sentiment_score"].notna().any() else 1.0
        score_range = st.slider(
            "Compound score range",
            min_value=-1.0,
            max_value=1.0,
            value=(max(-1.0, score_min), min(1.0, score_max)),
            step=0.01,
        )

    filtered = df[df["sentiment"].isin(selected_sentiments)].copy()
    filtered = filtered[filtered["sentiment_score"].between(score_range[0], score_range[1], inclusive="both")]

    if filtered.empty:
        st.warning("No rows match the current filters.")
        return

    color_map = {"positive": "#22c55e", "neutral": "#94a3b8", "negative": "#ef4444"}

    # --- Counts ---
    counts = (
        filtered["sentiment"]
        .value_counts()
        .reindex(["positive", "neutral", "negative"])
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    counts.columns = ["sentiment", "count"]

    st.subheader("Charts (interactive)")

    c1, c2 = st.columns(2)
    with c1:
        fig_bar = px.bar(
            counts,
            x="sentiment",
            y="count",
            color="sentiment",
            color_discrete_map=color_map,
            text="count",
            title="Sentiment count",
        )
        fig_bar.update_layout(legend_title_text="", dragmode="zoom")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        fig_pie = px.pie(
            counts,
            names="sentiment",
            values="count",
            color="sentiment",
            color_discrete_map=color_map,
            hole=0.45,
            title="Sentiment share",
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(legend_title_text="")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Score distribution ---
    c3, c4 = st.columns(2)
    with c3:
        fig_hist = px.histogram(
            filtered.dropna(subset=["sentiment_score"]),
            x="sentiment_score",
            color="sentiment",
            color_discrete_map=color_map,
            nbins=30,
            title="Score distribution (histogram)",
        )
        fig_hist.update_layout(bargap=0.05, dragmode="zoom", legend_title_text="Sentiment")
        st.plotly_chart(fig_hist, use_container_width=True)

    with c4:
        fig_box = px.box(
            filtered.dropna(subset=["sentiment_score"]),
            x="sentiment",
            y="sentiment_score",
            color="sentiment",
            color_discrete_map=color_map,
            title="Score distribution (box plot)",
            points="outliers",
        )
        fig_box.update_layout(dragmode="zoom", legend_title_text="")
        st.plotly_chart(fig_box, use_container_width=True)

    # --- Optional trend chart if a datetime column exists ---
    candidate_cols = ["created_at", "timestamp", "time", "date", "datetime", "posted_at"]
    dt_col = None
    for c in result.columns:
        if c.lower() in candidate_cols:
            dt_col = c
            break

    if dt_col is not None:
        tmp = filtered[[dt_col, "sentiment_score"]].copy()
        tmp[dt_col] = pd.to_datetime(tmp[dt_col], errors="coerce")
        tmp["sentiment_score"] = pd.to_numeric(tmp["sentiment_score"], errors="coerce")
        tmp = tmp.dropna(subset=[dt_col, "sentiment_score"])
        if len(tmp) >= 10:
            tmp["date"] = tmp[dt_col].dt.floor("D")
            daily = tmp.groupby("date", as_index=False)["sentiment_score"].mean()
            fig_trend = px.line(
                daily,
                x="date",
                y="sentiment_score",
                title=f"Sentiment trend (auto-detected '{dt_col}')",
                markers=True,
            )
            fig_trend.update_xaxes(rangeslider_visible=True)
            fig_trend.update_layout(dragmode="zoom")
            st.plotly_chart(fig_trend, use_container_width=True)


def _ext(filename: str) -> str:
    return os.path.splitext(filename or "")[1].lower().lstrip(".")


def extract_texts_from_upload(uploaded) -> Tuple[list[str], str]:
    """
    Returns (texts, source_hint)
    - texts: list of texts to analyze (each becomes one row)
    - source_hint: what was extracted (for UI)
    Supported:
      - txt/md/log: whole file
      - csv: select a text column
      - xlsx/xls: select sheet + text column
      - json: extracts strings from a list/dict (best-effort)
      - pdf: extracts all pages text into one string
      - docx: extracts all paragraphs into one string
    """
    name = getattr(uploaded, "name", "uploaded_file")
    ext = _ext(name)

    # Text-like files
    if ext in {"txt", "md", "log"}:
        raw = uploaded.getvalue()
        text = raw.decode("utf-8", errors="ignore")
        return [text], f"{ext.upper()} text"

    # PDF
    if ext == "pdf":
        from pypdf import PdfReader

        reader = PdfReader(uploaded)
        parts = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        text = "\n".join(parts).strip()
        return [text], "PDF extracted text"

    # DOCX
    if ext == "docx":
        import docx  # python-docx

        d = docx.Document(uploaded)
        text = "\n".join([p.text for p in d.paragraphs]).strip()
        return [text], "DOCX extracted text"

    # JSON
    if ext == "json":
        raw = uploaded.getvalue()
        data = json.loads(raw.decode("utf-8", errors="ignore") or "{}")

        texts: list[str] = []

        def walk(x):
            if x is None:
                return
            if isinstance(x, str):
                if x.strip():
                    texts.append(x)
                return
            if isinstance(x, (int, float, bool)):
                return
            if isinstance(x, list):
                for i in x:
                    walk(i)
                return
            if isinstance(x, dict):
                for v in x.values():
                    walk(v)
                return

        walk(data)
        # Keep it reasonable
        texts = texts[:2000]
        return texts if texts else [""], "JSON extracted strings"

    # CSV
    if ext == "csv":
        df = pd.read_csv(uploaded)
        return [], "CSV (select column in UI)", df  # type: ignore[return-value]

    # Excel
    if ext in {"xlsx", "xls"}:
        # pandas will use openpyxl for xlsx. For xls you may need extra engines on some systems.
        xl = pd.ExcelFile(uploaded)
        return [], "Excel (select sheet + column in UI)", xl  # type: ignore[return-value]

    raise ValueError(f"Unsupported file type: .{ext if ext else '(no extension)'}")


st.set_page_config(page_title="Social Media Sentiment Analysis", page_icon="📊", layout="wide")

st.title("Social Media Sentiment Analysis")
st.caption("Paste text or upload a file to analyze sentiment (positive/neutral/negative) using VADER.")

tab_single, tab_files = st.tabs(["Analyze text", "Upload files"])

with tab_single:
    st.subheader("Analyze a single post")
    text = st.text_area(
        "Paste a post/tweet/comment",
        height=160,
        placeholder="E.g. I love this new update! 🔥",
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        run = st.button("Analyze", type="primary", use_container_width=True)
    with col2:
        st.write("")

    if run:
        if not text.strip():
            st.warning("Please paste some text first.")
        else:
            label, score = predict_sentiment(text)
            st.metric("Sentiment", label.capitalize(), f"{score:+.3f} (compound)")
            st.write("**Details:**")
            analyzer = _get_analyzer()
            st.json(analyzer.polarity_scores(_clean_text(text)))

with tab_files:
    st.subheader("Upload a file (CSV / Excel / JSON / TXT / PDF / DOCX)")
    st.write(
        "Tip: For CSV/Excel, upload a dataset of posts and pick the column that contains the text."
    )

    uploaded = st.file_uploader(
        "Upload file",
        type=None,  # allow all; we validate by extension after upload
        accept_multiple_files=False,
    )

    if uploaded is not None:
        name = getattr(uploaded, "name", "uploaded_file")
        ext = _ext(name)

        try:
            extracted = extract_texts_from_upload(uploaded)
        except ValueError as e:
            st.error(str(e))
            st.stop()

        # Special handling for CSV / Excel where we need user selection
        if isinstance(extracted, tuple) and len(extracted) == 3:
            _, hint, obj = extracted  # type: ignore[misc]
            st.info(hint)

            if ext == "csv":
                df = obj  # type: ignore[assignment]
                st.write("Preview:")
                st.dataframe(df.head(20), use_container_width=True)

                suggested = pick_text_column(df)
                text_col = st.selectbox(
                    "Select the text column",
                    options=list(df.columns),
                    index=(list(df.columns).index(suggested) if suggested in df.columns else 0),
                )
                if st.button("Analyze file", type="primary"):
                    result = analyze_dataframe(df, text_col=text_col)

                    st.write("Results (preview):")
                    st.dataframe(result.head(50), use_container_width=True)

                    render_charts(result)

                    st.download_button(
                        "Download results as CSV",
                        data=result.to_csv(index=False).encode("utf-8"),
                        file_name="sentiment_results.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

            elif ext in {"xlsx", "xls"}:
                xl = obj  # type: ignore[assignment]
                sheet = st.selectbox("Select sheet", options=list(xl.sheet_names), index=0)
                df = xl.parse(sheet)

                st.write("Preview:")
                st.dataframe(df.head(20), use_container_width=True)

                suggested = pick_text_column(df)
                text_col = st.selectbox(
                    "Select the text column",
                    options=list(df.columns),
                    index=(list(df.columns).index(suggested) if suggested in df.columns else 0),
                )
                if st.button("Analyze file", type="primary"):
                    result = analyze_dataframe(df, text_col=text_col)

                    st.write("Results (preview):")
                    st.dataframe(result.head(50), use_container_width=True)

                    render_charts(result)

                    st.download_button(
                        "Download results as CSV",
                        data=result.to_csv(index=False).encode("utf-8"),
                        file_name="sentiment_results.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

            st.stop()

        # Non-table files: we already have texts list
        texts, hint = extracted  # type: ignore[assignment]
        st.success(f"Loaded: {name} • {hint}")

        if not any(t.strip() for t in texts):
            st.warning("No text found in this file (or it was empty).")
            st.stop()

        max_items = min(len(texts), 2000)
        if len(texts) > max_items:
            st.info(f"Analyzing first {max_items} extracted text items.")
            texts = texts[:max_items]

        df = pd.DataFrame({"text": texts})

        if st.button("Analyze file", type="primary"):
            result = analyze_dataframe(df, text_col="text")

            st.write("Results (preview):")
            st.dataframe(result.head(50), use_container_width=True)

            render_charts(result)

            st.download_button(
                "Download results as CSV",
                data=result.to_csv(index=False).encode("utf-8"),
                file_name="sentiment_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
