import os, sys, json, shutil, zipfile, subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

APP_NAME = "mcLauncher"
HOME = Path(os.getenv("APPDATA", str(Path.home()))) / APP_NAME
PACKS = HOME / "packs"
PROFILES = HOME / "profiles"
CONFIG = HOME / "config.json"

def bedrock_data():
    p = Path(os.getenv("LOCALAPPDATA", "")) / "Packages"
    if p.exists():
        matches = list(p.glob("Microsoft.MinecraftUWP_*")) + list(p.glob("Microsoft.MinecraftWindowsBeta_*"))
        for m in matches:
            candidate = m / "LocalState" / "games" / "com.mojang"
            if candidate.exists():
                return candidate
    return None

def load_config():
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return {"offline_name": "Jogador", "packs": []}

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        HOME.mkdir(parents=True, exist_ok=True)
        PACKS.mkdir(exist_ok=True)
        PROFILES.mkdir(exist_ok=True)
        self.cfg = load_config()
        self.title("mcLauncher")
        self.geometry("850x600")
        self.minsize(720, 500)
        self.configure(bg="#101810")
        self._style()
        self._ui()
        self.refresh()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background="#101810")
        s.configure("TLabel", background="#101810", foreground="#e8f5e9", font=("Segoe UI", 10))
        s.configure("Title.TLabel", font=("Segoe UI", 23, "bold"), foreground="#79d279")
        s.configure("TButton", background="#285c32", foreground="white", padding=9, font=("Segoe UI", 10, "bold"))
        s.map("TButton", background=[("active", "#397b45")])
        s.configure("Treeview", background="#17251a", foreground="white", fieldbackground="#17251a", rowheight=28)
        s.configure("Treeview.Heading", background="#285c32", foreground="white")

    def _ui(self):
        head = ttk.Frame(self, padding=18); head.pack(fill="x")
        ttk.Label(head, text="mcLauncher", style="Title.TLabel").pack(side="left")
        ttk.Label(head, text="BEDROCK • WINDOWS", foreground="#9ab59d").pack(side="right")
        self.tabs = ttk.Notebook(self); self.tabs.pack(fill="both", expand=True, padx=16, pady=(0,16))
        self.mods = ttk.Frame(self.tabs, padding=14); self.tabs.add(self.mods, text="  Mods e addons  ")
        self.versions = ttk.Frame(self.tabs, padding=14); self.tabs.add(self.versions, text="  Versões  ")
        self.account = ttk.Frame(self.tabs, padding=14); self.tabs.add(self.account, text="  Conta  ")
        self._mods_tab(); self._versions_tab(); self._account_tab()
        foot = ttk.Frame(self, padding=(16,0,16,12)); foot.pack(fill="x")
        ttk.Button(foot, text="▶  INICIAR MINECRAFT", command=self.launch).pack(side="left")
        ttk.Button(foot, text="↻  REINICIAR LAUNCHER", command=self.restart).pack(side="right")

    def _mods_tab(self):
        ttk.Label(self.mods, text="Gerencie seus pacotes e addons", style="Title.TLabel").pack(anchor="w", pady=(0,10))
        bar=ttk.Frame(self.mods); bar.pack(fill="x", pady=6)
        ttk.Button(bar, text="＋ Importar .mcaddon / .mcpack / .zip", command=self.import_pack).pack(side="left")
        ttk.Button(bar, text="Excluir selecionado", command=self.delete_pack).pack(side="right")
        self.packlist=ttk.Treeview(self.mods, columns=("type","path"), show="headings")
        self.packlist.heading("type", text="Arquivo"); self.packlist.heading("path", text="Local")
        self.packlist.column("type", width=230); self.packlist.column("path", width=450)
        self.packlist.pack(fill="both", expand=True, pady=10)
        ttk.Label(self.mods, text="Os arquivos .mcaddon/.mcpack são abertos pelo Minecraft para importação oficial. ZIP é guardado no gerenciador.", foreground="#a9c5ad").pack(anchor="w")

    def _versions_tab(self):
        ttk.Label(self.versions, text="Versões e perfis", style="Title.TLabel").pack(anchor="w", pady=(0,10))
        self.version_info=ttk.Label(self.versions, text="Verificando instalação do Minecraft…")
        self.version_info.pack(anchor="w", pady=8)
        ttk.Button(self.versions, text="Atualizar detecção", command=self.refresh).pack(anchor="w", pady=6)
        ttk.Label(self.versions, text="O Bedrock é distribuído e atualizado pela Microsoft Store/Xbox. Este launcher não baixa nem redistribui versões antigas do jogo.", wraplength=700, foreground="#a9c5ad").pack(anchor="w", pady=12)
        ttk.Label(self.versions, text="Perfis locais do mcLauncher", style="Title.TLabel").pack(anchor="w", pady=(18,8))
        row=ttk.Frame(self.versions); row.pack(fill="x")
        ttk.Button(row, text="＋ Criar perfil", command=self.create_profile).pack(side="left")
        ttk.Button(row, text="Excluir perfil", command=self.delete_profile).pack(side="right")
        self.profilelist=tk.Listbox(self.versions, bg="#17251a", fg="white", selectbackground="#397b45", height=7)
        self.profilelist.pack(fill="x", pady=8)

    def _account_tab(self):
        ttk.Label(self.account, text="Conta", style="Title.TLabel").pack(anchor="w", pady=(0,12))
        ttk.Label(self.account, text="Perfil offline (apenas identificação local)", foreground="#a9c5ad").pack(anchor="w")
        row=ttk.Frame(self.account); row.pack(fill="x", pady=8)
        self.name=tk.StringVar(value=self.cfg.get("offline_name","Jogador"))
        ttk.Entry(row, textvariable=self.name, width=35).pack(side="left", padx=(0,8))
        ttk.Button(row, text="Salvar nome", command=self.save_name).pack(side="left")
        ttk.Separator(self.account).pack(fill="x", pady=18)
        ttk.Label(self.account, text="Conta Microsoft", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self.account, text="Use o botão abaixo para abrir o Minecraft oficial, onde o login Microsoft é realizado com segurança. O mcLauncher não coleta senhas nem tokens.", wraplength=700).pack(anchor="w", pady=8)
        ttk.Button(self.account, text="Abrir Minecraft para entrar na conta", command=self.launch).pack(anchor="w", pady=6)
        ttk.Label(self.account, text="Importante: o perfil offline não autentica nos serviços Xbox, Realms ou multiplayer online.", foreground="#e6c878", wraplength=700).pack(anchor="w", pady=12)

    def save(self):
        CONFIG.write_text(json.dumps(self.cfg, indent=2, ensure_ascii=False), encoding="utf-8")

    def save_name(self):
        name=self.name.get().strip()
        if not name: messagebox.showwarning("mcLauncher","Digite um nome."); return
        self.cfg["offline_name"]=name; self.save()
        messagebox.showinfo("mcLauncher","Nome do perfil salvo.")

    def import_pack(self):
        paths=filedialog.askopenfilenames(title="Escolha addons", filetypes=[("Addons e ZIP","*.mcaddon *.mcpack *.zip"),("Todos","*.*")])
        if not paths: return
        for src in paths:
            src=Path(src); dest=PACKS/src.name
            if dest.exists():
                dest=PACKS/(src.stem+"_copy"+src.suffix)
            shutil.copy2(src,dest)
            if src.suffix.lower() in (".mcaddon",".mcpack"):
                try: os.startfile(str(dest))
                except Exception: pass
        self.refresh()
        messagebox.showinfo("mcLauncher","Arquivo(s) guardado(s). Para .mcaddon/.mcpack, confirme a importação na janela do Minecraft.")

    def delete_pack(self):
        sel=self.packlist.selection()
        if not sel: return
        item=self.packlist.item(sel[0]); path=Path(item["values"][1])
        if messagebox.askyesno("Excluir addon",f"Excluir {path.name} do gerenciador?"):
            try: path.unlink()
            except Exception as e: messagebox.showerror("Erro",str(e))
            self.refresh()

    def create_profile(self):
        name=simpledialog.askstring("Novo perfil","Nome do perfil:")
        if not name: return
        safe="".join(c for c in name if c.isalnum() or c in " _-").strip()
        if safe: (PROFILES/safe).mkdir(exist_ok=True); self.refresh()

    def delete_profile(self):
        sel=self.profilelist.curselection()
        if not sel: return
        name=self.profilelist.get(sel[0])
        if messagebox.askyesno("Excluir perfil",f"Excluir o perfil '{name}'?"):
            shutil.rmtree(PROFILES/name, ignore_errors=True); self.refresh()

    def refresh(self):
        if hasattr(self,"packlist"):
            for x in self.packlist.get_children(): self.packlist.delete(x)
            for p in sorted(PACKS.iterdir()):
                if p.is_file(): self.packlist.insert("", "end", values=(p.name,str(p)))
        if hasattr(self,"version_info"):
            data=bedrock_data()
            self.version_info.config(text=("Minecraft Bedrock detectado. Dados: "+str(data)) if data else "Minecraft Bedrock não detectado. Instale-o pela Microsoft Store/Xbox.")
            self.profilelist.delete(0,"end")
            for p in sorted(PROFILES.iterdir()):
                if p.is_dir(): self.profilelist.insert("end",p.name)

    def launch(self):
        try:
            subprocess.Popen(["explorer.exe","shell:AppsFolder\\Microsoft.MinecraftUWP_8wekyb3d8bbwe!App"])
        except Exception:
            try: os.startfile("minecraft:")
            except Exception: messagebox.showwarning("mcLauncher","Não encontrei o Minecraft. Instale/abra pela Microsoft Store ou Xbox.")

    def restart(self):
        self.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    Launcher().mainloop()
