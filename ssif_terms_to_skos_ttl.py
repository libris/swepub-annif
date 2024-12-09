import csv
import os
import sys
from datetime import datetime

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(__file__)} csv_file")
    sys.exit(1)

print(f"# Generated by {os.path.basename(__file__)} from {sys.argv[1]} on {datetime.now().isoformat()}")
print("@prefix ssif: <https://begrepp.uka.se/SSIF/> .")
print("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .")

with open(sys.argv[1], newline="") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
    for row in reader:
        data = {k: v.strip() for k, v in row.items()}
        if data["level1"]:
            print(f"""
ssif:{data['level1']} a skos:Concept ;
    skos:inScheme ssif: ;
    skos:prefLabel "{data["en"]}"@en,
        "{data["sv"]}"@sv .""")
        if data["level2"]:
            print(f"""
ssif:{data['level2']} a skos:Concept ;
    skos:inScheme ssif: ;
    skos:broader ssif:{data["level2"][:1]} ;
    skos:prefLabel "{data["en"]}"@en,
        "{data["sv"]}"@sv .""")
        if data["level3"]:
            print(f"""
ssif:{data['level3']} a skos:Concept ;
    skos:inScheme ssif: ;
    skos:broader ssif:{data["level3"][:3]} ;
    skos:prefLabel "{data["en"]}"@en,
        "{data["sv"]}"@sv .""")
