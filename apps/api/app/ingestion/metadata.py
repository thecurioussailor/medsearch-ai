DOMAINS = {
    **{i: "Health system determinants" for i in range(1, 13)},
    **{i: "Service delivery" for i in range(13, 29)},
    **{i: "Risk factors" for i in range(29, 36)},
    **{i: "Outcomes and impacts" for i in range(36, 45)},
}


SUBDOMAINS = {
    # Health system determinants
    1: "Governance",
    2: "Governance",
    3: "Governance",
    4: "Governance",
    5: "Governance",

    6: "Financing",
    7: "Financing",

    8: "Health workforce",

    9: "Medicines and health technologies",
    10: "Medicines and health technologies",
    11: "Medicines and health technologies",

    12: "Health information",

    # Service delivery
    13: "Processes of care: assessment of risk factors for diabetes",
    14: "Processes of care: assessment of risk factors for diabetes",
    15: "Processes of care: assessment of risk factors for diabetes",
    16: "Processes of care: assessment of risk factors for diabetes",

    17: "Processes of care: diagnosis",
    18: "Processes of care: diagnosis",

    19: "Processes of care: assessment of risk factor for diabetes complications",

    20: "Processes of care: assessment of complications",
    21: "Processes of care: assessment of complications",
    22: "Processes of care: assessment of complications",

    23: "Processes of care: treatment",
    24: "Processes of care: treatment",
    25: "Processes of care: treatment",
    26: "Processes of care: treatment",
    27: "Processes of care: treatment",
    28: "Processes of care: treatment",

    # Risk factors
    29: "Risk factors for diabetes",
    30: "Risk factors for diabetes",
    31: "Risk factors for diabetes",
    32: "Risk factors for diabetes",

    33: "Risk factors for diabetes complications",
    34: "Risk factors for diabetes complications",
    35: "Risk factors for diabetes complications",

    # Outcomes and impacts
    36: "Morbidity",
    37: "Morbidity",
    38: "Morbidity",
    39: "Morbidity",
    40: "Morbidity",
    41: "Morbidity",

    42: "Mortality",
    43: "Mortality",
    44: "Mortality",
}


INDICATORS = {
    1: "Existence and implementation of national diabetes prevention and control plan",
    2: "Existence and implementation of policies and legislation for diabetes prevention",
    3: "Existence and enforcement of tax on alcoholic beverages, tobacco, sugar-sweetened beverages, foods high in saturated fats, trans fats, free sugars and/or salt",
    4: "Existence of national guidelines for diabetes management",
    5: "Referral and back-referral system for diabetes management",
    6: "Insulin, insulin delivery devices and blood glucose self-monitoring included in health benefits package",
    7: "Insulin, insulin delivery devices and blood glucose self-monitoring affordability",
    8: "Availability of trained health care staff for diabetes management",
    9: "Availability of diabetes, cardiovascular disease and hypertension core medicines",
    10: "Availability of plasma glucose testing",
    11: "Availability of glycated haemoglobin (HbA1c) testing",
    12: "Availability and quality of diabetes surveillance system",

    13: "Overweight and obesity assessment",
    14: "Tobacco use assessment",
    15: "Cardiovascular disease risk assessment",
    16: "Hypertension screening",
    17: "Diabetes diagnosis",
    18: "Diabetic ketoacidosis at diagnosis",
    19: "Blood glucose measurement",
    20: "Retinopathy assessment",
    21: "Chronic kidney disease assessment",
    22: "Diabetic foot assessment",
    23: "Treatment with glucose-lowering medication",
    24: "Insulin treatment",
    25: "Statin treatment",
    26: "Treatment with blood pressure-lowering medication",
    27: "Retinopathy treatment",
    28: "Diabetic foot treatment",

    29: "Physical inactivity prevalence",
    30: "Overweight and obesity prevalence",
    31: "Tobacco use prevalence",
    32: "Hypertension prevalence",
    33: "Glycaemic control based on glycated haemoglobin (HbA1c)",
    34: "Glycaemic control based on fasting plasma glucose",
    35: "Blood pressure control",

    36: "Diabetes prevalence",
    37: "Hospitalization for diabetes",
    38: "Cardiovascular disease",
    39: "Blindness",
    40: "End-stage kidney disease",
    41: "Lower-extremity amputation",
    42: "Cardiovascular disease mortality rate",
    43: "Diabetes mortality rate",
    44: "Probability of premature mortality from noncommunicable diseases",
}


INDICATOR_PAGE_RANGES = {
    1: (30, 30),
    2: (31, 31),
    3: (32, 32),
    4: (33, 33),
    5: (34, 34),
    6: (35, 35),
    7: (36, 36),
    8: (37, 37),

    9: (38, 39),
    10: (40, 40),
    11: (41, 41),

    12: (42, 43),

    13: (45, 45),
    14: (46, 46),
    15: (47, 47),
    16: (48, 48),
    17: (49, 49),
    18: (50, 50),
    19: (51, 51),
    20: (52, 52),
    21: (53, 53),
    22: (54, 54),
    23: (55, 55),
    24: (56, 56),
    25: (57, 57),
    26: (58, 58),
    27: (59, 59),
    28: (60, 60),

    29: (62, 62),
    30: (63, 63),
    31: (64, 64),
    32: (65, 65),

    33: (66, 67),
    34: (68, 69),
    35: (70, 70),

    36: (72, 72),
    37: (73, 73),
    38: (74, 74),
    39: (75, 75),
    40: (76, 76),
    41: (77, 77),
    42: (78, 78),
    43: (79, 79),
    44: (80, 80),
}


def get_indicator_metadata(indicator_number: int) -> dict:
    if indicator_number not in INDICATORS:
        raise ValueError(
            f"Unknown indicator number: {indicator_number}"
        )

    return {
        "domain": DOMAINS[indicator_number],
        "subdomain": SUBDOMAINS[indicator_number],
        "indicator_number": indicator_number,
        "indicator_name": INDICATORS[indicator_number],
    }


def get_indicator_for_page(page_number: int) -> int | None:
    for indicator_number, (start_page, end_page) in INDICATOR_PAGE_RANGES.items():
        if start_page <= page_number <= end_page:
            return indicator_number

    return None