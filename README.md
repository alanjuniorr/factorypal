# factorypal

## 🛠️ Setup & Installation

### 1️⃣ Install Dependencies
Make sure you have **Python 3.8+** installed.

```bash
pip install -r requirements.txt
````

### 2️⃣ Run the Django Server

```bash
python manage.py runserver
```

Your API will be available at http://127.0.0.1:8000/.

## ✅ Running Tests

```bash
pytest
```

## 📌 Key Design Decisions
Handling Irregular Sampling Frequency

✔ Sliding time window (60 minutes)

✔ Uses timestamp-based filtering

✔ No assumption about fixed sampling rates

Handling Delayed or Lost Samples

✔ Delayed samples are accepted if within 60 minutes

✔ Lost samples are ignored (metrics use available data)

✔ Uses deque (O(1) operations) for efficiency