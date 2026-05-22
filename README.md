# Social Media Sentiment Analysis (Streamlit)

An interactive Streamlit app to analyze sentiment (positive/neutral/negative) for social media posts using **VADER**.

## Features
- Paste a post/tweet/comment → sentiment + score + details
- Upload files:
  - **CSV**: pick text column → analyze → download results
  - **Excel (XLSX/XLS)**: pick sheet + text column → analyze → download results
  - **JSON**: extracts strings (best-effort) → analyze → download results
  - **TXT / MD / LOG**: analyze file text
  - **PDF / DOCX**: extract text → analyze
- Interactive charts (Plotly): bar, pie/donut, histogram, box plot
- Optional trend line if a date/time column exists (`date`, `timestamp`, `created_at`, etc.)

---

## Project structure
```
sentiment_app/
  app.py
  requirements.txt
  README.md
```

## Run locally (recommended)

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Use on other devices (same Wi‑Fi)
By default, `localhost` works only on your computer. To open from your phone/other laptop on the same network:
```bash
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
Then open:
```
http://<YOUR_PC_IPV4>:8501
```
To find your IP on Windows: run `ipconfig` and look for **IPv4 Address**.

## Hosting options
### Option A: Streamlit Community Cloud (easiest)
1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Deploy with main file path: `sentiment_app/app.py`

### Option B: VPS (DigitalOcean/AWS/etc.)
Run:
```bash
pip install -r requirements.txt
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
Open port **8501** (firewall/security group). For production, put Nginx + HTTPS in front.

### Option C: ngrok (quick public URL from your PC)
1. Start the app:
```bash
python -m streamlit run app.py --server.port 8501
```
2. In another terminal:
```bash
ngrok http 8501
```

---

## Notes
- First run may download the NLTK VADER lexicon automatically.
- If you get `streamlit is not recognized`, use `python -m streamlit ...` (as shown above).
