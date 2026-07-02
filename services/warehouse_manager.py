from models.barang import Barang
from models.barang_elektronik import BarangElektronik
from models.barang_makanan import BarangMakanan
from models.barang_furniture import BarangFurniture
from datetime import datetime

class WarehouseManager:
    def __init__(self, storage):
        self.storage = storage
        self.barang_list = []
        self.load_data()

    def load_data(self):
        data = self.storage.load()
        for item in data:
            try:
                barang = Barang.from_dict(item)
                self.barang_list.append(barang)
            except Exception as e:
                print(f"Error loading item from JSON: {e}")

    def save_data(self):
        data = [barang.to_dict() for barang in self.barang_list]
        self.storage.save(data)

    def tambah_barang(self, kategori, kode, nama, stok_str, **kwargs):
        kode = kode.strip()
        nama = nama.strip()
        stok_str = stok_str.strip()
        kategori = kategori.strip()

        if not kode:
            raise ValueError("Kode barang tidak boleh kosong")
        if not nama:
            raise ValueError("Nama barang tidak boleh kosong")
        if not stok_str:
            raise ValueError("Stok tidak boleh kosong")
        if not Barang.validasi_kode(kode):
            raise ValueError("Kode barang harus berupa angka")
        
        try:
            stok = int(stok_str)
        except ValueError:
            raise ValueError("Stok harus berupa angka")
        
        if stok <= 0:
            raise ValueError("Stok tidak boleh 0 atau kurang")
        if self.cari_barang(kode):
            raise ValueError(f"Barang dengan kode {kode} sudah terdaftar")

        if kategori == "Elektronik":
            garansi = kwargs.get("garansi", "").strip()
            daya = kwargs.get("daya", "").strip()
            if not garansi:
                raise ValueError("Masa garansi tidak boleh kosong")
            if not daya:
                raise ValueError("Daya listrik tidak boleh kosong")
            barang = BarangElektronik(kode, nama, stok, garansi, daya)

        elif kategori == "Makanan":
            kadaluarsa = kwargs.get("kadaluarsa", "").strip()
            halal = kwargs.get("halal", "").strip()
            if not kadaluarsa:
                raise ValueError("Tanggal kadaluarsa tidak boleh kosong")
            if not halal:
                raise ValueError("Status halal tidak boleh kosong")
            try:
                datetime.strptime(kadaluarsa, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Format tanggal kadaluarsa harus DD-MM-YYYY (contoh: 31-12-2026)")
            barang = BarangMakanan(kode, nama, stok, kadaluarsa, halal)

        elif kategori == "Furniture":
            material = kwargs.get("material", "").strip()
            berat_str = kwargs.get("berat", "").strip()
            if not material:
                raise ValueError("Material tidak boleh kosong")
            if not berat_str:
                raise ValueError("Berat tidak boleh kosong")
            try:
                berat = float(berat_str)
            except ValueError:
                raise ValueError("Berat harus berupa angka")
            if berat <= 0:
                raise ValueError("Berat tidak boleh 0 atau kurang")
            barang = BarangFurniture(kode, nama, stok, material, berat)

        else:
            raise ValueError(f"Kategori tidak dikenal: {kategori}")

        self.barang_list.append(barang)
        self.save_data()
        return barang

    def tampilkan_semua(self):
        return self.barang_list

    def cari_barang(self, kode):
        for barang in self.barang_list:
            if barang.get_kode() == kode:
                return barang
        return None

    def update_barang(self, kode, nama, stok_str, **kwargs):
        kode = kode.strip()
        nama = nama.strip()
        stok_str = stok_str.strip()

        if not kode:
            raise ValueError("Kode barang tidak boleh kosong")
        if not nama:
            raise ValueError("Nama barang tidak boleh kosong")
        if not stok_str:
            raise ValueError("Stok tidak boleh kosong")
        
        try:
            stok = int(stok_str)
        except ValueError:
            raise ValueError("Stok harus berupa angka")
        
        if stok <= 0:
            raise ValueError("Stok tidak boleh 0 atau kurang")

        barang = self.cari_barang(kode)
        if not barang:
            raise ValueError(f"Barang dengan kode {kode} tidak ditemukan")

        barang.set_nama(nama)
        barang.set_stok(stok)

        if barang.kategori() == "Elektronik":
            garansi = kwargs.get("garansi", "").strip()
            daya = kwargs.get("daya", "").strip()
            if not garansi:
                raise ValueError("Masa garansi tidak boleh kosong")
            if not daya:
                raise ValueError("Daya listrik tidak boleh kosong")
            barang.set_garansi(garansi)
            barang.set_daya(daya)
            
        elif barang.kategori() == "Makanan":
            kadaluarsa = kwargs.get("kadaluarsa", "").strip()
            halal = kwargs.get("halal", "").strip()
            if not kadaluarsa:
                raise ValueError("Tanggal kadaluarsa tidak boleh kosong")
            if not halal:
                raise ValueError("Status halal tidak boleh kosong")
            try:
                datetime.strptime(kadaluarsa, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Format tanggal kadaluarsa harus DD-MM-YYYY (contoh: 31-12-2026)")
            barang.set_kadaluarsa(kadaluarsa)
            barang.set_halal(halal)

        elif barang.kategori() == "Furniture":
            material = kwargs.get("material", "").strip()
            berat_str = kwargs.get("berat", "").strip()
            if not material:
                raise ValueError("Material tidak boleh kosong")
            if not berat_str:
                raise ValueError("Berat tidak boleh kosong")
            try:
                berat = float(berat_str)
            except ValueError:
                raise ValueError("Berat harus berupa angka")
            
            if berat <= 0:
                raise ValueError("Berat tidak boleh 0 atau kurang")
            barang.set_material(material)
            barang.set_berat(berat)

        self.save_data()
        return barang

    def hapus_barang(self, kode):
        kode = kode.strip()
        if not kode:
            raise ValueError("Masukkan kode barang terlebih dahulu")
        barang = self.cari_barang(kode)
        if not barang:
            raise ValueError(f"Barang dengan kode {kode} tidak ditemukan")
        self.barang_list.remove(barang)
        self.save_data()