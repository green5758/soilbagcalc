#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoilBagCalc - Garden Soil, Mulch, Compost & Raised Bed Volume Calculator
+ Automated Daily Amazon Product Review Publisher
Affiliate StoreID: everythi00099-20
"""

import os
import json
import math
import hashlib
import datetime
import urllib.request
import urllib.parse
import urllib.error

AFFILIATE_TAG = "everythi00099-20"
STATE_FILE = "posts_state.json"
OUTPUT_DIR = "public"
REVIEWS_DIR = os.path.join(OUTPUT_DIR, "reviews")
DAILY_NEW_ARTICLES = 3

REPO_FULL = os.environ.get("GITHUB_REPOSITORY", "username/soilbagcalc")
REPO_OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", REPO_FULL.split("/")[0])
REPO_NAME = REPO_FULL.split("/")[-1] if "/" in REPO_FULL else "soilbagcalc"

if REPO_NAME.lower() == f"{REPO_OWNER.lower()}.github.io":
    BASE_URL = f"https://{REPO_OWNER.lower()}.github.io"
else:
    BASE_URL = f"https://{REPO_OWNER.lower()}.github.io/{REPO_NAME}"

INDEXNOW_KEY = hashlib.md5(f"soilbagcalc-{AFFILIATE_TAG}".encode("utf-8")).hexdigest()


def amazon_search_url(query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.amazon.com/s?k={encoded}&tag={AFFILIATE_TAG}"


# ==============================================================================
# MASTER BEST SELLER & COMPARISON CATALOG (10 FLAGSHIP GARDEN SOIL & BED PRODUCTS)
# ==============================================================================
CORE_PRODUCTS = [
    {
        "id": "fox-farm-ocean-forest-potting-soil",
        "name": "FoxFarm FX14053 Ocean Forest Organic Potting Soil (12-Quart / 2 Cu.Ft.)",
        "brand": "FoxFarm",
        "category": "Potting & Raised Bed Soil",
        "bag_cuft": 2.0,
        "coverage_at_3in_sqft": 8.0,
        "soil_type": "Aged Forest Humus, Earthworm Castings & Bat Guano",
        "ph_range": "6.3 – 6.8 pH (Ready to Plant)",
        "rating": "4.7",
        "reviews_count": 26400,
        "badge": "#1 Best Selling Potting Soil",
        "search_query": "FoxFarm Ocean Forest Organic Potting Soil",
        "highlight": "Pre-charged with composted forest humus, peat moss, earthworm castings, fish emulsion, and sandy loam for vigorous root aeration."
    },
    {
        "id": "miracle-gro-raised-bed-soil",
        "name": "Miracle-Gro Raised Bed Soil Blended for Vegetables, Herbs & Flowers",
        "brand": "Miracle-Gro",
        "category": "Potting & Raised Bed Soil",
        "bag_cuft": 2.0,
        "coverage_at_3in_sqft": 8.0,
        "soil_type": "Compost, Peat Moss & Slow-Release Plant Food",
        "ph_range": "6.0 – 7.0 pH (Feeds up to 3 Months)",
        "rating": "4.6",
        "reviews_count": 18900,
        "badge": "Best Raised Bed Mix",
        "search_query": "Miracle-Gro Raised Bed Soil Vegetables Flowers",
        "highlight": "Formulated specifically not to compact in raised wooden or metal beds while feeding tomatoes, peppers, and greens for up to 3 months."
    },
    {
        "id": "vivosun-heavy-duty-fabric-grow-bags",
        "name": "VIVOSUN 5-Pack 10-Gallon Heavy-Duty 300G Nonwoven Fabric Grow Pots",
        "brand": "VIVOSUN",
        "category": "Fabric Grow Bags",
        "bag_cuft": 1.34,
        "coverage_at_3in_sqft": 12.5,
        "soil_type": "300g Thickened Breathable Nonwoven Geotextile",
        "ph_range": "Air-Prunes Roots & Prevents Overwatering",
        "rating": "4.7",
        "reviews_count": 39200,
        "badge": "#1 Best Selling Grow Bags",
        "search_query": "VIVOSUN Heavy Duty Fabric Grow Bags 10 Gallon",
        "highlight": "Reinforced stitched handles and breathable fabric walls promote fibrous root air-pruning and superior drainage on patios or decks."
    },
    {
        "id": "vegega-galvanized-raised-garden-bed",
        "name": "VEGEGA 8x2x1.5 ft 9-in-1 Modular Galvanized Metal Raised Garden Bed",
        "brand": "VEGEGA",
        "category": "Metal Raised Garden Beds",
        "bag_cuft": 24.0,
        "coverage_at_3in_sqft": 16.0,
        "soil_type": "Aluzinc Corrosion-Resistant Steel (0.8mm–1.8mm)",
        "ph_range": "Eco-Friendly Non-Leaching Coating",
        "rating": "4.6",
        "reviews_count": 5840,
        "badge": "Best Deep Raised Bed",
        "search_query": "VEGEGA Galvanized Metal Raised Garden Bed",
        "highlight": "17-inch tall wall height supports deep root crops and hugelkultur bottom-fill layering while resisting rust for 20+ years."
    },
    {
        "id": "scott-naturals-cedar-mulch",
        "name": "Scotts Nature Scapes 2 Cu. Ft. Deep Forest Brown Color-Enhanced Mulch",
        "brand": "Scotts",
        "category": "Garden Mulch & Compost",
        "bag_cuft": 2.0,
        "coverage_at_3in_sqft": 8.0,
        "soil_type": "100% Recycled Forest Wood Fiber (1-Year Color Lock)",
        "ph_range": "Suppresses Weeds & Retains Soil Moisture",
        "rating": "4.6",
        "reviews_count": 11300,
        "badge": "#1 Best Selling Mulch",
        "search_query": "Scotts Nature Scapes Mulch 2 cu ft",
        "highlight": "Locks in soil moisture during hot summer weeks and blocks annual weed germination around shrubs, trees, and perennial borders."
    },
    {
        "id": "coast-of-maine-stonington-blend",
        "name": "Coast of Maine Stonington Blend Organic Grower's Mix (1 Cu. Ft.)",
        "brand": "Coast of Maine",
        "category": "Potting & Raised Bed Soil",
        "bag_cuft": 1.0,
        "coverage_at_3in_sqft": 4.0,
        "soil_type": "Lobster & Crab Compost, Sphagnum Peat & Kelp Meal",
        "ph_range": "6.2 – 6.8 pH (OMRI Listed Organic)",
        "rating": "4.7",
        "reviews_count": 4720,
        "badge": "Top Organic Grower Mix",
        "search_query": "Coast of Maine Stonington Blend Organic Grower Mix",
        "highlight": "Rich marine compost and kelp meal blend with balanced water retention and drainage for heirloom vegetables and containers."
    },
    {
        "id": "black-kow-composted-cow-manure",
        "name": "Black Kow 50-lb (1 Cu. Ft.) Composted Cow Manure Soil Amendment",
        "brand": "Black Kow",
        "category": "Garden Mulch & Compost",
        "bag_cuft": 1.0,
        "coverage_at_3in_sqft": 4.0,
        "soil_type": "100% Composted Cow Manure + Lime & Humus",
        "ph_range": "Odor-Free Aged Organic Microbe Booster",
        "rating": "4.7",
        "reviews_count": 15600,
        "badge": "Best Soil Conditioner",
        "search_query": "Black Kow Composted Cow Manure 50 lb",
        "highlight": "Improves clay and sandy native soil structure by blending 25%–50% composted organic matter into existing garden beds."
    },
    {
        "id": "ac-infinity-heavy-duty-grow-bags",
        "name": "AC Infinity 4-Pack 5-Gallon Heavy-Duty 500G Fabric Grow Bags",
        "brand": "AC Infinity",
        "category": "Fabric Grow Bags",
        "bag_cuft": 0.67,
        "coverage_at_3in_sqft": 8.0,
        "soil_type": "Ultra-Thick 500G Woven Fabric + Nylon Straps",
        "ph_range": "High-Drainage Root Zone Aeration",
        "rating": "4.8",
        "reviews_count": 8910,
        "badge": "Heavy-Duty 500G Fabric",
        "search_query": "AC Infinity Heavy Duty 5 Gallon Fabric Grow Bags",
        "highlight": "Heavy 500gsm fabric resists tearing when moving loaded pots and keeps root temperatures cooler in direct afternoon sun."
    },
    {
        "id": "vivosun-galvanized-raised-bed-oval",
        "name": "VIVOSUN 6x3x1 ft Oval Galvanized Steel Raised Garden Bed Kit",
        "brand": "VIVOSUN",
        "category": "Metal Raised Garden Beds",
        "bag_cuft": 18.0,
        "coverage_at_3in_sqft": 18.0,
        "soil_type": "Double-Layer Anti-Rust Galvanized Sheet Steel",
        "ph_range": "Open-Bottom Drainage + Rubber Edge Trim",
        "rating": "4.6",
        "reviews_count": 12800,
        "badge": "Best Value Metal Bed",
        "search_query": "VIVOSUN Galvanized Raised Garden Bed 6x3x1 ft",
        "highlight": "Tool-friendly bolt assembly with protective top edge strip and open bottom for natural earthworm migration and drainage."
    },
    {
        "id": "back-to-the-roots-organic-seed-starter",
        "name": "Back to the Roots 100% Organic Potting Mix & Seed Starting Blend",
        "brand": "Back to the Roots",
        "category": "Potting & Raised Bed Soil",
        "bag_cuft": 1.5,
        "coverage_at_3in_sqft": 6.0,
        "soil_type": "Peat-Free / Sustainable Coir, Compost & Perlite",
        "ph_range": "6.2 – 6.8 pH (Peat-Free Option)",
        "rating": "4.5",
        "reviews_count": 6430,
        "badge": "Best Peat-Free Blend",
        "search_query": "Back to the Roots Organic Potting Mix",
        "highlight": "Lightweight organic blend with yucca extract wetting agent for even moisture distribution across indoor planters and outdoor beds."
    }
]


# ==============================================================================
# COMBINATORIAL ENGINE FOR 1,800 UNIQUE DAILY GARDEN SOIL & BED REVIEWS
# ==============================================================================
BRANDS_MATRIX = [
    ("FoxFarm", "Aged Forest Humus, Earthworm Castings & Balanced Drainage"),
    ("Miracle-Gro", "Controlled-Release Plant Nutrition & Loose Root Aeration"),
    ("Coast of Maine", "Marine Kelp Meal, Lobster Compost & OMRI Organic Matter"),
    ("Black Kow", "Aged Composted Cow Manure & Beneficial Soil Microbes"),
    ("VIVOSUN", "Breathable Nonwoven Root Fabric & Anti-Rust Galvanized Panels"),
    ("VEGEGA", "Heavy-Gauge Aluzinc Steel & Modular Multi-Shape Bed Framing"),
    ("Scotts", "Color-Lock Forest Mulch Fiber & Moisture-Retaining Texture"),
    ("AC Infinity", "500G Heavy-Duty Woven Geotextile & Reinforced Load Handles"),
    ("Back to the Roots", "Sustainable Organic Compost Blend & Even Wetting Matrix"),
    ("Espoma Organic", "Mycorrhizae Root Enhancer & Natural Compost Humate"),
    ("Happy Frog", "Soil Conditioner with Beneficial Fungi & Humic Acids"),
    ("Gardzen", "Heavy-Duty Breathable Aeration Pots & Drainage Reinforcement"),
    ("Keter", "Weather-Resistant Resin Planter Wall & Wood-Grain Finish"),
    ("LifeSmart", "UV-Stabilized Composite Garden Edging & Modular Bed Kit"),
    ("Burpee", "Eco-Friendly Seed & Root Blend with High Perlite Porosity"),
]

MODELS_MATRIX = [
    ("2 Cu. Ft. Organic Raised Bed & Potting Soil Bag", 2.0, 8.0, "Potting & Raised Bed Soil", "6.3–6.8 pH", "Loose Loam & Compost"),
    ("1.5 Cu. Ft. Premium Container & Planter Mix", 1.5, 6.0, "Potting & Raised Bed Soil", "6.2–6.7 pH", "High-Perlite Aeration Mix"),
    ("1 Cu. Ft. (50 lb) Composted Manure Soil Amendment", 1.0, 4.0, "Garden Mulch & Compost", "Neutral pH", "Rich Organic Humus"),
    ("2 Cu. Ft. Deep Forest Hardwood & Bark Mulch", 2.0, 8.0, "Garden Mulch & Compost", "Weed & Moisture Barrier", "Shredded Bark & Wood Fiber"),
    ("8x2x1.5 ft (24 Cu. Ft.) Deep Metal Raised Garden Bed", 24.0, 16.0, "Metal Raised Garden Beds", "18-Inch Root Depth", "Galvanized Corrugated Steel"),
    ("6x3x1 ft (18 Cu. Ft.) Oval Galvanized Raised Bed", 18.0, 18.0, "Metal Raised Garden Beds", "12-Inch Wall Height", "Anti-Rust Coated Steel"),
    ("4x4x1 ft (16 Cu. Ft.) Square Kitchen Garden Bed", 16.0, 16.0, "Metal Raised Garden Beds", "12-Inch Wall Height", "Modular Corner Panels"),
    ("5-Pack 10-Gallon Heavy-Duty Breathable Grow Bags", 6.7, 15.0, "Fabric Grow Bags", "Air-Pruning Walls", "Thick Nonwoven Geotextile"),
    ("5-Pack 7-Gallon Tomato, Pepper & Potato Grow Pots", 4.7, 12.0, "Fabric Grow Bags", "High Drainage Rate", "Reinforced Strap Fabric"),
    ("4-Pack 15-Gallon Large Shrub & Patio Grow Bags", 8.0, 20.0, "Fabric Grow Bags", "Deep Root Volume", "Heavy-Duty Aeration Cloth"),
    ("3 Cu. Ft. Bulk-Equivalent Garden Soil Value Pack", 3.0, 12.0, "Potting & Raised Bed Soil", "6.2–6.8 pH", "Compost & Screened Topsoil"),
    ("2 Cu. Ft. Cedar & Cypress Landscape Mulch Bag", 2.0, 8.0, "Garden Mulch & Compost", "Natural Aromatic Fiber", "Moisture-Locking Mulch"),
]

APPLICATIONS_MATRIX = [
    ("8x4 ft Raised Vegetable Bed at 9-Inch Soil Depth (24 Cu. Ft.)", 24.0, "fills a classic 8x4 ft raised bed cleanly without running short mid-project"),
    ("4x8 ft Herb, Salad Green & Root Crop Planter (16 Cu. Ft.)", 16.0, "provides loose, clod-free root media for carrots, radishes, lettuce, and basil"),
    ("Backyard Shrub Border & Tree Ring Mulching at 3-Inch Depth", 18.0, "locks in moisture, moderates soil temperature swings, and suppresses weeds"),
    ("Sunny Patio, Deck & Balcony Container Garden Setup", 10.0, "delivers balanced drainage and aeration for tomatoes, peppers, and patio herbs"),
    ("Heavy Clay Yard Soil Remediation & Organic Matter Tilling", 20.0, "loosens dense clay structure when blended 1:3 with native backyard soil"),
    ("Deep-Rooted Raised Bed for Tomatoes, Zucchini & Peppers", 27.0, "supports deep taproots and moisture consistency during peak summer heat"),
    ("Pollinator Flower Bed & Perennial Border Refresh", 14.0, "creates a nutrient-rich bed for coneflowers, lavender, zinnias, and perennials"),
    ("Small Urban Backyard & Rental Yard Modular Bed Project", 12.0, "makes it easy to grow fresh produce in tight spaces without tearing up turf"),
    ("Walkway & Fence-Line Weed Suppression Mulch Strip", 15.0, "keeps narrow side-yard strips tidy with minimal seasonal maintenance"),
    ("Multi-Bed Kitchen Garden Expansion (Two 6x3 ft Beds)", 36.0, "scales efficiently across multiple raised beds while keeping bag math simple"),
]


def get_article_blueprint(index: int) -> dict:
    """Secara deterministik menghasilkan artikel review tanah/mulsa/bed kebun unik berdasarkan indeks."""
    b_idx = index % len(BRANDS_MATRIX)
    m_idx = (index // len(BRANDS_MATRIX)) % len(MODELS_MATRIX)
    a_idx = (index // (len(BRANDS_MATRIX) * len(MODELS_MATRIX))) % len(APPLICATIONS_MATRIX)

    brand_name, brand_tech = BRANDS_MATRIX[b_idx]
    model_name, vol_cuft, cov_3in, category, spec_note, media_type = MODELS_MATRIX[m_idx]
    app_title, target_cuft, app_benefit = APPLICATIONS_MATRIX[a_idx]

    bags_needed = max(1, math.ceil(target_cuft / max(vol_cuft, 0.5)))
    cu_yards = round(target_cuft / 27.0, 2)

    slug = f"review-{brand_name.lower().replace(' ', '-')}-{model_name.lower().replace('.', '').replace('/', '').replace(' ', '-')}-{index + 1}"
    slug = "".join(c if c.isalnum() or c == "-" else "" for c in slug)
    while "--" in slug:
        slug = slug.replace("--", "-")

    title = f"{brand_name} {model_name} Review: Sized for {app_title}"
    search_q = f"{brand_name} {model_name}"

    return {
        "index": index,
        "slug": slug,
        "title": title,
        "brand": brand_name,
        "brand_tech": brand_tech,
        "model_name": model_name,
        "category": category,
        "vol_cuft": vol_cuft,
        "cov_3in": cov_3in,
        "spec_note": spec_note,
        "media_type": media_type,
        "app_title": app_title,
        "target_cuft": target_cuft,
        "cu_yards": cu_yards,
        "bags_needed": bags_needed,
        "app_benefit": app_benefit,
        "rating": "4.8" if (index % 2 == 0) else "4.7",
        "search_query": search_q,
        "affiliate_url": amazon_search_url(search_q),
    }


def load_and_advance_state() -> tuple[list[dict], list[dict]]:
    """Memuat posts_state.json dan menambahkan 3 artikel review baru setiap hari."""
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {
            "last_run_date": "",
            "next_index": 0,
            "published_articles": []
        }

    newly_added = []
    if len(state["published_articles"]) == 0:
        count_to_add = 6
    else:
        count_to_add = DAILY_NEW_ARTICLES

    for _ in range(count_to_add):
        idx = state["next_index"]
        bp = get_article_blueprint(idx)
        entry = {
            "index": idx,
            "slug": bp["slug"],
            "date": today_str,
            "title": bp["title"]
        }
        state["published_articles"].append(entry)
        newly_added.append({**bp, "date": today_str})
        state["next_index"] = idx + 1

    state["last_run_date"] = today_str

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    all_articles = []
    for item in reversed(state["published_articles"]):
        bp = get_article_blueprint(item["index"])
        bp["date"] = item["date"]
        all_articles.append(bp)

    return all_articles, newly_added


# ==============================================================================
# SHARED CSS — GREY BACKGROUND THEME
# ==============================================================================
GLOBAL_CSS = """
:root {
  --bg-page: #cbd5e1;
  --bg-section: #e2e8f0;
  --bg-card: #f1f5f9;
  --bg-dark: #1e293b;
  --bg-darker: #0f172a;
  --border-grey: #94a3b8;
  --text-main: #0f172a;
  --text-muted: #334155;
  --accent-amazon: #ff9900;
  --accent-green: #15803d;
  --accent-link: #0369a1;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: var(--bg-page);
  color: var(--text-main);
  line-height: 1.6;
}
a { color: var(--accent-link); text-decoration: none; }
.container { max-width: 1240px; margin: 0 auto; padding: 0 18px; }

.top-promo-banner {
  background: linear-gradient(90deg, #0f172a 0%, #334155 50%, #1e293b 100%);
  color: #ffffff;
  padding: 12px 16px;
  border-bottom: 3px solid var(--accent-amazon);
  text-align: center;
  font-size: 0.94rem;
}
.top-promo-banner .badge-live {
  background: var(--accent-amazon);
  color: #0f172a;
  font-weight: 900;
  padding: 3px 10px;
  border-radius: 4px;
  margin-right: 10px;
  text-transform: uppercase;
  font-size: 0.78rem;
}
.top-promo-banner a.banner-cta {
  display: inline-block;
  margin-left: 12px;
  background: #4ade80;
  color: #052e16;
  font-weight: 800;
  padding: 4px 14px;
  border-radius: 5px;
}

header.site-header {
  background-color: var(--bg-dark);
  color: #f8fafc;
  padding: 16px 0;
  box-shadow: 0 3px 10px rgba(0,0,0,0.22);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-flex {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
}
.brand-logo {
  font-size: 1.55rem;
  font-weight: 900;
  color: #ffffff;
}
.brand-logo span { color: var(--accent-amazon); }
.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  list-style: none;
}
.nav-links a {
  color: #e2e8f0;
  font-weight: 600;
  font-size: 0.92rem;
  padding: 6px 10px;
  border-radius: 5px;
}
.nav-links a:hover { background: #334155; color: var(--accent-amazon); }

.hero-banner {
  background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
  color: #f8fafc;
  padding: 34px 26px;
  margin: 24px 0;
  border-radius: 12px;
  border: 2px solid #64748b;
}
.hero-grid {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 24px;
  align-items: center;
}
@media (max-width: 860px) { .hero-grid { grid-template-columns: 1fr; } }
.hero-banner h1 { font-size: 2.05rem; line-height: 1.22; margin-bottom: 12px; color: #ffffff; }
.hero-banner p { color: #cbd5e1; font-size: 1.02rem; margin-bottom: 18px; }
.hero-deal-box {
  background: #0f172a;
  border: 2px solid var(--accent-amazon);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}
.hero-deal-box h3 { color: var(--accent-amazon); margin-bottom: 8px; font-size: 1.16rem; }

.btn-amazon {
  display: inline-block;
  background: linear-gradient(180deg, #ffd814 0%, #ff9900 100%);
  color: #0f172a !important;
  font-weight: 800;
  padding: 11px 18px;
  border-radius: 6px;
  border: 1px solid #d97706;
  text-align: center;
  cursor: pointer;
}
.btn-amazon:hover { background: linear-gradient(180deg, #f7ca00 0%, #e68a00 100%); }
.btn-outline {
  display: inline-block;
  padding: 9px 14px;
  border: 2px solid #1e293b;
  color: #0f172a;
  font-weight: 700;
  border-radius: 6px;
  font-size: 0.88rem;
}
.btn-outline:hover { background: #1e293b; color: #ffffff; }

.grey-section {
  background-color: var(--bg-section);
  border: 1px solid var(--border-grey);
  border-radius: 12px;
  padding: 26px;
  margin-bottom: 26px;
}
.section-title {
  font-size: 1.55rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
  border-left: 6px solid var(--accent-amazon);
  padding-left: 12px;
}
.section-sub { color: var(--text-muted); margin-bottom: 20px; font-size: 0.96rem; }

.calc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
@media (max-width: 860px) { .calc-grid { grid-template-columns: 1fr; } }
.calc-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  padding: 22px;
  border-radius: 10px;
}
.preset-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.preset-btn {
  background: #cbd5e1;
  border: 1px solid #64748b;
  color: #0f172a;
  padding: 7px 12px;
  border-radius: 6px;
  font-size: 0.83rem;
  font-weight: 700;
  cursor: pointer;
}
.preset-btn:hover { background: #94a3b8; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-weight: 700; margin-bottom: 5px; font-size: 0.9rem; color: #1e293b; }
.form-group input, .form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #64748b;
  border-radius: 6px;
  background: #ffffff;
  font-size: 0.98rem;
  color: #0f172a;
}
.metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.metric-card {
  background: #e2e8f0;
  border: 1px solid #94a3b8;
  padding: 14px;
  border-radius: 8px;
  text-align: center;
}
.metric-card .val { font-size: 1.5rem; font-weight: 900; color: #0f172a; }
.metric-card .lbl { font-size: 0.78rem; font-weight: 700; color: #334155; text-transform: uppercase; }
.rec-box {
  background: #ffffff;
  border: 2px solid var(--accent-green);
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
}
.rec-box h4 { color: var(--accent-green); font-size: 1.04rem; margin-bottom: 6px; }

.search-bar { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 18px; }
.search-input {
  flex: 1;
  min-width: 240px;
  padding: 12px 15px;
  border: 2px solid #475569;
  border-radius: 8px;
  font-size: 1rem;
  background: #ffffff;
}
.filter-select {
  padding: 12px 15px;
  border: 2px solid #475569;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #ffffff;
  font-weight: 700;
}

.product-grid, .articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 18px;
}
.product-card, .article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.badge-tag {
  display: inline-block;
  background: #1e293b;
  color: var(--accent-amazon);
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  align-self: flex-start;
  text-transform: uppercase;
}
.spec-box {
  list-style: none;
  margin: 10px 0 14px;
  font-size: 0.88rem;
  background: #e2e8f0;
  padding: 10px 12px;
  border-radius: 6px;
}
.spec-box li { margin-bottom: 4px; }

.table-wrap { overflow-x: auto; }
table.comp-table {
  width: 100%;
  border-collapse: collapse;
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
}
table.comp-table th {
  background: #1e293b;
  color: #ffffff;
  text-align: left;
  padding: 13px 12px;
  font-size: 0.86rem;
  text-transform: uppercase;
}
table.comp-table td {
  padding: 12px;
  border-bottom: 1px solid #cbd5e1;
  font-size: 0.91rem;
}
table.comp-table tr:nth-child(even) { background: #e2e8f0; }

details.faq-item {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 12px;
}
details.faq-item summary { font-weight: 800; font-size: 1.02rem; cursor: pointer; color: #0f172a; }
details.faq-item p { margin-top: 10px; color: #334155; font-size: 0.95rem; }

.sitemap-columns { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
.sitemap-box { background: var(--bg-card); border: 1px solid var(--border-grey); padding: 18px; border-radius: 8px; }
.sitemap-box h3 { margin-bottom: 10px; font-size: 1.1rem; color: #0f172a; }
.sitemap-box ul { padding-left: 18px; font-size: 0.9rem; line-height: 1.8; }

footer.site-footer {
  background: var(--bg-darker);
  color: #cbd5e1;
  padding: 36px 0;
  margin-top: 40px;
  border-top: 4px solid var(--accent-amazon);
  font-size: 0.9rem;
}
.footer-links { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 14px; }
.footer-links a { color: #f8fafc; font-weight: 600; }
"""


def build_article_page(article: dict, recent_articles: list[dict]) -> str:
    related_links = ""
    for rel in recent_articles[:8]:
        if rel["slug"] == article["slug"]:
            continue
        related_links += f"""
        <li>
          <a href="{BASE_URL}/reviews/{rel['slug']}.html"><strong>{rel['title']}</strong></a>
          <span> ({rel['vol_cuft']} Cu. Ft. / {rel['media_type']} — {rel['date']})</span>
        </li>
        """

    bed_scenarios = [
        ("4x4 ft Raised Bed (6-in Depth)", 4.0, 4.0, 6.0),
        ("4x8 ft Raised Bed (9-in Depth)", 4.0, 8.0, 
