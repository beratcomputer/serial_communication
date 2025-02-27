# edit parameters below and get the neseccary c files.
# output files: "protocol.c", "protocol.h"



# ENUM CREATOR
def write_enum_to_h(enum_dict, enum_name, filename="protocol.h"):
    """
    Verilen dictionary ve enum ismine göre bir enum tanımını .h dosyasına ekler.
    
    Parameters:
    enum_dict (dict): Enum'da kullanılacak anahtar-değer çiftleri.
    enum_name (str): Oluşturulacak enum'un adı.
    filename (str): Yazılacak .h dosyasının adı (varsayılan: "parameters.h").
    """
    # Enum tanımını oluşturma
    enum_def = f"typedef enum {{\n"
    for key, value in enum_dict.items():
        enum_def += f"    {key} = {value},\n"
    enum_def += f"}} {enum_name};\n\n"
    
    # Dosyaya ekleme yapma
    with open(filename, "a") as file:
        file.write(enum_def)

enum1 = {
    "PARAMETER1": 10,
    "PARAMETER2": 11,
    "PARAMETER3": 12,
}

# İkinci enum için farklı bir dictionary
enum2 = {
    "VALUE_A": 100,
    "VALUE_B": 200,
    "VALUE_C": 300,
    "VALUE_D": 400,
}

write_enum_to_h(enum1, "FirstEnum")
write_enum_to_h(enum2, "SecondEnum")

print("Enum tanımları belirtilen .h dosyasına başarıyla eklendi.")