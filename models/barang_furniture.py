from models.barang import Barang

class BarangFurniture(Barang):

    def __init__(self, kode, nama, stok, material, berat):
        super().__init__(kode, nama, stok)

        self.__material = material
        self.__berat = berat

    def get_material(self):
        return self.__material

    def get_berat(self):
        return self.__berat

    def set_material(self, material):
        self.__material = material

    def set_berat(self, berat):
        self.__berat = berat

    def cek_material(self):
        return self.__material

    def estimasi_pengiriman(self):

        if self.__berat < 10:
            return "Pengiriman Ringan"

        return "Pengiriman Berat"

    def kategori(self):
        return "Furniture"

    def to_dict(self):

        data = super().to_dict()

        data.update({

            "material": self.__material,
            "berat": self.__berat

        })

        return data