from models.barang import Barang

class BarangElektronik(Barang):
    def __init__(self, kode, nama, stok, garansi, daya):
        super().__init__(kode, nama, stok)
        self.__garansi = garansi
        self.__daya = daya

    def get_garansi(self):
        return self.__garansi
    
    def get_daya(self):
        return self.__daya
    
    def set_garansi(self, garansi):
        self.__garansi = garansi

    def set_daya(self, daya):
        self.__daya = daya

    def masa_garansi(self):
        return f"{self.__garansi} Bulan"
    
    def cek_daya(self):
        return f"{self.__daya} Watt"
    
    def kategori(self):
        return "Elektronik"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "garansi": self.__garansi,
            "daya": self.__daya
        })
        return data