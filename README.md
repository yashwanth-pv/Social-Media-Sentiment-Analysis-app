# [Social Media Sentiment Analysis — App Guide](https://social-media-sentiment-analysis-app-0.streamlit.app/)

This Streamlit app analyzes sentiment (**positive / neutral / negative**) for social media text using **VADER**.

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/d8c187c6573c4475c48aec6f459bedf4f3bbc5da/Outputs/Screenshot%202026-05-28%20155439.png)

## 1) Analyze text
1. Open the **Analyze text** tab
2. Paste a post/tweet/comment
3. Click **Analyze**

You’ll get:
- Sentiment label (positive/neutral/negative)
- Compound score (from -1 to +1)
- Score breakdown details

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/d8c187c6573c4475c48aec6f459bedf4f3bbc5da/Outputs/Screenshot%202026-05-28%20155534.png)

## 2) Analyze uploaded files
Open the **Upload files** tab and upload any of these:

### Table files (you choose a text column)
- **CSV** (`.csv`)
- **Excel** (`.xlsx`, `.xls`) — select a sheet + a text column

### Text extraction files (auto-extract then analyze)
- **Text** (`.txt`, `.md`, `.log`)
- **JSON** (`.json`) — extracts strings (best-effort)
- **PDF** (`.pdf`) — extracts text from pages
- **DOCX** (`.docx`) — extracts paragraph text

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/d8c187c6573c4475c48aec6f459bedf4f3bbc5da/Outputs/Screenshot%202026-05-28%20163947.png)

After analysis, you’ll see:
- Results table preview
- Multiple **interactive charts** (zoom/pan, hover tooltips, legend toggles)
- A **Download results as CSV** button

## Charts
- **Bar chart**: sentiment counts
- **Donut chart**: sentiment share
- **Histogram**: score distribution
- **Box plot**: score distribution by sentiment
- **Trend line (auto)**: appears if a date/time column exists (e.g., `date`, `timestamp`, `created_at`)

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/d8c187c6573c4475c48aec6f459bedf4f3bbc5da/Outputs/Screenshot%202026-05-28%20155559.png)

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/d8c187c6573c4475c48aec6f459bedf4f3bbc5da/Outputs/Screenshot%202026-05-28%20155733.png)

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/999c88872b2c61e7d393c8a7d885b5948c1e1d4e/Outputs/Screenshot%202026-05-28%20155798.png)
