# [Social Media Sentiment Analysis — App Guide](https://social-media-sentiment-analysis-app-0.streamlit.app/)

This Streamlit app analyzes sentiment (**positive / neutral / negative**) for social media text using **VADER**.

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235249.png)

## 1) Analyze text
1. Open the **Analyze text** tab
2. Paste a post/tweet/comment
3. Click **Analyze**

You’ll get:
- Sentiment label (positive/neutral/negative)
- Compound score (from -1 to +1)
- Score breakdown details

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235404.png)

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

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235445.png)

After analysis, you’ll see:
- Results table preview
- Multiple **interactive charts** (zoom/pan, hover tooltips, legend toggles)
- A **Download results as CSV** button

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235523.png)

## Charts
- **Bar chart**: sentiment counts
- **Donut chart**: sentiment share
- **Histogram**: score distribution
- **Box plot**: score distribution by sentiment
- **Trend line (auto)**: appears if a date/time column exists (e.g., `date`, `timestamp`, `created_at`)

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235702.png)

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235741.png)

![image alt](https://github.com/yashwanth-pv/Social-Media-Sentiment-Analysis-app/blob/f3a2eb78a4d1f7c7022e8e431e57661b2d17f0f2/Outputs/Screenshot%202026-05-28%20235752.png)
