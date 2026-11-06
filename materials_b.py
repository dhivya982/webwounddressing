AUTHOR = "Lakshanna V"

# These sample scores are for learning only, not clinical recommendations.
DRESSINGS = {
    "Hydrogel": {
        "absorbency": 4,
        "antibacterial": 6,
        "cost": 3,
    },
    "Alginate": {
        "absorbency": 9,
        "antibacterial": 5,
        "cost": 6,
    },
    "Chitosan": {
        "absorbency": 6,
        "antibacterial": 8,
        "cost": 5,
    },
}

WEIGHTS = {
    "absorbency": 0.5,
    "antibacterial": 0.3,
    "cost": 0.2,
}

SOURCES = [
    {
        "material": "Alginate",
        "author": "Andrée Lee et al.",
        "title": "Alginate: Properties and biomedical applications",
        "year": 2018,
        "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6027439/",
    },
    {
        "material": "Hydrogel",
        "author": "Y. Wang et al.",
        "title": "Hydrogels for Wound Healing: Recent Advances in Biomaterials and Application",
        "year": 2021,
        "link": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7889296",
    },
    {
        "material": "Chitosan",
        "author": "M. M. Rahman et al.",
        "title": "Chitosan-Based Biomaterials for Tissue Engineering and Wound Healing Applications",
        "year": 2020,
        "link": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7767230",
    },
]