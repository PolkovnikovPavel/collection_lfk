line = '9' * 127
while '999' in line or '333' in line:
    print(line)
    if '333' in line:
        i = line.find('333')
        line = '9' + line[i + 3:]
    else:
        i = line.find('999')
        line = line[0:i] + '3' + line[i + 3:]
print(line)
