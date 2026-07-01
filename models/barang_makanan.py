from datetime import datetime
from models.barang import Barang

class BarangMakanan(Barang):
    def __init__(self, kode, nama, stok, kadaluarsa, halal):
        super().__init__(kode, nama, stok)
        self.__kadaluarsa = kadaluarsa
        self.__halal = halal

    def get_kadaluarsa(self):
        return self.__kadaluarsa
    
    def get_halal(self):
        return self.__halal
    
    def set_kadaluarsa(self, kadaluarsa):
        self.__kadaluarsa = kadaluarsa

    def set_halal(self, halal):
        self.__halal = halal

    def cek_kadaluarsa(self):
        expired = datetime.strptime(
            self.__kadaluarsa,
            "%d-%m-%Y"
        )
        return expired > datetime.now()
    
    def status_halal(self):
        if self.__halal.lower() == "ya":
            return "Halal"
        return "Non Halal"
    
    def kategori(self):
        return "Makanan"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "kadaluarsa": self.__kadaluarsa,
            "halal": self.__halal
        })
        return data