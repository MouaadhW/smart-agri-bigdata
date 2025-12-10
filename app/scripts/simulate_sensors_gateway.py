import json
import os
import random
from datetime import datetime, timedelta

FIELDS = [
    {"fieldid": "field01", "croptype": "tomato", "lat": 36.8, "lon": 10.2},
    {"fieldid": "field02", "croptype": "potato", "lat": 36.9, "lon": 10.3},
]

def generatereading(basetime, field):
    soilmoisture = max(0, min(1, random.gauss(0.35, 0.1)))
    soiltemp = random.uniform(18, 26)
    soilph = random.uniform(5.5, 7.5)
    airtemp = random.uniform(20, 30)
    airhumidity = random.uniform(40, 90)
    light = random.uniform(300, 1100)

    droughtrisk = (
        "high" if soilmoisture < 0.2 and airtemp > 28 else
        "medium" if soilmoisture < 0.3 else
        "low"
    )

    return {
        "fieldid": field["fieldid"],
        "sensorid": f"{field['fieldid']}_sensor",
        "timestamp": basetime.isoformat(),
        "sensortype": "combined",
        "croptype": field["croptype"],
        "location": {"lat": field["lat"], "lon": field["lon"]},
        "soil": {
            "moisture": round(soilmoisture, 3),
            "temperature": round(soiltemp, 2),
            "ph": round(soilph, 2),
        },
        "atmosphere": {
            "temperature": round(airtemp, 2),
            "humidity": round(airhumidity, 2),
            "light": round(light, 2),
        },
        "qualityflags": {
            "outlier": False,
            "imputed": False,
        },
        "derived": {
            "droughtrisk": droughtrisk,
            "diseaseriskscore": round(random.uniform(0, 1), 3),
        },
    }

def main():
    starttime = datetime(2025, 12, 9, 0, 0, 0)
    endtime = starttime + timedelta(days=1)
    step = timedelta(minutes=15)

    outdir = "data/gateway_output"
    os.makedirs(outdir, exist_ok=True)

    current = starttime
    while current < endtime:
        batch = [generatereading(current, f) for f in FIELDS]
        tsstr = current.strftime("%Y%m%d%H%M")
        filename = os.path.join(outdir, f"sensorbatch{tsstr}.json")
        with open(filename, "w", encoding="utf-8") as f:
            for doc in batch:
                f.write(json.dumps(doc) + "\n")
        current += step

    print("Sensor simulation finished. Files in data/gateway_output/")


if __name__ == "__main__":
    main()