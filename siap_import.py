import pandas as pd

LINE_BREAK = "/r/n"

"""
"Fecha",
"Tipo",
"Punto de Venta",
"Número Desde",
"Número Hasta",
"Cód. Autorización",
"Tipo Doc. Emisor",
"Nro. Doc. Emisor",
"Denominación Emisor",
"Tipo Cambio",
"Moneda",
"Imp. Neto Gravado",
"Imp. Neto No Gravado",
"Imp. Op. Exentas",
"IVA",
"Imp. Total"
"""

ZFILLS = [8, 3, 5, 20, 16, 2, 20, 30] + [15] * 8 + [3, 10, 1, 1, 15, 15, 11, 30, 15]

def read_csv(source):
    df = pd.read_csv(source)
    return df[pd.notnull(df['IVA']) & df["IVA"] > 0]

def convert_date(date):
    day, month, year = date.split('/')
    return f"{year}{month}{day}"

def voucher_type(voucher_desc):
    return voucher_desc.split(' ')[0]

def currency(curr):
    return "USD" if curr == "USD" else "PES"

def convert_row(row):
    cells = [
        convert_date(row['Fecha']), 
        voucher_type(row['Tipo']),
        row['Punto de Venta'],
        row['Número Desde'],
        "0",
        "8",
        row['Nro. Doc. Emisor'],
        row['Denominación Emisor'][:30],
        int(row['Imp. Total'] * 100),
        0,
        0,
        0,
        0,
        0,
        0,
        int(row['Imp. Neto No Gravado'] * 100),
        currency(row['Moneda']),
        f"{float(row['Tipo Cambio']):.6f}".replace('.', ''),
        "1",
        "0",
        int(row["IVA"] * 100),
        "0",
        "0",
        "0",
        "0",
    ]
    cells_fill = [str(cell).zfill(zeros) for cell, zeros in zip(cells, ZFILLS)]
    return "".join(cells_fill)

def convert_dataframe(df):
    return [convert_row(row) for _, row in df.iterrows()]

def save_txt(lines):
    with open('example/example-siap.txt', 'w') as f:
        for line in lines:
            f.write(f"{line}\r\n")

def process_raw(source):
    df = read_csv(source)
    lines = convert_dataframe(df)
    return "\r\n".join(lines)

if __name__ == '__main__':
    try:
        df = read_csv('example/example.csv')
        lines = convert_dataframe(df)
        save_txt(lines)
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
