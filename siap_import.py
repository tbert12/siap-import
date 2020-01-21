import pandas as pd

LINE_BREAK = "/r/n"

""" Comprobante
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

VOUCHER_ZFILLS = [8, 3, 5, 20, 16, 2, 20, 30] + [15] * 8 + [3, 10, 1, 1, 15, 15, 11, 30, 15]
ALIQUOT_ZFILLS = [3, 5, 20, 2, 20, 15, 4, 15]

def read_csv(source):
    df = pd.read_csv(source)
    return df[pd.notnull(df['IVA']) & df["IVA"] > 0]

def convert_date(date):
    day, month, year = date.split('/')
    return f"{year}{month}{day}"

def voucher_type(voucher_desc):
    return voucher_desc.split(' ')[0]

def currency(curr):
    return "USD" if curr == "DOL" else "PES"

def convert_voucher(row):
    row_voucher_type = voucher_type(row['Tipo'])
    total = -float(row['Imp. Total']) if row_voucher_type == "3" else float(row['Imp. Total'])
    cells = [
        convert_date(row['Fecha']), 
        row_voucher_type,
        row['Punto de Venta'],
        row['Número Desde'],
        " " * 16,
        "80".ljust(2),
        row['Nro. Doc. Emisor'],
        row['Denominación Emisor'][:30].ljust(30),
        int(total * 100 + .5),
        0,
        0,
        0,
        0,
        0,
        0,
        int(row['Imp. Neto No Gravado'] * 100 + .5),
        currency(row['Moneda']),
        f"{float(row['Tipo Cambio']):.6f}".replace('.', ''),
        "1",
        "0",
        int(row["IVA"] * 100 + .5),
        "0",
        "0",
        " " * 30,
        "0",
    ]
    cells_fill = [str(cell).zfill(zeros) for cell, zeros in zip(cells, VOUCHER_ZFILLS)]
    return "".join(cells_fill)

def convert_aliquot(row):
    row_voucher_type = voucher_type(row['Tipo'])
    total = -float(row['Imp. Total']) if row_voucher_type == "3" else float(row['Imp. Total'])
    cells = [
        row_voucher_type,
        row['Punto de Venta'],
        row['Número Desde'],
        "80".ljust(2),
        row['Nro. Doc. Emisor'],
        int(row["Imp. Neto Gravado"] * 100 + .5),
        "5",
        int(row["IVA"] * 100 + .5),
    ]
    cells_fill = [str(cell).zfill(zeros) for cell, zeros in zip(cells, ALIQUOT_ZFILLS)]
    return "".join(cells_fill)

def convert_dataframe_voucher(df):
    return [convert_voucher(row) for _, row in df.iterrows()]

def convert_datafame_aliquot(df):
    return [convert_aliquot(row) for _, row in df.iterrows()]

def save_voucher_txt(filename, lines):
    filename_out = f"{filename.split('.', 1)[0]}-comprobante.txt"
    save_txt(filename_out, lines)

def save_aliquot_txt(filename, lines):
    filename_out = f"{filename.split('.', 1)[0]}-alicuota.txt"
    save_txt(filename_out, lines)

def save_txt(filename, lines):
    print(f"Saving in '{filename}'")
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f"{line}\r\n")

def process_voucher_raw(source):
    df = read_csv(source)
    lines = convert_dataframe_voucher(df)
    return "\r\n".join(lines), f"{source.filename.rsplit('.', 1)[0]}-comprobante.txt"

def process_aliquot_raw(source):
    df = read_csv(source)
    lines = convert_datafame_aliquot(df)
    return "\r\n".join(lines), f"{source.filename.rsplit('.', 1)[0]}-alicuota.txt"

if __name__ == '__main__':
    try:
        import sys
        filename = sys.argv[1]
        print(f"Converting '{filename}'")
        df = read_csv(filename)
        voucher_lines = convert_dataframe_voucher(df)
        save_voucher_txt(filename, voucher_lines)
        aliquot_lines = convert_datafame_aliquot(df)
        save_aliquot_txt(filename, aliquot_lines)
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
