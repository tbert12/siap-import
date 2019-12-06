from siap_import import save_txt, ZFILLS
lines = []
with open('example/out/Comprobantes.txt') as file:
    for raw_line in file:
        line = list(raw_line)[:-1]
        acc = 0
        for i, pos in enumerate(ZFILLS):
            line.insert(acc + i + pos, " ")
            acc+=pos
        print(line)
        lines.append("".join(line))

save_txt('example/out/Comprobantes-spaces.txt', lines)