# Stories for Thursday 26 November 2026 — researched 26 Nov 2026 from
# Reuters, BBC, The Guardian, Headline Desk and EventGraph.
# Every headline below is a real story of the day; certainty labels are
# CONFIRMED (outlet states it as fact), CLAIM (one party's claim, not
# independently confirmed), REPORTED (outlet attributes it to records or
# reports) or FORECAST (a prediction). Regions: NA, EU, ME, APAC, AF, LATAM.
# Counted stories: 2 heroes + 24 section cards + 4 sport + 5 late wire = 35.

DAY = "Thursday 26 November 2026"
DATE_SHORT = "26 NOVEMBER 2026"

HEROES = [
    {
        "kicker": "LEAD — TRADE WAR",
        "headline": "TRUMP HITS 14 ECONOMIES WITH NEW TARIFFS",
        "deck": ("The White House proposes duties of up to 35% on China, the EU, "
                 "Japan and 11 other economies under Section 301, citing "
                 "excess capacity. Markets brace as Thanksgiving shuts US trading."),
        "source": "REUTERS · BBC",
        "certainty": "CONFIRMED",
        "region": "NA",
        "art": "tariffs",
    },
    {
        "kicker": "LEAD — MIDDLE EAST",
        "headline": "HOUTHIS CLAIM STRIKE ON SAUDI MEGA-REFINERY",
        "deck": ("Yemen's Houthis say they hit Ras Tanura, the kingdom's largest "
                 "refinery. Riyadh says four drones were shot down; satellites "
                 "show black smoke. Brent tops $94 a barrel."),
        "source": "REUTERS",
        "certainty": "CLAIM",
        "region": "ME",
        "art": "refinery",
    },
]

SECTIONS = [
    {
        "name": "WORLD",
        "color": (193, 39, 45),
        "cards": [
            {
                "headline": "NETANYAHU CASE 4000: JUDGES URGE CHARGES DROPPED",
                "deck": ("Israeli judges recommend prosecutors drop the most serious "
                         "case against the PM, over telecoms favours for good coverage."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "ME",
                "motif": "gavel",
            },
            {
                "headline": "ISRAELI STRIKE KILLS SENIOR HAMAS OFFICIAL IN GAZA",
                "deck": ("Hamas internal security chief and his family killed in a "
                         "Gaza City strike, as an Israeli ground operation pushes on."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "ME",
            },
            {
                "headline": "KYIV SAYS FIVE RUSSIAN JETS HIT IN AIRFIELD STRIKE",
                "deck": ("Ukraine claims the strike on a Russian airfield; "
                         "Moscow has not confirmed the losses."),
                "source": "BBC", "certainty": "CLAIM", "region": "EU",
                "motif": "drone",
            },
            {
                "headline": "RUSSIA'S OWN FIGURES: NEARLY 500,000 LOST IN UKRAINE",
                "deck": ("Moscow's data point to almost half a million people lost "
                         "in the war, the BBC reports."),
                "source": "BBC", "certainty": "REPORTED", "region": "EU",
            },
            {
                "headline": "31 KILLED AS FUEL TANKER FIRE ENGULFS CAIRO HIGHWAY",
                "deck": ("Tanker overturns on a busy ring road; 21 more injured "
                         "in the blaze."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "AF",
                "motif": "flame",
            },
            {
                "headline": "COLOMBIA FREES 76 HOSTAGES AFTER 17-HOUR SIEGE",
                "deck": ("Police storm a supermarket and free all 76 people "
                         "held inside."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "LATAM",
            },
            {
                "headline": "NORTH KOREA EXPELS SWISS DIPLOMAT IN SANCTIONS ROW",
                "deck": ("Pyongyang orders the envoy out as tensions over "
                         "sanctions deepen."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "APAC",
            },
            {
                "headline": "ABREGO GARCIA LANDS IN SPAIN, ENDING DEPORTATION BATTLE",
                "deck": ("Kilmar Abrego Garcia arrives in Spain, closing the "
                         "Trump-era deportation fight."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "NA",
            },
        ],
    },
    {
        "name": "MONEY & TECH",
        "color": (20, 33, 61),
        "cards": [
            {
                "headline": "BANK OF KOREA LIFTS RATE TO 3.25%",
                "deck": ("Quarter-point hike resumes tightening after the October "
                         "pause, as chip exports boom and inflation runs hot."),
                "source": "REUTERS", "certainty": "CONFIRMED", "region": "APAC",
                "motif": "bank",
            },
            {
                "headline": "BOJ SIGNALS FASTER HIKES IF PRICES OVERSHOOT",
                "deck": ("Board member Tamura says the Bank of Japan must respond "
                         "swiftly to signs of an inflation overshoot."),
                "source": "REUTERS", "certainty": "CONFIRMED", "region": "APAC",
            },
            {
                "headline": "NVIDIA SLIDES 3.9% AS S&P PUTS RATING ON WATCH",
                "deck": ("Chipmaker $2.3 trillion below its October peak; S&P cites "
                         "management and board oversight."),
                "source": "REUTERS", "certainty": "CONFIRMED", "region": "NA",
                "motif": "chip",
            },
            {
                "headline": "US CLEARS SPACEX PLAN FOR A MILLION AI SATELLITES",
                "deck": ("FCC approves the Starmind constellation: up to a million "
                         "solar-powered data satellites in orbit."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "NA",
                "motif": "satellite",
            },
            {
                "headline": "TRUMP ACCOUNTS TRADED NVIDIA 44 TIMES THIS YEAR",
                "deck": ("Records show the president's accounts bought and sold "
                         "the chip stock 44 times in 2026."),
                "source": "BBC", "certainty": "REPORTED", "region": "NA",
            },
            {
                "headline": "UBER NAMES RANJAN TO RUN INDIA AND SOUTH ASIA",
                "deck": ("Rakesh Ranjan takes the president's job from 4 January 2027."),
                "source": "REUTERS", "certainty": "CONFIRMED", "region": "APAC",
            },
            {
                "headline": "ANZ DROPPED FROM NEW YORK FED'S FX LIST",
                "deck": ("Australia's ANZ is removed from the Fed's foreign-exchange "
                         "counterparties; no reason given."),
                "source": "REUTERS", "certainty": "CONFIRMED", "region": "APAC",
            },
        ],
    },
    {
        "name": "SCIENCE & PLANET",
        "color": (46, 111, 64),
        "cards": [
            {
                "headline": "CHINA LOFTS FIRST PAKISTANI ASTRONAUT TO SPACE STATION",
                "deck": ("Shenzhou-24 carries Muhammad Zeeshan Ali to Tiangong — "
                         "the first foreign guest aboard."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "APAC",
            },
            {
                "headline": "EUCLID FINDS MOST DISTANT QUASAR YET",
                "deck": ("Light from 13.1 billion years ago: a giant black hole just "
                         "630 million years after the Big Bang."),
                "source": "HEADLINE DESK", "certainty": "CONFIRMED", "region": "EU",
                "motif": "atom",
            },
            {
                "headline": "HERA SEES STADIUM-SIZED CRATER ON DEFLECTED ASTEROID",
                "deck": ("Europe's Hera spacecraft images Dimorphos after NASA's "
                         "2022 DART impact test."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "EU",
                "motif": "asteroid",
            },
            {
                "headline": "KING TIDES FLOOD CALIFORNIA COAST",
                "deck": ("Record tides swamp roads and businesses as high water "
                         "meets El Nino seas."),
                "source": "BBC · GUARDIAN", "certainty": "CONFIRMED", "region": "NA",
                "motif": "drop",
            },
            {
                "headline": "PUNJAB FARM FIRES DOWN 53% AS STUBBLE FINDS A MARKET",
                "deck": ("Farmers sell paddy straw to biomass plants instead of "
                         "burning it: 5,114 fires, down from 2024."),
                "source": "REUTERS", "certainty": "CONFIRMED", "region": "APAC",
            },
        ],
    },
    {
        "name": "SOCIETY & CULTURE",
        "color": (146, 90, 24),
        "cards": [
            {
                "headline": "DURAN DURAN GUITARIST ANDY TAYLOR DIES AT 65",
                "deck": ("The Wild Boys guitarist, whose riffs defined the 1980s, "
                         "dies aged 65."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "EU",
                "motif": "mic",
            },
            {
                "headline": "JOLIE AND PITT SETTLE WINERY BATTLE",
                "deck": ("Former spouses end the legal fight over their French vineyard."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "NA",
            },
            {
                "headline": "MACY'S POSTPONES THANKSGIVING PARADE ON WEATHER",
                "deck": ("New York's parade is pushed back as bad weather hits "
                         "the holiday."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "NA",
                "motif": "storm",
            },
            {
                "headline": "NOLLYWOOD STAR PETE EDOCHIE DIES AT 79",
                "deck": ("Veteran Nigerian actor, a giant of Nollywood, dies aged 79."),
                "source": "BBC", "certainty": "CONFIRMED", "region": "AF",
            },
        ],
    },
]

SPORT = [
    {
        "headline": "MAN UTD HELD IN LISBON AMID CHAOS",
        "deck": "Four goals and controversy as Sporting deny United; Fernandes scores twice.",
        "source": "BBC", "certainty": "CONFIRMED", "region": "EU",
    },
    {
        "headline": "MALEN PENALTY EARNS ROMA DRAW AT PSG",
        "deck": "Roma hold Paris Saint-Germain in the Champions League.",
        "source": "BBC", "certainty": "CONFIRMED", "region": "EU",
    },
    {
        "headline": "PADRES SIGN ROMERO FOR $21M OVER THREE YEARS",
        "deck": "World Series-winning reliever JoJo Romero heads to San Diego.",
        "source": "REUTERS", "certainty": "REPORTED", "region": "NA",
    },
    {
        "headline": "TIGERS ADD GAUSMAN ON $25M ONE-YEAR DEAL",
        "deck": "Detroit lands veteran right-hander Kevin Gausman.",
        "source": "REUTERS", "certainty": "REPORTED", "region": "NA",
    },
]

LATE_WIRE = [
    ("BBC journalists vote for work stoppage over cuts and workloads.", "BBC", "CONFIRMED", "EU"),
    ("Sarkozy and wife Carla Bruni to face trial, French court rules.", "BBC", "CONFIRMED", "EU"),
    ("Zimbabwe issues arrest warrant for Robert Mugabe's son.", "BBC", "CONFIRMED", "AF"),
    ("Amnesty urges ICC genocide probe over births in Gaza.", "EVENTGRAPH", "REPORTED", "ME"),
    ("Ukraine legalises crypto market; 271 MPs vote yes.", "EVENTGRAPH", "REPORTED", "EU"),
]

# By-the-numbers band: figures drawn from the stories above, not new stories.
BY_THE_NUMBERS = [
    ("550,000", "barrels a day at Ras Tanura"),
    ("500,000", "people Russia has lost, per its own figures"),
    ("31", "killed in the Cairo tanker fire"),
    ("76", "hostages freed in Colombia"),
    ("1,000,000", "satellites in SpaceX's approved constellation"),
    ("44", "Nvidia trades by Trump accounts in 2026"),
    ("3.25%", "Bank of Korea rate after the hike"),
    ("$94.81", "Brent crude a barrel"),
]

MARKETS = "NIKKEI +1.6%   ·   KOSPI +1.9%   ·   BRENT $94.81   ·   GOLD $3,566   ·   DOLLAR 103.71   ·   US 10-YR 4.85%"
WEATHER = "KING TIDES FLOOD CALIFORNIA   ·   MACY'S PARADE POSTPONED   ·   THANKSGIVING: US MARKETS SHUT"

# UTC timeline of the day, from source timestamps seen on 26 Nov 2026.
TIMELINE = [
    ("00:01", "Roma hold PSG in Paris"),
    ("00:23", "BBC front page leads with the new US tariffs"),
    ("00:32", "BBC journalists vote for a work stoppage"),
    ("01:10", "Bank of Korea lifts its rate to 3.25%"),
    ("02:00", "JETRO: Chinese firms close on Japan rivals"),
    ("02:09", "Uber names Ranjan for India"),
]

REGIONS = {
    "NA": "N. AMERICA",
    "EU": "EUROPE",
    "ME": "MIDDLE EAST",
    "APAC": "ASIA-PACIFIC",
    "AF": "AFRICA",
    "LATAM": "LATIN AMERICA",
}


def all_stories():
    """Every counted story, in ranked order."""
    items = list(HEROES)
    for section in SECTIONS:
        items.extend(section["cards"])
    items.extend(SPORT)
    for text, source, certainty, region in LATE_WIRE:
        items.append({"headline": text, "source": source,
                      "certainty": certainty, "region": region})
    return items


def story_count():
    return len(all_stories())


def region_counts():
    counts = {}
    for story in all_stories():
        region = story.get("region")
        if region:
            counts[region] = counts.get(region, 0) + 1
    return counts


def field_counts():
    counts = {"WORLD": len(HEROES) + len(SECTIONS[0]["cards"])}
    for section in SECTIONS[1:]:
        counts[section["name"]] = len(section["cards"])
    counts["SPORT"] = len(SPORT)
    counts["LATE WIRE"] = len(LATE_WIRE)
    return counts
