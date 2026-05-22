import pandas as pd

def export_to_excel(test_cases):
    df = pd.DataFrame(test_cases)

    file_path = "test_cases.xlsx"
    df.to_excel(file_path, index=False)

    return file_path