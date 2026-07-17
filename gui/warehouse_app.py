import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class WarehouseApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("Warehouse Management System")
        self.root.geometry("950x600")
        self.root.configure(bg="#F3F4F6")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(".", font=("Segoe UI", 10), background="#F3F4F6", foreground="#1F2937")
        
        self.style.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI", 10),
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1F2937",
            borderwidth=0
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#EEF2FF")],
            foreground=[("selected", "#4F46E5")]
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#E5E7EB",
            foreground="#374151",
            relief="flat",
            padding=5
        )

        self.style.configure(
            "TCombobox",
            arrowcolor="#4F46E5",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            darkcolor="#FFFFFF",
            lightcolor="#FFFFFF"
        )

        self.buat_header()
        
        self.main_container = tk.Frame(self.root, bg="#F3F4F6")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        self.left_pane = tk.Frame(self.main_container, bg="#F3F4F6")
        self.left_pane.pack(side="left", fill="both", padx=(0, 10))
        self.right_pane = tk.Frame(self.main_container, bg="#F3F4F6")
        self.right_pane.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.buat_form()
        self.buat_tabel()
        self.refresh_table()

    def buat_header(self):
        header_frame = tk.Frame(self.root, bg="#4F46E5", height=60)
        header_frame.pack(fill="x", side="top")
        
        # Label Title
        title_label = tk.Label(
            header_frame,
            text=" 📦  Warehouse Inventory System",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#4F46E5",
            pady=15
        )
        title_label.pack(side="left", padx=20)

        exit_btn = tk.Button(
            header_frame,
            text="Keluar",
            command=self.konfirmasi_keluar,
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg="#EF4444",
            activebackground="#ff0000",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        exit_btn.pack(side="right", padx=20, pady=15, ipady=6, ipadx=12)

    def konfirmasi_keluar(self):
        ans = messagebox.askyesno("Konfirmasi Keluar", "Apakah Anda yakin ingin menutup aplikasi?")
        if ans:
            self.root.destroy()

    def buat_form(self):
        
        form_card = tk.Frame(self.left_pane,
                             bg="#FFFFFF",
                             bd=1,
                             relief="flat",
                             highlightbackground="#E5E7EB",
                             highlightthickness=1)
        
        form_card.pack(fill="both", expand=True, ipady=15)        
        
        canvas = tk.Canvas(form_card, bg="#FFFFFF", bd=0, highlightthickness=0, width=280)
        self.form_canvas = canvas 
        
        scrollbar = ttk.Scrollbar(form_card, orient="vertical", command=canvas.yview)

        inner_frame = tk.Frame(canvas, bg="#FFFFFF", bd=0, highlightthickness=0)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas_frame_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        def configure_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        def configure_canvas(event):
  
            canvas.itemconfig(canvas_frame_id, width=event.width)
            
        inner_frame.bind("<Configure>", configure_frame)
        canvas.bind("<Configure>", configure_canvas)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
            
        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        inner_frame.bind("<Enter>", _bind_mousewheel)
        inner_frame.bind("<Leave>", _unbind_mousewheel)

        tk.Label(
            inner_frame,
            text="Detail Barang",
            font=("Segoe UI", 12, "bold"),
            fg="#1F2937",
            bg="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(20, 15))

        def create_field(parent, label_text):
            frame = tk.Frame(parent, bg="#FFFFFF")
            frame.pack(fill="x", padx=20, pady=6)
            lbl = tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 9, "bold"),
                fg="#4B5563",
                bg="#FFFFFF"
            )
            lbl.pack(anchor="w", pady=(0, 4))
            entry = tk.Entry(
                frame,
                font=("Segoe UI", 10),
                bg="#F9FAFB",
                fg="#1F2937",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#D1D5DB",
                highlightcolor="#4F46E5",
                insertbackground="#1F2937"
            )
            entry.pack(fill="x", ipady=6)
            return entry

        self.kode_entry = create_field(inner_frame, "Kode Barang")
        self.nama_entry = create_field(inner_frame, "Nama Barang")
        self.stok_entry = create_field(inner_frame, "Stok Barang")

        cat_frame = tk.Frame(inner_frame, bg="#FFFFFF")
        cat_frame.pack(fill="x", padx=20, pady=6)
        tk.Label(
            cat_frame,
            text="Kategori",
            font=("Segoe UI", 9, "bold"),
            fg="#4B5563",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))
        
        self.kategori = ttk.Combobox(
            cat_frame,
            values=["Elektronik", "Makanan", "Furniture"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.kategori.pack(fill="x", ipady=4)
        self.kategori.current(0)
        
        self.kategori.bind("<MouseWheel>", lambda e: (self.form_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"), "break")[1])

        self.dynamic_frame = tk.Frame(inner_frame, bg="#FFFFFF")
        self.dynamic_frame.pack(fill="x", padx=20, pady=0)

        self.kategori.bind("<<ComboboxSelected>>", self.on_kategori_change)

        self.on_kategori_change()

        btn_frame = tk.Frame(inner_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", padx=20, pady=(25, 20))

        def create_button(parent, text, color, hover_color, command, row, col, columnspan=1):
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=("Segoe UI", 9, "bold"),
                fg="#FFFFFF",
                bg=color,
                activebackground=hover_color,
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                cursor="hand2"
            )
            btn.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=4, pady=5, ipady=8)

            btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
            return btn

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        create_button(btn_frame, "Tambah", "#10B981", "#059669", self.tambah_barang, row=0, col=0)
        create_button(btn_frame, "Update", "#F59E0B", "#D97706", self.update_barang, row=0, col=1)
        create_button(btn_frame, "Cari", "#3B82F6", "#2563EB", self.cari_barang, row=1, col=0)
        create_button(btn_frame, "Hapus", "#EF4444", "#DC2626", self.hapus_barang, row=1, col=1)

    def on_kategori_change(self, event=None):

        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
            
        cat = self.kategori.get()
        
        def create_dynamic_entry(label_text, is_combobox=False, values=None):
            frame = tk.Frame(self.dynamic_frame, bg="#FFFFFF")
            frame.pack(fill="x", pady=4)
            lbl = tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 9, "bold"),
                fg="#4B5563",
                bg="#FFFFFF"
            )
            lbl.pack(anchor="w", pady=(0, 2))
            if is_combobox:
                widget = ttk.Combobox(
                    frame,
                    values=values,
                    state="readonly",
                    font=("Segoe UI", 10)
                )
                widget.pack(fill="x", ipady=4)
                widget.current(0)
                
                widget.bind("<MouseWheel>", lambda e: (self.form_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"), "break")[1])
            else:
                widget = tk.Entry(
                    frame,
                    font=("Segoe UI", 10),
                    bg="#F9FAFB",
                    fg="#1F2937",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#D1D5DB",
                    highlightcolor="#4F46E5",
                    insertbackground="#1F2937"
                )
                widget.pack(fill="x", ipady=6)
            return widget

        if cat == "Elektronik":
            self.spec1_entry = create_dynamic_entry("Garansi (Bulan)")
            self.spec2_entry = create_dynamic_entry("Daya (Watt)")
        elif cat == "Makanan":
            self.spec1_entry = create_dynamic_entry("Tanggal Kadaluarsa (DD-MM-YYYY)")
            self.spec2_entry = create_dynamic_entry("Halal (Ya/Tidak)", is_combobox=True, values=["Ya", "Tidak"])
        elif cat == "Furniture":
            self.spec1_entry = create_dynamic_entry("Material / Bahan")
            self.spec2_entry = create_dynamic_entry("Berat (Kg)")

    def buat_tabel(self):
        table_card = tk.Frame(self.right_pane, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E5E7EB", highlightthickness=1)
        table_card.pack(fill="both", expand=True)
        
        tk.Label(
            table_card,
            text="Daftar Inventaris",
            font=("Segoe UI", 12, "bold"),
            fg="#1F2937",
            bg="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        kolom = (
            "Kode",
            "Nama",
            "Stok",
            "Kategori",
            "Garansi (bulan)",
            "Daya",
            "Expired",
            "Halal",
            "Material",
            "Berat (Kg)"
        )
        

        tree_frame = tk.Frame(table_card, bg="#FFFFFF")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=kolom,
            show="headings"
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        for col in kolom:
            self.tree.heading(col, text=col, anchor="w")
            if col == "Kode":
                self.tree.column(col, width=60, minwidth=50, anchor="w")
            elif col == "Nama":
                self.tree.column(col, width=130, minwidth=100, anchor="w")
            elif col == "Stok":
                self.tree.column(col, width=50, minwidth=40, anchor="w")
            elif col == "Kategori":
                self.tree.column(col, width=80, minwidth=70, anchor="w")
            elif col in ("Garansi", "Daya", "Expired", "Halal", "Material", "Berat (Kg)"):
                self.tree.column(col, width=80, minwidth=60, anchor="w")
                
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for barang in self.manager.tampilkan_semua():
            garansi = barang.get_garansi() if barang.kategori() == "Elektronik" else "-"
            daya = barang.get_daya() if barang.kategori() == "Elektronik" else "-"
            kadaluarsa = barang.get_kadaluarsa() if barang.kategori() == "Makanan" else "-"
            halal = barang.get_halal() if barang.kategori() == "Makanan" else "-"
            material = barang.get_material() if barang.kategori() == "Furniture" else "-"
            berat = barang.get_berat() if barang.kategori() == "Furniture" else "-"
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    barang.get_kode(),
                    barang.get_nama(),
                    barang.get_stok(),
                    barang.kategori(),
                    garansi,
                    daya,
                    kadaluarsa,
                    halal,
                    material,
                    berat
                )
            )

    def tambah_barang(self):
        try:
            kategori = self.kategori.get().strip()
            kode = self.kode_entry.get().strip()
            nama = self.nama_entry.get().strip()
            stok = self.stok_entry.get().strip()

            spec1 = self.spec1_entry.get().strip()
            spec2 = self.spec2_entry.get().strip()
            
            kwargs = {}
            if kategori == "Elektronik":
                try:
                    kwargs["garansi"] = int(spec1)
                except ValueError:
                    raise Exception("Garansi harus berupa angka bulat (Integer)!")
                try:
                    kwargs["daya"] = float(spec2)
                except ValueError:
                    raise Exception("Daya harus berupa angka desimal/bulat (Float)!")
            elif kategori == "Makanan":
                kwargs["kadaluarsa"] = spec1
                kwargs["halal"] = spec2
            elif kategori == "Furniture":
                kwargs["material"] = spec1
                try:
                    berat = float(spec2)
                    if berat > 1000.0:
                        raise Exception("Berat tidak boleh lebih dari 1000 Kg!")
                    kwargs["berat"] = berat
                except ValueError:
                    raise Exception("Berat harus berupa angka desimal/bulat (Float)!")
                
            self.manager.tambah_barang(kategori, kode, nama, stok, **kwargs)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo(
                "Sukses",
                "Data berhasil ditambahkan"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def update_barang(self):
        try:
            kategori = self.kategori.get().strip()
            kode = self.kode_entry.get().strip()
            nama = self.nama_entry.get().strip()
            stok = self.stok_entry.get().strip()

            spec1 = self.spec1_entry.get().strip()
            spec2 = self.spec2_entry.get().strip()
            
            kwargs = {}
            if kategori == "Elektronik":
                try:
                    kwargs["garansi"] = int(spec1)
                except ValueError:
                    raise Exception("Garansi harus berupa angka bulat (Integer)!")
                try:
                    kwargs["daya"] = float(spec2)
                except ValueError:
                    raise Exception("Daya harus berupa angka desimal/bulat (Float)!")
            elif kategori == "Makanan":
                kwargs["kadaluarsa"] = spec1
                kwargs["halal"] = spec2
            elif kategori == "Furniture":
                kwargs["material"] = spec1
                try:
                    berat = float(spec2)
                    if berat > 1000.0:
                        raise Exception("Berat tidak boleh lebih dari 1000 Kg!")
                    kwargs["berat"] = berat
                except ValueError:
                    raise Exception("Berat harus berupa angka desimal/bulat (Float)!")
                
            self.manager.update_barang(kode, nama, stok, **kwargs)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo(
                "Sukses",
                "Data berhasil diupdate"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def hapus_barang(self):
        try:
            kode = self.kode_entry.get().strip()
            self.manager.hapus_barang(kode)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo(
                "Sukses",
                "Data berhasil dihapus"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def cari_barang(self):
        search_win = tk.Toplevel(self.root)
        search_win.title("Pencarian Barang")
        search_win.geometry("600x480")
        search_win.configure(bg="#F3F4F6")
        search_win.transient(self.root) 
        search_win.grab_set() 
        
        s_header = tk.Frame(search_win, bg="#4F46E5", height=45)
        s_header.pack(fill="x", side="top")
        
        tk.Label(
            s_header,
            text="🔍 Cari Barang",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg="#4F46E5",
            pady=10
        ).pack(side="left", padx=15)
        
        s_container = tk.Frame(search_win, bg="#F3F4F6")
        s_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        inputs_card = tk.Frame(s_container, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E5E7EB", highlightthickness=1)
        inputs_card.pack(fill="x", pady=(0, 10))
        
        q_frame = tk.Frame(inputs_card, bg="#FFFFFF")
        q_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
        
        tk.Label(
            q_frame,
            text="Kode atau Nama Barang:",
            font=("Segoe UI", 9, "bold"),
            fg="#4B5563",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))
        
        q_entry = tk.Entry(
            q_frame,
            font=("Segoe UI", 10),
            bg="#F9FAFB",
            fg="#1F2937",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D1D5DB",
            highlightcolor="#4F46E5"
        )
        q_entry.pack(fill="x", ipady=5)

        cat_frame = tk.Frame(inputs_card, bg="#FFFFFF")
        cat_frame.pack(side="right", padx=15, pady=10)
        
        tk.Label(
            cat_frame,
            text="Kategori:",
            font=("Segoe UI", 9, "bold"),
            fg="#4B5563",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))
        
        s_cat_combo = ttk.Combobox(
            cat_frame,
            values=["Semua", "Elektronik", "Makanan", "Furniture"],
            state="readonly",
            font=("Segoe UI", 10),
            width=15
        )
        s_cat_combo.pack(fill="x", ipady=3)
        s_cat_combo.current(0)

        table_card = tk.Frame(s_container, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E5E7EB", highlightthickness=1)
        table_card.pack(fill="both", expand=True)
        
        kolom = ("Kode", "Nama", "Stok", "Kategori")
        tree_frame = tk.Frame(table_card, bg="#FFFFFF")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        s_tree = ttk.Treeview(
            tree_frame,
            columns=kolom,
            show="headings",
            height=8
        )
        s_tree.grid(row=0, column=0, sticky="nsew")
        
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=s_tree.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        s_tree.configure(yscrollcommand=v_scroll.set)
        
        for col in kolom:
            s_tree.heading(col, text=col, anchor="w")
            if col == "Kode":
                s_tree.column(col, width=70, anchor="w")
            elif col == "Nama":
                s_tree.column(col, width=180, anchor="w")
            elif col == "Stok":
                s_tree.column(col, width=60, anchor="w")
            elif col == "Kategori":
                s_tree.column(col, width=100, anchor="w")

        actions_frame = tk.Frame(s_container, bg="#F3F4F6")
        actions_frame.pack(fill="x", pady=(10, 0))      
    
        def run_search(event=None):
            for row in s_tree.get_children():
                s_tree.delete(row)
                
            query = q_entry.get().strip().lower()
            category_filter = s_cat_combo.get()
            
            all_items = self.manager.tampilkan_semua()
            for item in all_items:
               
                if category_filter != "Semua" and item.kategori() != category_filter:
                    continue
 
                name_match = item.get_nama().lower().startswith(query)
                code_match = item.get_kode().lower().startswith(query)
                
                if query and not (name_match or code_match):
                    continue
                    
                s_tree.insert(
                    "",
                    tk.END,
                    values=(
                        item.get_kode(),
                        item.get_nama(),
                        item.get_stok(),
                        item.kategori()
                    )
                )                
   
        q_entry.bind("<KeyRelease>", run_search)
        s_cat_combo.bind("<<ComboboxSelected>>", run_search)        
       
        run_search()
        
        def pilih_barang_pencarian():
            selected = s_tree.focus()
            if not selected:
                messagebox.showwarning("Peringatan", "Pilih barang dari tabel pencarian terlebih dahulu", parent=search_win)
                return
            data = s_tree.item(selected)["values"]
            
            barang = self.manager.cari_barang(str(data[0]))
            if barang:
                self.clear_form()
                self.kode_entry.insert(0, barang.get_kode())
                self.kode_entry.config(state="disabled")
                self.nama_entry.insert(0, barang.get_nama())
                self.stok_entry.insert(0, barang.get_stok())
                
                cat = barang.kategori()
                self.kategori.set(cat)
                self.kategori.config(state="disabled")
                self.on_kategori_change()
                
                if cat == "Elektronik":
                    self.spec1_entry.insert(0, barang.get_garansi())
                    self.spec2_entry.insert(0, barang.get_daya())
                elif cat == "Makanan":
                    self.spec1_entry.insert(0, barang.get_kadaluarsa())
                    self.spec2_entry.set(barang.get_halal())
                elif cat == "Furniture":
                    self.spec1_entry.insert(0, barang.get_material())
                    self.spec2_entry.insert(0, barang.get_berat())
                
                search_win.destroy()
   
        s_tree.bind("<Double-1>", lambda e: pilih_barang_pencarian())        
        
        btn_select = tk.Button(
            actions_frame,
            text="Pilih Barang",
            command=pilih_barang_pencarian,
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#10B981",
            activebackground="#059669",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn_select.pack(side="left", ipady=6, ipadx=15)        
      
        btn_close = tk.Button(
            actions_frame,
            text="Tutup",
            command=search_win.destroy,
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#EF4444",
            activebackground="#DC2626",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn_close.pack(side="right", ipady=6, ipadx=15)

    def pilih_data(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        data = self.tree.item(selected)["values"]
        self.clear_form()
        
        self.kode_entry.insert(0, data[0])
        self.kode_entry.config(state="disabled")
        self.nama_entry.insert(0, data[1])
        self.stok_entry.insert(0, data[2])

        cat = data[3]
        self.kategori.set(cat)
        self.kategori.config(state="disabled")
        self.on_kategori_change()

        if cat == "Elektronik":
            self.spec1_entry.insert(0, data[4])
            self.spec2_entry.insert(0, data[5])
        elif cat == "Makanan":
            self.spec1_entry.insert(0, data[6])
            self.spec2_entry.set(data[7])
        elif cat == "Furniture":
            self.spec1_entry.insert(0, data[8])
            self.spec2_entry.insert(0, data[9])

    def clear_form(self):
        self.kode_entry.config(state="normal")
        self.kode_entry.delete(0, tk.END)
        self.nama_entry.delete(0, tk.END)
        self.stok_entry.delete(0, tk.END)
        self.kategori.config(state="readonly")

        if hasattr(self, 'spec1_entry') and self.spec1_entry.winfo_exists():
            if isinstance(self.spec1_entry, ttk.Combobox):
                self.spec1_entry.set("")
            else:
                self.spec1_entry.delete(0, tk.END)

        if hasattr(self, 'spec2_entry') and self.spec2_entry.winfo_exists():
            if isinstance(self.spec2_entry, ttk.Combobox):
                self.spec2_entry.current(0)
            else:
                self.spec2_entry.delete(0, tk.END)