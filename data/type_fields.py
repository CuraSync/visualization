def type_field_getter (type):
    data = {}

    if type == 'full blood count':
        data['WBC'] = (['WBC', 'white blood count', 'leukocytes', 'white blood cell count'], 0)
        data['HGB'] = (['HGB', 'hemoglobin', 'hb'], 0)
        data['RBC'] = (['RBC', 'red blood cell count', 'erythrocyte count'], 0)
        data['HCT'] = (['HCT', 'hematocrit', 'packed cell volume'], 0)
        data['PLT'] = (['PLT', 'platelet count', 'thrombocyte count'], 0)
        data['NEUT'] = (['NEUT', 'neutrophils', 'neutrophil count', 'absolute neutrophil count'], 0)
        data['LYMPH'] = (['LYMPH', 'lymphocytes', 'lymphocyte count'], 0)
        data['EO'] = (['EO', 'eosinophils', 'eosinophil count'], 0)
        data['MONO'] = (['MONO', 'monocytes', 'monocyte count'], 0)
        data['BASO'] = (['BASO', 'basophils', 'basophil count'], 0)
        data['IG'] = (['IG', 'immature granulocytes', 'band cells', 'immature granulocyte count'], 0)
        data['MCV'] = (['MCV', 'mean corpuscular volume'], 0)
        data['MCH'] = (['MCH', 'mean corpuscular hemoglobin'], 0)
        data['MCHC'] = (['MCHC', 'mean corpuscular hemoglobin concentration'], 0)

    elif type == 'blood sugar':
        data['blood sugar'] = (['blood sugar', 'blood glucose', 'fasting blood sugar', 'HbA1c', 'A1C test', 'random blood sugar', 'glucose test'], 0)
        data['Fasting Blood Sugar'] = (['Fasting Glucose', 'Fasting Blood Sugar', 'Fasting Glucose Level'], 0)

    elif type == 'Serum Creatinine':
        data['Serum Creatinine'] = (['serum creatinine', 'scr', 'creatinine (serum)', 'serum creatinine level'], 0)
        data['estimate GFR'] = (['estimate GFR', 'Estimated Glomerular Filtration Rate'], 0)

    elif type == 'Serum Electrolytes':
        data['SODIUM'] = (['SODIUM', 'Serum Sodium', 'Na Level'], 0)
        data['POTASSIUM'] = (['POTASSIUM', 'Serum Potassium', 'K Level'], 0)
        data['CHLORIDE'] = (['CHLORIDE', 'Cl', 'Serum Chloride', 'Cl Level'], 0)

    elif type == 'GAMMA GT':
        data['Gamma-GT'] = (['Gamma-GT', 'GGT', 'Gamma-Glutamyl Transferase', 'Serum GGT', 'GGT (IU/mL)'], 0)

    elif type == 'lipid profile':
        data['Total Cholesterol'] = (['Total Cholesterol', 'Cholesterol', 'Total Cholesterol Level'], 0)
        data['HDL Cholesterol'] = (['HDL Cholesterol', 'HDL', 'HDL Cholesterol Level'], 0)
        data['LDL Cholesterol'] = (['LDL Cholesterol', 'LDL', 'LDL Cholesterol Level'], 0)

    elif type == 'thyroid function test':
        data['TSH'] = (['TSH', 'Thyroid-Stimulating Hormone', 'Thyrotropin', 'Serum TSH', 'TSH (mlU/mL)'], 0)

    return data