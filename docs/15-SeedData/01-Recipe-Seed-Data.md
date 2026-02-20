---
created: 2026-02-17
modified: 2026-02-17
version: 1.0
status: Draft
---

# Recipe Seed Data

Seed recipes for the Epicura `recipes` table. Based on Posha's 500+ one-pot recipe library across 10 cuisines. Each recipe includes nutrition per serving, tags for filtering, cuisine type, and image reference.

> [!note] Image Convention
> All images should show the finished food in a bowl, photographed from above at ~45° angle. Store in S3/R2 at `recipes/{slug}.jpg` (800x800px, JPEG, 80% quality).

---

## Schema Mapping

| Column | Source Field |
|--------|-------------|
| `name` | Recipe name |
| `category` | Category (dal, curry, rice, pasta, soup, stir-fry, breakfast, dessert, snack, one-pot) |
| `cuisine` | Cuisine type |
| `tags` | Array of filter tags |
| `difficulty` | easy / medium / hard |
| `time_minutes` | Total cook time |
| `servings` | Default servings |
| `calories` | kcal per serving |
| `protein_g` | Protein per serving (g) |
| `carbs_g` | Carbs per serving (g) |
| `fats_g` | Fats per serving (g) |
| `image_url` | CDN path |

---

## Indian Cuisine

### Dals

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 1 | Dal Tadka | dal | indian | vegetarian, protein-rich, healthy, gluten-free | easy | 35 | 4 | 320 | 18 | 42 | 8 | dal-tadka |
| 2 | Dal Makhani | dal | indian | vegetarian, protein-rich | medium | 55 | 4 | 380 | 16 | 40 | 16 | dal-makhani |
| 3 | Moong Dal | dal | indian | vegetarian, healthy, gluten-free, quick | easy | 25 | 4 | 240 | 14 | 36 | 4 | moong-dal |
| 4 | Toor Dal Fry | dal | indian | vegetarian, healthy, gluten-free | easy | 30 | 4 | 260 | 15 | 38 | 5 | toor-dal-fry |
| 5 | Chana Dal | dal | indian | vegetarian, protein-rich, gluten-free | medium | 45 | 4 | 340 | 20 | 48 | 6 | chana-dal |
| 6 | Masoor Dal | dal | indian | vegetarian, healthy, gluten-free, quick | easy | 20 | 4 | 230 | 16 | 34 | 3 | masoor-dal |
| 7 | Dal Palak | dal | indian | vegetarian, healthy, gluten-free | easy | 30 | 4 | 250 | 16 | 32 | 6 | dal-palak |
| 8 | Urad Dal | dal | indian | vegetarian, protein-rich, gluten-free | medium | 50 | 4 | 350 | 22 | 44 | 8 | urad-dal |
| 9 | Panchmel Dal | dal | indian | vegetarian, protein-rich, gluten-free | medium | 40 | 4 | 310 | 20 | 40 | 7 | panchmel-dal |
| 10 | Sambar | dal | indian | vegan, healthy, gluten-free | medium | 40 | 4 | 280 | 12 | 44 | 6 | sambar |

### Curries

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 11 | Paneer Butter Masala | curry | indian | vegetarian, protein-rich | medium | 40 | 4 | 420 | 22 | 28 | 24 | paneer-butter-masala |
| 12 | Palak Paneer | curry | indian | vegetarian, protein-rich, healthy | medium | 35 | 4 | 350 | 20 | 18 | 22 | palak-paneer |
| 13 | Chole (Chickpea Curry) | curry | indian | vegan, protein-rich, gluten-free | medium | 45 | 4 | 360 | 18 | 50 | 10 | chole |
| 14 | Rajma (Kidney Bean Curry) | curry | indian | vegan, protein-rich, gluten-free | medium | 50 | 4 | 340 | 16 | 52 | 6 | rajma |
| 15 | Aloo Gobi | curry | indian | vegan, healthy, gluten-free | easy | 30 | 4 | 220 | 6 | 32 | 8 | aloo-gobi |
| 16 | Bhindi Masala | curry | indian | vegan, healthy, gluten-free | easy | 25 | 4 | 180 | 4 | 20 | 10 | bhindi-masala |
| 17 | Egg Curry | curry | indian | protein-rich, gluten-free | easy | 30 | 4 | 310 | 18 | 16 | 20 | egg-curry |
| 18 | Chicken Curry | curry | indian | protein-rich, gluten-free | medium | 45 | 4 | 380 | 32 | 14 | 22 | chicken-curry |
| 19 | Butter Chicken | curry | indian | protein-rich | medium | 45 | 4 | 440 | 34 | 18 | 26 | butter-chicken |
| 20 | Kadai Paneer | curry | indian | vegetarian, protein-rich | medium | 35 | 4 | 390 | 20 | 22 | 24 | kadai-paneer |
| 21 | Matar Paneer | curry | indian | vegetarian, protein-rich | easy | 30 | 4 | 360 | 18 | 26 | 20 | matar-paneer |
| 22 | Shahi Paneer | curry | indian | vegetarian, protein-rich | hard | 50 | 4 | 450 | 22 | 24 | 30 | shahi-paneer |
| 23 | Mushroom Masala | curry | indian | vegan, healthy, gluten-free | easy | 25 | 4 | 200 | 8 | 18 | 12 | mushroom-masala |
| 24 | Baingan Bharta | curry | indian | vegan, healthy, gluten-free | medium | 35 | 4 | 190 | 4 | 22 | 10 | baingan-bharta |
| 25 | Malai Kofta | curry | indian | vegetarian | hard | 55 | 4 | 480 | 16 | 34 | 32 | malai-kofta |
| 26 | Keema (Mutton Mince) | curry | indian | protein-rich, gluten-free | medium | 40 | 4 | 420 | 30 | 12 | 28 | keema |
| 27 | Fish Curry | curry | indian | protein-rich, gluten-free, healthy | medium | 30 | 4 | 320 | 28 | 10 | 18 | fish-curry |
| 28 | Prawn Masala | curry | indian | protein-rich, gluten-free | medium | 30 | 4 | 300 | 26 | 12 | 16 | prawn-masala |
| 29 | Dum Aloo | curry | indian | vegetarian, gluten-free | medium | 40 | 4 | 320 | 8 | 38 | 16 | dum-aloo |
| 30 | Mixed Veg Curry | curry | indian | vegan, healthy, gluten-free | easy | 30 | 4 | 210 | 6 | 28 | 8 | mixed-veg-curry |

### Rice Dishes

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 31 | Jeera Rice | rice | indian | vegan, gluten-free, quick | easy | 20 | 4 | 280 | 6 | 52 | 6 | jeera-rice |
| 32 | Veg Biryani | rice | indian | vegetarian | hard | 55 | 4 | 420 | 12 | 64 | 14 | veg-biryani |
| 33 | Chicken Biryani | rice | indian | protein-rich | hard | 60 | 4 | 520 | 28 | 62 | 16 | chicken-biryani |
| 34 | Mutton Biryani | rice | indian | protein-rich | hard | 70 | 4 | 560 | 32 | 58 | 20 | mutton-biryani |
| 35 | Paneer Biryani | rice | indian | vegetarian, protein-rich | hard | 55 | 4 | 480 | 20 | 60 | 18 | paneer-biryani |
| 36 | Egg Biryani | rice | indian | protein-rich | medium | 50 | 4 | 460 | 22 | 58 | 14 | egg-biryani |
| 37 | Pulao | rice | indian | vegetarian, gluten-free | easy | 30 | 4 | 320 | 8 | 56 | 8 | pulao |
| 38 | Lemon Rice | rice | indian | vegan, gluten-free, quick | easy | 20 | 4 | 290 | 6 | 54 | 6 | lemon-rice |
| 39 | Tomato Rice | rice | indian | vegan, gluten-free, quick | easy | 25 | 4 | 300 | 6 | 56 | 6 | tomato-rice |
| 40 | Khichdi | rice | indian | vegetarian, healthy, gluten-free | easy | 25 | 4 | 280 | 12 | 46 | 4 | khichdi |
| 41 | Curd Rice | rice | indian | vegetarian, gluten-free, quick | easy | 15 | 4 | 260 | 8 | 44 | 6 | curd-rice |
| 42 | Bisibele Bath | rice | indian | vegetarian, protein-rich | medium | 45 | 4 | 380 | 14 | 56 | 10 | bisibele-bath |

### Breakfast / Snacks

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 43 | Upma | breakfast | indian | vegetarian, healthy, quick | easy | 15 | 4 | 220 | 6 | 36 | 6 | upma |
| 44 | Poha | breakfast | indian | vegan, healthy, gluten-free, quick | easy | 15 | 4 | 250 | 6 | 42 | 6 | poha |
| 45 | Oats Porridge | breakfast | indian | vegetarian, healthy, quick | easy | 10 | 2 | 180 | 6 | 30 | 4 | oats-porridge |
| 46 | Halwa (Suji) | dessert | indian | vegetarian | easy | 20 | 4 | 350 | 4 | 48 | 16 | suji-halwa |
| 47 | Kheer (Rice Pudding) | dessert | indian | vegetarian, gluten-free | easy | 30 | 4 | 320 | 8 | 50 | 10 | kheer |

---

## Italian Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 48 | Pasta Arrabbiata | pasta | italian | vegan | easy | 20 | 4 | 380 | 12 | 62 | 10 | pasta-arrabbiata |
| 49 | Pasta Alfredo | pasta | italian | vegetarian | easy | 20 | 4 | 480 | 16 | 56 | 22 | pasta-alfredo |
| 50 | Penne Pesto | pasta | italian | vegetarian | easy | 20 | 4 | 440 | 14 | 54 | 20 | penne-pesto |
| 51 | Spaghetti Aglio e Olio | pasta | italian | vegan | easy | 15 | 4 | 400 | 12 | 58 | 14 | spaghetti-aglio-olio |
| 52 | Mac and Cheese | pasta | italian | vegetarian | easy | 25 | 4 | 520 | 20 | 52 | 26 | mac-and-cheese |
| 53 | Pasta Bolognese | pasta | italian | protein-rich | medium | 35 | 4 | 480 | 28 | 52 | 18 | pasta-bolognese |
| 54 | Mushroom Risotto | rice | italian | vegetarian | medium | 35 | 4 | 420 | 12 | 58 | 16 | mushroom-risotto |
| 55 | Tomato Basil Soup | soup | italian | vegan, healthy, gluten-free | easy | 25 | 4 | 180 | 4 | 24 | 8 | tomato-basil-soup |
| 56 | Minestrone Soup | soup | italian | vegan, healthy | easy | 30 | 4 | 200 | 8 | 32 | 4 | minestrone-soup |
| 57 | Creamy Pumpkin Risotto | rice | italian | vegetarian | medium | 40 | 4 | 400 | 10 | 56 | 14 | pumpkin-risotto |

---

## American Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 58 | Chili Con Carne | one-pot | american | protein-rich, gluten-free | medium | 45 | 4 | 420 | 28 | 36 | 18 | chili-con-carne |
| 59 | Chicken Gumbo | soup | american | protein-rich | medium | 50 | 4 | 380 | 26 | 30 | 16 | chicken-gumbo |
| 60 | Jambalaya | rice | american | protein-rich | medium | 45 | 4 | 460 | 24 | 54 | 14 | jambalaya |
| 61 | Clam Chowder | soup | american | protein-rich | medium | 35 | 4 | 340 | 18 | 28 | 18 | clam-chowder |
| 62 | Beef Stroganoff | one-pot | american | protein-rich | medium | 35 | 4 | 440 | 30 | 32 | 22 | beef-stroganoff |
| 63 | Corn Chowder | soup | american | vegetarian, gluten-free | easy | 25 | 4 | 280 | 8 | 38 | 12 | corn-chowder |
| 64 | BBQ Pulled Chicken | one-pot | american | protein-rich, gluten-free | medium | 40 | 4 | 360 | 30 | 24 | 14 | bbq-pulled-chicken |

---

## Chinese Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 65 | Veg Fried Rice | rice | chinese | vegan, stir-fry, quick | easy | 20 | 4 | 340 | 8 | 56 | 10 | veg-fried-rice |
| 66 | Chicken Fried Rice | rice | chinese | protein-rich, stir-fry | easy | 25 | 4 | 420 | 22 | 54 | 12 | chicken-fried-rice |
| 67 | Egg Fried Rice | rice | chinese | protein-rich, stir-fry, quick | easy | 15 | 4 | 380 | 14 | 54 | 12 | egg-fried-rice |
| 68 | Hakka Noodles (Veg) | stir-fry | chinese | vegan, stir-fry | easy | 20 | 4 | 360 | 10 | 56 | 10 | veg-hakka-noodles |
| 69 | Chicken Hakka Noodles | stir-fry | chinese | protein-rich, stir-fry | easy | 25 | 4 | 420 | 22 | 52 | 14 | chicken-hakka-noodles |
| 70 | Manchurian Gravy | curry | chinese | vegetarian, stir-fry | medium | 30 | 4 | 300 | 8 | 34 | 14 | manchurian-gravy |
| 71 | Sweet and Sour Chicken | stir-fry | chinese | protein-rich, stir-fry | medium | 30 | 4 | 380 | 26 | 36 | 12 | sweet-sour-chicken |
| 72 | Kung Pao Chicken | stir-fry | chinese | protein-rich, stir-fry, gluten-free | medium | 25 | 4 | 360 | 28 | 20 | 18 | kung-pao-chicken |
| 73 | Hot and Sour Soup | soup | chinese | healthy, quick | easy | 15 | 4 | 140 | 8 | 16 | 4 | hot-sour-soup |
| 74 | Mapo Tofu | curry | chinese | vegan, protein-rich, gluten-free | medium | 25 | 4 | 280 | 18 | 14 | 18 | mapo-tofu |

---

## Mexican Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 75 | Mexican Rice | rice | mexican | vegan, gluten-free | easy | 25 | 4 | 300 | 6 | 54 | 6 | mexican-rice |
| 76 | Black Bean Stew | one-pot | mexican | vegan, protein-rich, gluten-free, healthy | easy | 35 | 4 | 280 | 16 | 44 | 4 | black-bean-stew |
| 77 | Chicken Burrito Bowl | one-pot | mexican | protein-rich, gluten-free | medium | 35 | 4 | 440 | 30 | 48 | 14 | chicken-burrito-bowl |
| 78 | Enchilada Sauce Chicken | one-pot | mexican | protein-rich, gluten-free | medium | 40 | 4 | 380 | 28 | 22 | 18 | enchilada-chicken |
| 79 | Refried Beans | one-pot | mexican | vegan, protein-rich, gluten-free | easy | 30 | 4 | 240 | 14 | 38 | 4 | refried-beans |
| 80 | Salsa Verde Chicken | one-pot | mexican | protein-rich, gluten-free | medium | 35 | 4 | 340 | 30 | 14 | 16 | salsa-verde-chicken |

---

## Korean Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 81 | Bibimbap (Rice Bowl) | rice | korean | healthy | medium | 35 | 4 | 420 | 18 | 56 | 14 | bibimbap |
| 82 | Kimchi Fried Rice | rice | korean | stir-fry, quick | easy | 15 | 4 | 360 | 12 | 52 | 12 | kimchi-fried-rice |
| 83 | Japchae (Glass Noodles) | stir-fry | korean | stir-fry, gluten-free | medium | 30 | 4 | 320 | 10 | 48 | 10 | japchae |
| 84 | Tteokbokki (Spicy Rice Cakes) | one-pot | korean | vegan, stir-fry | easy | 20 | 4 | 340 | 8 | 60 | 6 | tteokbokki |
| 85 | Korean Army Stew (Budae Jjigae) | soup | korean | protein-rich | medium | 35 | 4 | 420 | 24 | 34 | 20 | budae-jjigae |
| 86 | Sundubu Jjigae (Tofu Stew) | soup | korean | protein-rich, gluten-free | medium | 30 | 4 | 280 | 18 | 16 | 16 | sundubu-jjigae |

---

## Thai Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 87 | Green Curry (Veg) | curry | thai | vegan, gluten-free | medium | 30 | 4 | 320 | 8 | 22 | 22 | thai-green-curry-veg |
| 88 | Green Curry Chicken | curry | thai | protein-rich, gluten-free | medium | 35 | 4 | 400 | 28 | 18 | 24 | thai-green-curry-chicken |
| 89 | Red Curry Shrimp | curry | thai | protein-rich, gluten-free | medium | 30 | 4 | 360 | 24 | 16 | 22 | red-curry-shrimp |
| 90 | Pad Thai (Veg) | stir-fry | thai | vegan, stir-fry | medium | 25 | 4 | 380 | 10 | 54 | 14 | pad-thai-veg |
| 91 | Pad Thai Chicken | stir-fry | thai | protein-rich, stir-fry | medium | 30 | 4 | 440 | 24 | 52 | 16 | pad-thai-chicken |
| 92 | Tom Yum Soup | soup | thai | healthy, gluten-free | easy | 20 | 4 | 180 | 12 | 14 | 8 | tom-yum-soup |
| 93 | Tom Kha Gai | soup | thai | protein-rich, gluten-free | medium | 25 | 4 | 300 | 20 | 12 | 20 | tom-kha-gai |
| 94 | Thai Basil Chicken | stir-fry | thai | protein-rich, stir-fry, gluten-free, quick | easy | 20 | 4 | 340 | 28 | 14 | 18 | thai-basil-chicken |

---

## Asian (Pan-Asian)

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 95 | Teriyaki Chicken | stir-fry | asian | protein-rich, stir-fry | easy | 25 | 4 | 380 | 30 | 28 | 14 | teriyaki-chicken |
| 96 | Japanese Curry | curry | asian | protein-rich | medium | 40 | 4 | 420 | 22 | 48 | 16 | japanese-curry |
| 97 | Miso Soup | soup | asian | vegan, healthy, quick | easy | 10 | 4 | 120 | 8 | 10 | 4 | miso-soup |
| 98 | Laksa | soup | asian | protein-rich | medium | 35 | 4 | 440 | 22 | 40 | 22 | laksa |
| 99 | Pho Broth (Beef) | soup | asian | protein-rich, gluten-free | hard | 60 | 4 | 360 | 24 | 36 | 12 | pho-beef |
| 100 | Nasi Goreng | rice | asian | stir-fry | easy | 20 | 4 | 400 | 16 | 56 | 12 | nasi-goreng |

---

## Global Cuisine

| # | Name | Category | Cuisine | Tags | Difficulty | Time | Servings | Cal | Protein | Carbs | Fats | Image Slug |
|---|------|----------|---------|------|------------|------|----------|-----|---------|-------|------|------------|
| 101 | Shakshuka | one-pot | global | vegetarian, protein-rich, gluten-free, healthy | easy | 25 | 4 | 280 | 16 | 20 | 16 | shakshuka |
| 102 | Daal Soup (Moroccan) | soup | global | vegan, healthy, gluten-free | easy | 30 | 4 | 240 | 14 | 36 | 4 | moroccan-daal-soup |
| 103 | Spanish Rice | rice | global | vegan, gluten-free | easy | 25 | 4 | 310 | 6 | 56 | 6 | spanish-rice |
| 104 | Ratatouille | one-pot | global | vegan, healthy, gluten-free | medium | 40 | 4 | 180 | 4 | 24 | 8 | ratatouille |
| 105 | Couscous with Vegetables | one-pot | global | vegan, healthy | easy | 20 | 4 | 300 | 10 | 52 | 6 | couscous-veg |
| 106 | Lentil Soup (Turkish) | soup | global | vegan, protein-rich, healthy, gluten-free | easy | 30 | 4 | 260 | 16 | 38 | 4 | turkish-lentil-soup |
| 107 | Jollof Rice | rice | global | vegan, gluten-free | medium | 40 | 4 | 380 | 8 | 62 | 10 | jollof-rice |
| 108 | Congee (Rice Porridge) | breakfast | global | healthy, gluten-free | easy | 30 | 4 | 200 | 6 | 38 | 2 | congee |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Recipes** | 108 |
| **Cuisines** | 9 (Indian, Italian, American, Chinese, Mexican, Korean, Thai, Asian, Global) |
| **Categories** | 10 (dal, curry, rice, pasta, soup, stir-fry, one-pot, breakfast, dessert, snack) |
| **Vegan** | 28 |
| **Vegetarian** | 38 |
| **Protein Rich** | 48 |
| **Gluten Free** | 52 |
| **Healthy** | 22 |
| **Quick (≤20 min)** | 16 |
| **Stir Fry** | 14 |
| **Easy** | 48 |
| **Medium** | 50 |
| **Hard** | 10 |

---

## SQL Insert Template

```sql
INSERT INTO recipes (name, category, cuisine, tags, difficulty, time_minutes, servings,
                     calories, protein_g, carbs_g, fats_g, image_url, is_published, version)
VALUES
  ('Dal Tadka', 'dal', 'indian',
   ARRAY['vegetarian','protein-rich','healthy','gluten-free'],
   'easy', 35, 4, 320, 18, 42, 8,
   'https://cdn.epicura.io/recipes/dal-tadka.jpg', true, 1),
  -- ... repeat for all recipes
;
```

---

## Image Requirements

Each recipe needs a hero image:
- **Format:** JPEG, 800x800px, 80% quality
- **Style:** Overhead 45° shot of food in a round bowl on dark/neutral background
- **Naming:** `{image-slug}.jpg` (lowercase, hyphenated)
- **Storage:** S3/R2 bucket at path `recipes/`
- **CDN URL pattern:** `https://cdn.epicura.io/recipes/{image-slug}.jpg`

> [!tip] Image Generation
> Use an AI image generator (DALL-E, Midjourney) with prompt: *"Overhead photo of {recipe name} in a round white ceramic bowl on dark wood table, professional food photography, warm lighting, 45 degree angle"*

---

## Related Documentation

- [[../10-Backend/02-Database-Schema|Database Schema]] — `recipes` table definition
- [[../11-API/01-REST-API-Reference|REST API Reference]] — Recipe CRUD endpoints
- [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] — Recipe card layout

#epicura #recipes #seed-data #database

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-17 | Manas Pradhan | Initial seed data — 108 recipes across 9 cuisines |
