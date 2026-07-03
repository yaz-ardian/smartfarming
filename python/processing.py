import math

from config import HEAVY_ANALYSIS_ITERATIONS


# ==========================================================
# HEALTH SCORE
# ==========================================================

def calculate_health(temp, hum, soil, ph, light):

    soil_score = max(0, min(100, (900 - soil) / 6))

    temp_score = max(0, 100 - abs(temp - 28) * 8)

    hum_score = max(0, 100 - abs(hum - 70) * 2)

    ph_score = max(0, 100 - abs(ph - 6.5) * 30)

    light_score = max(0, 100 - abs(light - 700) / 8)

    health = (
        soil_score +
        temp_score +
        hum_score +
        ph_score +
        light_score
    ) / 5

    return round(health, 2), soil_score


# ==========================================================
# WATER STRESS
# ==========================================================

def calculate_water_stress(temp, hum, soil_score):

    stress = (
        abs(temp - 28) * 0.6 +
        abs(hum - 70) * 0.4 +
        (100 - soil_score) * 0.5
    )

    return round(min(100, stress), 2)


# ==========================================================
# DISEASE RISK
# ==========================================================

def calculate_disease(temp, hum, soil_score):

    risk = (
        hum * 0.45 +
        temp * 0.35 +
        (100 - soil_score) * 0.20
    )

    if risk >= 70:
        return "High"

    elif risk >= 50:
        return "Medium"

    return "Low"


# ==========================================================
# IRRIGATION
# ==========================================================

def calculate_irrigation(soil_score, water_stress):

    irrigation = (
        (100 - soil_score) * 0.8 +
        water_stress * 0.3
    )

    return round(max(0, irrigation), 2)


# ==========================================================
# FERTILIZER
# ==========================================================

def calculate_fertilizer(ph):

    return round(max(0, 7 - ph), 2)


# ==========================================================
# CROP RECOMMENDATION
# ==========================================================

def recommend_crop(ph, hum):

    if ph >= 6.2 and hum >= 65:
        return "Rice"

    elif ph >= 5.8:
        return "Corn"

    return "Soybean"


# ==========================================================
# STATUS
# ==========================================================

def determine_status(health):

    if health >= 80:
        return "Healthy"

    elif health >= 60:
        return "Moderate"

    return "Critical"


# ==========================================================
# HEAVY ANALYSIS
# ==========================================================

def heavy_analysis(temp, hum, soil, ph, light):

    score = 0.0

    for i in range(HEAVY_ANALYSIS_ITERATIONS):

        score += (
            math.sin(temp * i / 500)
            + math.cos(ph * i / 300)
            + math.sqrt(i + 1)
            + math.log(i + 2)
        )

    return score


# ==========================================================
# MAIN PROCESS
# ==========================================================

def process_data(data):

    temp = data["temperature"]
    hum = data["humidity"]
    soil = data["soil"]
    ph = data["ph"]
    light = data["light"]

    # Analisis kesehatan lahan
    health, soil_score = calculate_health(
        temp,
        hum,
        soil,
        ph,
        light
    )

    # Analisis water stress
    water_stress = calculate_water_stress(
        temp,
        hum,
        soil_score
    )

    # Analisis risiko penyakit
    disease = calculate_disease(
        temp,
        hum,
        soil_score
    )

    # Rekomendasi irigasi
    irrigation = calculate_irrigation(
        soil_score,
        water_stress
    )

    # Rekomendasi pupuk
    fertilizer = calculate_fertilizer(ph)

    # Rekomendasi tanaman
    crop = recommend_crop(ph, hum)

    # Status lahan
    status = determine_status(health)

    # Simulasi komputasi berat
    heavy_analysis(
        temp,
        hum,
        soil,
        ph,
        light
    )

    return {

        "id": data["id"],

        "grid": data["grid"],

        "health_score": health,

        "status": status,

        "water_stress": water_stress,

        "disease_risk": disease,

        "irrigation": irrigation,

        "fertilizer": fertilizer,

        "crop": crop

    }