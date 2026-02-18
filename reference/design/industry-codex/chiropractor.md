---
industry: chiropractor
last_researched: 2026-02-18
sources: iMatrix, Colorlib, Perfect Patients, Brand Chiro, ChiroHosting, HubSpot, HTMLBurger
---

# Design Codex — Chiropractor

Visual conventions for chiropractic / spinal care websites.
Use this file to inform v0 prompts and template color overrides.

---

## Colors

### Dominant palette families (pick one track)

**Track A — Warm Wellness** (family care, holistic, pediatric, prenatal)
- Background: `#FFFFFF` or `#F8F8F6`
- Primary: soft teal `#2A9D8F` or sage green `#7EBC59`
- Dark sections: warm slate `#2C3E50`
- Light sections: warm cream `#F2F4F7`
- Accent tint: `#E8F5F4`

**Track B — Modern Clinical** (sports injuries, pain specialist, urban, premium)
- Background: `#FFFFFF` (light) or `#1A1A1A` (dark minimal)
- Primary: navy `#1B3A5C` or teal `#54C6D3`
- Dark sections: near-black `#1A1A1A` or dark slate `#2C3E50`
- Light sections: cool light gray `#F2F4F7`
- Accent tint: `#E0F4F8`

### Accent colors (CTA buttons only — never dominant)
- Green: `#5CB85C` or `#4CAF50` — "book now" buttons
- Warm amber: `#E8A838` — specials or callouts
- Gold: `#AC8400` — premium / established practice feel

### Colors to avoid
- Bright red — signals pain/alarm (the opposite of the desired feeling)
- Bright orange as primary — reads cheap and impulsive
- Saturated yellow — blinding, caution-sign association
- Neon or highly saturated anything — creates anxiety
- More than 2 dominant hues — signals amateur design
- Pure `#000000` black — use dark charcoals instead (`#1A1A1A`, `#2C2C2C`)

---

## Typography

### Track A — Warm/Approachable
- Display: Poppins SemiBold or Nunito Bold
- Body: Open Sans or Lato Regular
- Pairing: Poppins + Open Sans (most common in industry)

### Track B — Authoritative/Clinical
- Display: Montserrat Bold or Merriweather Bold
- Body: Source Sans Pro or Inter Regular
- Pairing: Montserrat + Open Sans, or Merriweather + Lato

### Rules
- Body size: 16px minimum, 17-18px recommended
- Line height: 1.5–1.7× (patients read slowly when in pain)
- Heading weight: 600–700 (bold to semibold — avoid thin/light)
- Max 2 font families per site
- Avoid: script fonts, decorative fonts, ALL CAPS in body, light weight body text

---

## Photography

### Primary subjects (in order of impact)
1. Chiropractor's hands on patient's spine/neck — calm, controlled adjustment
2. Doctor and patient in consultation — trust-building moment
3. Front desk staff welcoming a patient — warm and accessible
4. Treatment room — clean, organized, not sterile
5. Outcome lifestyle shots — patient hiking, playing with kids, running
6. Real team photos with full names and credentials (never stock doctor photos)

### Mood
- Natural, warm lighting — not harsh fluorescent or cold studio
- Slightly warm color grading — not blue-filtered
- Genuine expressions — not forced smiles
- Movement or interaction — not stiff poses
- Clean backgrounds — clinic hallway, treatment room

### What to avoid
- Stock "doctor with stethoscope" — wrong profession signal, kills trust instantly
- Empty office photos — signals no patients
- Generic "happy couple" or "business handshake" stock
- Heavy retouching that looks artificial
- Low resolution images at large sizes
- Hospital / urgent-care imagery — fear-inducing

---

## Layout conventions

### Hero
- Full-width image or left-text / right-image split
- H1: benefit-led, outcome language ("Finally feel like yourself again")
- H2: practice name + city/neighborhood
- Primary CTA: "Book Your Appointment" — high-contrast, below headline
- Micro-text: "New patients welcome" or "Same-day appointments available"
- Trust anchor immediately below hero: Google stars + review count

### Section order (top to bottom)
1. Sticky nav — logo left, nav center, "Book Now" button right (persistent on scroll)
2. Hero
3. Social proof bar — Google stars, review count, years serving [City]
4. Conditions treated / services — grid or cards, 4–8 items
5. About the doctor — real photo + bio + credentials
6. How it works — 3–4 step process (reduces anxiety about first visit)
7. Testimonials — video preferred, written with photo + name acceptable
8. Insurance / accepted plans — logo strip
9. Location + hours — map embed, address, phone, hours
10. Secondary CTA — repeat booking action
11. Footer — nav, contact, social, HIPAA note

### CTA rules
- Primary button: high-contrast accent (green or amber on blue/white)
- "Book Appointment" appears minimum 3× on page: nav, hero, footer
- Sticky header CTA follows on scroll
- Mobile: click-to-call phone number in sticky header

### Trust signal hierarchy
1. Google review rating + count (third-party, most credible)
2. Years in practice
3. Number of patients served
4. Video testimonials
5. Written testimonials with photo + first name
6. Professional association logos (ACA, state chiro association)
7. Insurance partner logos
8. Doctor credentials and education

---

## Tone and feel
- Calm — not clinical cold
- Welcoming — not generic corporate
- Confident — not aggressive
- Clear — no jargon in headlines
- Human — not institutional
- Outcome-focused — "get your life back" not "lumbar adjustment procedures"

### Copy pattern
Headline: outcome language → "Get back to the life you love"
Subhead: process language → "Evidence-based spinal adjustments, [City] FL"

---

## v0 prompt template

```
One-page chiropractic website for [Practice Name] in [City], FL.
Track: [Warm Wellness OR Modern Clinical].
Colors: [primary], [accent], white background, [dark section color].
Display font: [Poppins OR Montserrat]. Body font: [Open Sans OR Inter].
Sections:
  - Hero: full-width, benefit-led headline, "Book Appointment" CTA, Google stars trust anchor
  - Services/conditions: card grid, 6 items
  - About the doctor: photo placeholder + bio + credentials
  - How it works: 3-step numbered process
  - Testimonials: 2-3 cards with name + rating
  - Contact: address, phone, hours
  - Footer: HIPAA note, copyright
Sticky nav with persistent "Book Now" button. Mobile-first. Next.js + Tailwind.
```

---

## Credibility checklist
- [ ] Real doctor photo (not stock)
- [ ] Google review score visible above the fold
- [ ] Doctor credentials visible within first scroll
- [ ] Max 2 dominant colors
- [ ] "Book Appointment" CTA in sticky nav
- [ ] HIPAA compliance note in footer
- [ ] Mobile responsive
- [ ] Copyright year current
