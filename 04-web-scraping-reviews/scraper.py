"""
Web scraper for consumer product reviews.
Demonstrates scraping techniques with BeautifulSoup and stores results in SQLite.
Includes a demo mode that generates realistic sample data.
"""
import os
import sys
import sqlite3
import logging
import re
from datetime import datetime, timezone

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "reviews.db")
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")
LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "scraper.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(os.path.join(SQL_DIR, "schema.sql"), "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text.strip())
    text = text.encode("ascii", "ignore").decode("ascii")
    return text


def parse_rating(raw):
    if isinstance(raw, (int, float)):
        return max(1, min(5, int(raw)))
    match = re.search(r"(\d+(?:\.\d+)?)", str(raw))
    if match:
        return max(1, min(5, round(float(match.group(1)))))
    return None


def parse_date(raw):
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%d %B %Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw.strip()[:10]


def scrape_page(url):
    """Scrape a single page and extract review data (generic structure)."""
    if not requests or not BeautifulSoup:
        logger.error("requests and beautifulsoup4 are required for live scraping")
        return []

    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    reviews = []
    for card in soup.select("[data-review], .review-card, .review-item, .review"):
        author = card.select_one(".author, .reviewer-name, [data-author]")
        rating_el = card.select_one(".rating, .star-rating, [data-rating]")
        title_el = card.select_one(".review-title, .title, h3, h4")
        content_el = card.select_one(".review-text, .review-body, .content, p")
        date_el = card.select_one(".review-date, .date, time")
        helpful_el = card.select_one(".helpful-count, .helpful, [data-helpful]")

        review = {
            "author": clean_text(author.get_text() if author else None),
            "rating": parse_rating(rating_el.get("data-rating") or rating_el.get_text() if rating_el else None),
            "title": clean_text(title_el.get_text() if title_el else None),
            "content": clean_text(content_el.get_text() if content_el else None),
            "review_date": parse_date(date_el.get("datetime") or date_el.get_text() if date_el else None),
            "helpful_count": int(helpful_el.get_text().strip()) if helpful_el and helpful_el.get_text().strip().isdigit() else 0,
            "verified": 1 if card.select_one(".verified, .verified-purchase") else 0,
        }
        if review["content"]:
            reviews.append(review)

    return reviews


def store_reviews(conn, product_id, reviews):
    for r in reviews:
        conn.execute(
            """INSERT INTO reviews
               (product_id, author, rating, title, content, review_date, helpful_count, verified)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (product_id, r["author"], r["rating"], r["title"], r["content"],
             r["review_date"], r["helpful_count"], r["verified"]),
        )
    conn.commit()


def generate_sample_data():
    """Generate realistic sample review data for demonstration."""
    import random

    conn = init_db()

    sources = [
        ("Amazon", "https://www.amazon.com"),
        ("Best Buy", "https://www.bestbuy.com"),
        ("Walmart", "https://www.walmart.com"),
    ]
    for name, url in sources:
        conn.execute("INSERT OR IGNORE INTO sources (name, url) VALUES (?, ?)", (name, url))
    conn.commit()

    products = [
        ("Sony WH-1000XM5", "Audio", "Sony", 1, 4.6),
        ("Apple AirPods Pro 2", "Audio", "Apple", 1, 4.7),
        ("Samsung Galaxy S24 Ultra", "Smartphones", "Samsung", 1, 4.4),
        ("iPhone 15 Pro Max", "Smartphones", "Apple", 1, 4.5),
        ("Dell XPS 15", "Laptops", "Dell", 2, 4.3),
        ("MacBook Air M3", "Laptops", "Apple", 2, 4.8),
        ("LG C3 OLED 65\"", "TV", "LG", 2, 4.7),
        ("Samsung QN90C 55\"", "TV", "Samsung", 3, 4.4),
        ("Dyson V15 Detect", "Home", "Dyson", 3, 4.5),
        ("iRobot Roomba j7+", "Home", "iRobot", 3, 4.2),
        ("Bose QuietComfort Ultra", "Audio", "Bose", 1, 4.5),
        ("Google Pixel 8 Pro", "Smartphones", "Google", 2, 4.3),
    ]

    for name, category, brand, source_id, avg_r in products:
        conn.execute(
            "INSERT OR IGNORE INTO products (name, category, brand, source_id, avg_rating) VALUES (?, ?, ?, ?, ?)",
            (name, category, brand, source_id, avg_r),
        )
    conn.commit()

    first_names = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia",
                   "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Charlotte", "Alexander",
                   "Amelia", "Daniel", "Harper", "Michael", "Evelyn", "David", "Abigail",
                   "Joseph", "Emily", "Samuel", "Elizabeth", "Thomas", "Sofia", "John", "Ella"]

    positive_titles = [
        "Excellent product!", "Best purchase ever", "Highly recommended",
        "Worth every penny", "Amazing quality", "Love it!",
        "Great value for money", "Exceeded expectations", "Fantastic!",
        "Perfect for daily use", "Outstanding performance",
    ]
    neutral_titles = [
        "Decent product", "Good but not great", "Mixed feelings",
        "Average experience", "It's okay", "Some pros and cons",
    ]
    negative_titles = [
        "Disappointed", "Not worth the price", "Could be better",
        "Quality issues", "Returned it", "Below expectations",
    ]

    review_templates = {
        "Audio": {
            5: ["The noise cancellation is incredible. Best headphones I've ever owned. Sound quality is crystal clear and the battery lasts forever.",
                "Superb audio quality with deep bass and crisp highs. The comfort level is unmatched for long listening sessions.",
                "These are a game changer for my commute. The ANC blocks everything and the sound is premium quality."],
            4: ["Great sound overall. Noise cancellation works well in most situations. Minor comfort issue after 3+ hours.",
                "Very good headphones with excellent features. The app could use some improvements but sound is top notch.",
                "Solid audio product. Good build quality and comfortable fit. Wish the case was slightly smaller."],
            3: ["Sound is decent but nothing groundbreaking for the price. ANC is good but not the best I've tried.",
                "Average audio quality compared to competitors. Comfortable but the connectivity drops occasionally."],
            2: ["The noise cancellation stopped working after 2 months. Sound quality is mediocre at best.",
                "Not comfortable for extended use. The ear cups are too small and create pressure points."],
            1: ["Broke within a week. Terrible build quality for such an expensive product. Complete waste of money.",
                "Worst headphones I've purchased. Constant connectivity issues and the sound is tinny."],
        },
        "Smartphones": {
            5: ["The camera system is absolutely phenomenal. Best photos I've ever taken with a phone. Battery easily lasts all day.",
                "Blazing fast performance with a gorgeous display. This phone handles everything I throw at it effortlessly.",
                "The best smartphone on the market right now. Camera, display, performance - everything is top tier."],
            4: ["Great phone with excellent camera. Battery life is good but not exceptional. The display is stunning.",
                "Very satisfied with this purchase. Fast, reliable, and takes great photos. Minor software bugs but nothing major.",
                "Solid upgrade from my previous phone. The camera improvements alone make it worth it."],
            3: ["Good phone but overpriced for what you get. Camera is nice but similar to last year's model.",
                "It's fine. Does everything a modern smartphone should do. Nothing really stands out though."],
            2: ["Battery drains too fast. The phone gets warm during normal use. Camera is overhyped.",
                "Disappointing for the price. My previous phone felt more responsive and had better battery life."],
            1: ["Screen cracked easily. Worst smartphone experience I've had. Customer support was unhelpful.",
                "Constant crashes and freezes. Had to return it within the first week. Absolutely not recommended."],
        },
        "Laptops": {
            5: ["Perfect for both work and creative tasks. The display is gorgeous and performance is outstanding.",
                "This laptop replaced my desktop. Fast, portable, and the keyboard is a pleasure to type on.",
                "Best laptop I've ever used. The build quality is premium and it runs everything smoothly."],
            4: ["Very capable laptop with great performance. The screen is beautiful. Gets a bit warm under heavy load.",
                "Excellent for productivity. Good battery life and the trackpad is best in class. Wish it had more ports.",
                "Great machine overall. Fast, quiet, and well-built. The speakers are surprisingly good."],
            3: ["Decent laptop for the price. Performance is adequate but not impressive. Build quality is average.",
                "It does the job but I expected more for this price range. The fan noise can be distracting."],
            2: ["The keyboard started having issues after a month. Screen is okay but the bezels are too thick.",
                "Overheats during basic tasks. The trackpad is unreliable and the speakers are weak."],
            1: ["Dead on arrival. Had to return it immediately. The quality control is clearly lacking.",
                "Worst laptop purchase ever. Slow, buggy, and the battery barely lasts 3 hours."],
        },
        "TV": {
            5: ["The picture quality is absolutely stunning. OLED blacks are incredible and HDR content looks amazing.",
                "Best TV I've ever owned. The colors are vibrant, motion handling is smooth, and the smart features are great.",
                "This TV transformed my living room. Movies look cinematic and gaming at 120Hz is buttery smooth."],
            4: ["Excellent picture quality with great contrast. The smart TV interface is snappy. Some minor blooming in dark scenes.",
                "Very happy with this purchase. Great for movies and gaming. The remote could be more ergonomic.",
                "Beautiful display with rich colors. Easy setup and the built-in apps work well. Good value."],
            3: ["Picture is good but not mind-blowing for the price. The viewing angles could be better.",
                "It's a solid TV. Does what I need. The built-in speakers are mediocre but that's expected."],
            2: ["The HDR implementation is poor. Picture looks washed out in bright rooms. Disappointing.",
                "Too many software bugs. The TV freezes occasionally and some apps crash regularly."],
            1: ["Screen developed dead pixels after 2 weeks. Return process was a nightmare.",
                "The worst TV I've ever bought. Color accuracy is terrible and it makes a buzzing noise."],
        },
        "Home": {
            5: ["Incredible suction power and the laser detection is a game changer. Best vacuum I've used.",
                "This vacuum makes cleaning effortless. Smart navigation and powerful suction on all surfaces.",
                "Worth every penny. Picks up everything and the battery lasts long enough to clean my entire house."],
            4: ["Very effective cleaning performance. The app is well designed and scheduling works perfectly.",
                "Great vacuum with powerful suction. Gets stuck occasionally on rug edges but otherwise excellent.",
                "Solid appliance that does what it promises. Easy to maintain and the dustbin is a good size."],
            3: ["Decent cleaning power but struggles with pet hair in corners. The battery life is average.",
                "It works fine for daily maintenance but not deep cleaning. The noise level is higher than expected."],
            2: ["Gets stuck constantly and the navigation is poor. Misses large areas of the floor.",
                "The suction decreased significantly after a few months. Replacement parts are overpriced."],
            1: ["Broke after 3 months. The motor died and the warranty process took forever.",
                "Complete waste of money. It pushes dirt around more than it picks up. Very disappointing."],
        },
    }

    product_rows = conn.execute("SELECT product_id, name, category FROM products").fetchall()
    total = 0

    for product_id, product_name, category in product_rows:
        templates = review_templates.get(category, review_templates["Home"])
        num_reviews = random.randint(25, 50)

        for _ in range(num_reviews):
            weights = [0.05, 0.08, 0.15, 0.35, 0.37]
            rating = random.choices([1, 2, 3, 4, 5], weights=weights)[0]

            if rating >= 4:
                title = random.choice(positive_titles)
            elif rating == 3:
                title = random.choice(neutral_titles)
            else:
                title = random.choice(negative_titles)

            content = random.choice(templates.get(rating, templates[3]))
            author = random.choice(first_names) + " " + chr(random.randint(65, 90)) + "."
            year = random.choice([2025, 2025, 2025, 2026, 2026, 2026, 2026])
            month = random.randint(1, 12) if year == 2025 else random.randint(1, 10)
            day = random.randint(1, 28)
            review_date = f"{year}-{month:02d}-{day:02d}"
            helpful = random.choices([0, 0, 0, 0, 1, 2, 3, 5, 8, 12], weights=[40, 20, 10, 5, 8, 7, 5, 3, 1, 1])[0]
            verified = random.choices([0, 1], weights=[0.2, 0.8])[0]

            conn.execute(
                """INSERT INTO reviews
                   (product_id, author, rating, title, content, review_date, helpful_count, verified)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (product_id, author, rating, title, content, review_date, helpful, verified),
            )
            total += 1

    conn.execute("UPDATE products SET total_reviews = (SELECT COUNT(*) FROM reviews r WHERE r.product_id = products.product_id)")
    conn.commit()
    logger.info("Generated %d sample reviews for %d products", total, len(product_rows))
    conn.close()
    return total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Web review scraper")
    parser.add_argument("--url", help="URL to scrape reviews from")
    parser.add_argument("--demo", action="store_true", help="Generate sample data without scraping")
    args = parser.parse_args()

    if args.demo:
        generate_sample_data()
    elif args.url:
        conn = init_db()
        reviews = scrape_page(args.url)
        logger.info("Scraped %d reviews from %s", len(reviews), args.url)
        conn.close()
    else:
        logger.info("Use --demo for sample data or --url URL to scrape")
