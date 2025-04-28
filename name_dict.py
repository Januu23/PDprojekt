data = {}

# Pievienojam rezultātus
while True:
    # Ievadām vārdu, mēģinājumu skaitu, laiku un līmeni
    vards = input("Ievadiet vārdu: ")
    versi = int(input("Ievadiet {} mēģinājumu skaitu: ".format(vards)))
    laiks = int(input("Ievadiet {} laiku (sekundēs): ".format(vards)))
    level = int(input("Ievadiet {} izvēlēto līmeni: ".format(vards)))
    
    # Saglabājam datus vārdnīcā
    data[vards] = {'versi': versi, 'laiks': laiks, 'level': level}
    
    # Vai pievienot vēl vienu personu
    atk = input("Vai vēlaties pievienot vēl vienu personu? (j/n): ").strip().lower()
    if atk != 'j':
        break

# Ierakstām vārdnīcu failā
with open('rezultati.txt', 'a', encoding='utf-8') as file:
    for vards, info in data.items():
        file.write("{}: Mēģinājumi: {}, Laiks: {} sek., Līmenis: {}\n".format(vards, info['versi'], info['laiks'], info['level']))

print("Dati ir saglabāti failā.")