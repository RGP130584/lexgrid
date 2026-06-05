"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { 
  Key, 
  Plus, 
  Check, 
  Copy, 
  ShieldCheck, 
  ArrowLeft, 
  Search, 
  X, 
  Activity, 
  RotateCw,
  Eye,
  EyeOff,
  Lock,
  User as UserIcon,
  LogOut,
  ShieldAlert,
  AlertTriangle
} from "lucide-react";

interface AccessKey {
  id: number;
  key_hash: string;
  max_uses: number;
  current_uses: number;
  is_active: boolean;
  created_at: string | null;
}

export default function AdminDashboard() {
  const [isAdminLoggedIn, setIsAdminLoggedIn] = useState<boolean>(false);
  const [adminUser, setAdminUser] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [showAdminPassword, setShowAdminPassword] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loginSuccess, setLoginSuccess] = useState(false);

  const [keys, setKeys] = useState<AccessKey[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [generating, setGenerating] = useState(false);
  const [newKey, setNewKey] = useState<string | null>(null);
  const [copiedKeyId, setCopiedKeyId] = useState<number | null>(null);
  const [copiedNewKey, setCopiedNewKey] = useState(false);
  const [showSensitive, setShowSensitive] = useState(true);

  const API_BASE_URL = "http://localhost:8003/api";

  const fetchKeys = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE_URL}/admin-control/keys`);
      if (!res.ok) {
        throw new Error("Erro ao buscar a lista de chaves de acesso.");
      }
      const data = await res.json();
      setKeys(data);
    } catch (err: any) {
      setError(err.message || "Falha na comunicação com o servidor.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const session = typeof window !== "undefined" ? localStorage.getItem("lexgrid_admin_auth") : null;
    if (session === "true") {
      setIsAdminLoggedIn(true);
      fetchKeys();
    }
  }, []);

  const handleAdminLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);
    
    const normalizedUser = adminUser.trim().toLowerCase();
    
    if (normalizedUser === "ricardo" && adminPassword === "LEX@123") {
      setLoginSuccess(true);
      setTimeout(() => {
        localStorage.setItem("lexgrid_admin_auth", "true");
        setIsAdminLoggedIn(true);
        fetchKeys();
        setLoginSuccess(false);
      }, 1000);
    } else {
      setLoginError("Usuário ou senha incorretos.");
    }
  };

  const handleAdminLogout = () => {
    localStorage.removeItem("lexgrid_admin_auth");
    setIsAdminLoggedIn(false);
    setKeys([]);
    setAdminUser("");
    setAdminPassword("");
  };

  const handleToggle = async (keyId: number) => {
    try {
      const res = await fetch(`${API_BASE_URL}/admin-control/keys/${keyId}/toggle`, {
        method: "POST"
      });
      if (!res.ok) {
        throw new Error("Não foi possível alterar o status da chave.");
      }
      const data = await res.json();
      
      // Update local state
      setKeys(prev => 
        prev.map(k => k.id === keyId ? { ...k, is_active: data.is_active } : k)
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alternar status.");
    }
  };

  const handleGenerateKey = async () => {
    try {
      setGenerating(true);
      const res = await fetch(`${API_BASE_URL}/admin-control/generate-key`, {
        method: "POST"
      });
      if (!res.ok) {
        throw new Error("Falha ao gerar nova chave de acesso.");
      }
      const data = await res.json();
      setNewKey(data.key);
      fetchKeys(); // Refresh list
    } catch (err: any) {
      alert(err.message || "Erro ao gerar chave.");
    } finally {
      setGenerating(false);
    }
  };

  const handleCopy = (text: string, id: number | null = null) => {
    navigator.clipboard.writeText(text);
    if (id !== null) {
      setCopiedKeyId(id);
      setTimeout(() => setCopiedKeyId(null), 2000);
    } else {
      setCopiedNewKey(true);
      setTimeout(() => setCopiedNewKey(false), 2000);
    }
  };

  // Stats calculations
  const totalKeys = keys.length;
  const activeKeys = keys.filter(k => k.is_active).length;
  const totalUses = keys.reduce((acc, curr) => acc + curr.current_uses, 0);

  // Filter keys
  const filteredKeys = keys.filter(k => 
    k.key_hash.toLowerCase().includes(search.toLowerCase())
  );

  // Login Gate
  if (!isAdminLoggedIn) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-4 relative overflow-hidden font-sans">
        {/* Restrictive ambient glows */}
        <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-rose-500/10 rounded-full blur-[100px] pointer-events-none"></div>
        <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-80 h-80 bg-violet-500/10 rounded-full blur-[100px] pointer-events-none"></div>

        <div className="w-full max-w-md bg-slate-900/85 border border-slate-800 p-8 rounded-2xl shadow-2xl backdrop-blur-md relative z-10 space-y-6">
          <div className="text-center space-y-2">
            <div className="inline-flex p-3 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl mb-2">
              <ShieldAlert className="w-8 h-8 animate-pulse" />
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Painel Administrativo</h2>
            <p className="text-sm text-slate-400">Autentique-se com suas credenciais para gerenciar o sistema.</p>
          </div>

          {loginSuccess ? (
            <div className="p-4 bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 rounded-xl text-center text-sm font-medium animate-pulse">
              🔓 Acesso Autorizado! Carregando painel...
            </div>
          ) : (
            <form onSubmit={handleAdminLogin} className="space-y-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-400 block ml-1">Usuário</label>
                <div className="relative">
                  <UserIcon className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input 
                    type="text" 
                    value={adminUser}
                    onChange={(e) => {
                      setAdminUser(e.target.value);
                      setLoginError(null);
                    }}
                    placeholder="Nome de usuário"
                    required
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm text-slate-200 placeholder-slate-700 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500/20 transition-all text-white"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-400 block ml-1">Senha</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input 
                    type={showAdminPassword ? "text" : "password"} 
                    value={adminPassword}
                    onChange={(e) => {
                      setAdminPassword(e.target.value);
                      setLoginError(null);
                    }}
                    placeholder="••••••••"
                    required
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-10 py-3 text-sm text-slate-200 placeholder-slate-700 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500/20 transition-all text-white"
                  />
                  <button
                    type="button"
                    onClick={() => setShowAdminPassword(!showAdminPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
                  >
                    {showAdminPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {loginError && (
                <p className="text-xs text-rose-400 text-center font-medium animate-shake">{loginError}</p>
              )}
              
              <button 
                type="submit" 
                className="w-full py-3 bg-rose-600 hover:bg-rose-500 active:bg-rose-700 text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-rose-600/10 border border-rose-500/25 flex items-center justify-center gap-2 hover:scale-[1.01] active:scale-[0.99] mt-2"
              >
                <span>Entrar no Painel</span>
              </button>
            </form>
          )}

          <div className="text-center pt-2 flex justify-between items-center text-[10px] font-mono text-slate-650">
            <Link href="/" className="hover:text-slate-400 transition-colors flex items-center gap-1">
              <ArrowLeft className="w-3 h-3" /> Voltar ao Dashboard
            </Link>
            <span className="tracking-wider uppercase">LexGrid Security Guard</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col relative overflow-hidden font-sans animate-in fade-in duration-300">
      {/* Background gradients */}
      <div className="absolute top-0 left-1/4 -translate-x-1/2 w-[500px] h-[500px] bg-sky-500/5 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 translate-x-1/2 w-[500px] h-[500px] bg-violet-500/5 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Navbar */}
      <header className="border-b border-slate-900 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-sky-500/10 border border-sky-500/20 text-sky-400 rounded-lg">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight text-white flex items-center gap-2">
                LexGrid <span className="text-xs bg-sky-500/15 border border-sky-500/30 text-sky-400 font-mono px-2 py-0.5 rounded-full font-medium">ADMIN</span>
              </span>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <Link 
              href="/"
              className="flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors bg-slate-900 border border-slate-800 px-3.5 py-2 rounded-xl hover:border-slate-700"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Dashboard Principal
            </Link>
            <button 
              onClick={handleAdminLogout}
              className="flex items-center gap-2 text-xs font-semibold text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 transition-colors bg-slate-900 border border-slate-800 hover:border-rose-950 px-3.5 py-2 rounded-xl"
            >
              <LogOut className="w-3.5 h-3.5" />
              Sair
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10 space-y-8">
        
        {/* Title and Action header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white">Chaves de Acesso Beta</h1>
            <p className="text-sm text-slate-400 mt-1">Gerencie os códigos temporários para homologação de usuários no sistema LexGrid.</p>
          </div>
          
          <button
            onClick={handleGenerateKey}
            disabled={generating}
            className="inline-flex items-center justify-center gap-2 px-5 py-3 bg-sky-600 hover:bg-sky-500 active:bg-sky-700 text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-sky-600/10 border border-sky-500/25 disabled:opacity-50 hover:scale-[1.01] active:scale-[0.99]"
          >
            <Plus className="w-4 h-4" />
            {generating ? "Gerando..." : "Gerar Nova Chave Beta"}
          </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <div className="bg-slate-900/40 border border-slate-850 p-6 rounded-2xl backdrop-blur-sm relative overflow-hidden group hover:border-slate-800 transition-colors">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400 font-medium">Chaves Geradas</span>
              <div className="p-2 bg-slate-800/60 rounded-xl text-slate-400">
                <Key className="w-5 h-5" />
              </div>
            </div>
            <div className="mt-4">
              <span className="text-3xl font-bold text-white tracking-tight">{loading ? "..." : totalKeys}</span>
            </div>
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-sky-500/0 via-sky-500/20 to-sky-500/0"></div>
          </div>

          <div className="bg-slate-900/40 border border-slate-850 p-6 rounded-2xl backdrop-blur-sm relative overflow-hidden group hover:border-slate-800 transition-colors">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400 font-medium">Chaves Ativas</span>
              <div className="p-2 bg-slate-800/60 rounded-xl text-emerald-400">
                <Check className="w-5 h-5" />
              </div>
            </div>
            <div className="mt-4">
              <span className="text-3xl font-bold text-white tracking-tight">{loading ? "..." : activeKeys}</span>
            </div>
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-emerald-500/0 via-emerald-500/20 to-emerald-500/0"></div>
          </div>

          <div className="bg-slate-900/40 border border-slate-850 p-6 rounded-2xl backdrop-blur-sm relative overflow-hidden group hover:border-slate-800 transition-colors">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400 font-medium">Total de Utilizações</span>
              <div className="p-2 bg-slate-800/60 rounded-xl text-violet-400">
                <Activity className="w-5 h-5" />
              </div>
            </div>
            <div className="mt-4">
              <span className="text-3xl font-bold text-white tracking-tight">{loading ? "..." : totalUses}</span>
            </div>
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-violet-500/0 via-violet-500/20 to-violet-500/0"></div>
          </div>
        </div>

        {/* Highlight box for newly generated key */}
        {newKey && (
          <div className="bg-sky-500/5 border border-sky-500/30 p-6 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 animate-in fade-in slide-in-from-top-4 duration-300">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-sky-500/10 border border-sky-500/20 text-sky-400 rounded-xl">
                <Key className="w-6 h-6 animate-pulse" />
              </div>
              <div>
                <h3 className="font-semibold text-white">Nova Chave de Acesso Criada!</h3>
                <p className="text-xs text-slate-400 mt-0.5">Copie esta chave e envie para o testador beta. Ela possui 5 usos por padrão.</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3 w-full md:w-auto">
              <div className="flex-1 md:flex-initial bg-slate-950 border border-slate-850 rounded-xl px-4 py-2.5 font-mono text-xl font-bold tracking-widest text-sky-400 text-center select-all">
                {newKey}
              </div>
              <button
                onClick={() => handleCopy(newKey)}
                className="p-3 bg-slate-900 border border-slate-800 hover:border-slate-700 hover:text-white rounded-xl transition-all"
                title="Copiar Chave"
              >
                {copiedNewKey ? <Check className="w-5 h-5 text-emerald-400" /> : <Copy className="w-5 h-5" />}
              </button>
              <button
                onClick={() => setNewKey(null)}
                className="p-3 bg-slate-900/50 hover:bg-slate-900 text-slate-400 hover:text-white rounded-xl transition-all"
                title="Fechar"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}

        {/* Table & Controls Section */}
        <div className="bg-slate-900/30 border border-slate-900 rounded-2xl overflow-hidden backdrop-blur-sm">
          
          {/* Table Controls */}
          <div className="p-5 border-b border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:max-w-xs">
              <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Buscar chave..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full bg-slate-950 border border-slate-850 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-slate-700 focus:ring-1 focus:ring-slate-800 transition-all text-white"
              />
              {search && (
                <button 
                  onClick={() => setSearch("")} 
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            <div className="flex items-center gap-3 self-end sm:self-auto">
              <button
                onClick={() => setShowSensitive(!showSensitive)}
                className="p-2 bg-slate-950 border border-slate-850 hover:border-slate-800 hover:text-white rounded-xl text-slate-400 text-xs font-medium flex items-center gap-1.5 transition-all"
                title={showSensitive ? "Ocultar chaves" : "Mostrar chaves"}
              >
                {showSensitive ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                <span className="hidden sm:inline">{showSensitive ? "Mascarar" : "Revelar"}</span>
              </button>
              
              <button
                onClick={fetchKeys}
                className="p-2 bg-slate-950 border border-slate-850 hover:border-slate-800 hover:text-white rounded-xl text-slate-400 text-xs font-medium flex items-center gap-1.5 transition-all"
                title="Atualizar Tabela"
              >
                <RotateCw className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Atualizar</span>
              </button>
            </div>
          </div>

          {/* Error display */}
          {error && (
            <div className="p-8 text-center space-y-3">
              <AlertTriangle className="w-8 h-8 text-amber-500 mx-auto" />
              <p className="text-sm text-slate-400">{error}</p>
              <button
                onClick={fetchKeys}
                className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-lg text-xs font-semibold"
              >
                Tentar Novamente
              </button>
            </div>
          )}

          {/* Table display */}
          {!error && (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-900 text-xs font-semibold tracking-wider text-slate-500 bg-slate-950/20">
                    <th className="px-6 py-4">ID</th>
                    <th className="px-6 py-4">CHAVE DE ACESSO</th>
                    <th className="px-6 py-4">STATUS</th>
                    <th className="px-6 py-4">USOS RESTANTES / MÁXIMO</th>
                    <th className="px-6 py-4">CRIADA EM</th>
                    <th className="px-6 py-4 text-right">AÇÕES</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/60">
                  {loading ? (
                    // Skeleton loader
                    Array.from({ length: 3 }).map((_, i) => (
                      <tr key={i} className="animate-pulse">
                        <td className="px-6 py-5"><div className="h-4 w-6 bg-slate-900 rounded"></div></td>
                        <td className="px-6 py-5"><div className="h-4 w-20 bg-slate-900 rounded"></div></td>
                        <td className="px-6 py-5"><div className="h-5 w-16 bg-slate-900 rounded-full"></div></td>
                        <td className="px-6 py-5">
                          <div className="space-y-2">
                            <div className="h-3 w-32 bg-slate-900 rounded"></div>
                            <div className="h-1.5 w-full bg-slate-900 rounded-full"></div>
                          </div>
                        </td>
                        <td className="px-6 py-5"><div className="h-4 w-28 bg-slate-900 rounded"></div></td>
                        <td className="px-6 py-5 text-right"><div className="h-8 w-24 bg-slate-900 rounded-lg ml-auto"></div></td>
                      </tr>
                    ))
                  ) : filteredKeys.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-6 py-12 text-center">
                        <span className="text-slate-500 text-sm">Nenhuma chave encontrada.</span>
                      </td>
                    </tr>
                  ) : (
                    filteredKeys.map((k) => {
                      const percentage = (k.current_uses / k.max_uses) * 100;
                      const isFull = k.current_uses >= k.max_uses;
                      
                      // Progress bar colors
                      let progressColor = "bg-sky-500";
                      if (isFull) {
                        progressColor = "bg-rose-500";
                      } else if (percentage >= 80) {
                        progressColor = "bg-amber-500";
                      } else if (percentage > 0) {
                        progressColor = "bg-emerald-500";
                      }

                      const maskedKey = showSensitive ? k.key_hash : "•••" + k.key_hash.slice(-3);

                      return (
                        <tr 
                          key={k.id} 
                          className="hover:bg-slate-900/10 transition-colors group"
                        >
                          <td className="px-6 py-4 font-mono text-xs text-slate-500">
                            #{k.id}
                          </td>
                          <td className="px-6 py-4">
                            <span className="font-mono font-bold tracking-widest text-slate-200 bg-slate-950/80 px-2.5 py-1.5 rounded-lg border border-slate-900 text-sm">
                              {maskedKey}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <button
                              onClick={() => handleToggle(k.id)}
                              className={`relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
                                k.is_active ? "bg-sky-500" : "bg-slate-800"
                              }`}
                              title={k.is_active ? "Clique para desativar" : "Clique para ativar"}
                            >
                              <span
                                className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                                  k.is_active ? "translate-x-4" : "translate-x-0"
                                }`}
                              />
                            </button>
                          </td>
                          <td className="px-6 py-4">
                            <div className="w-full max-w-[180px] space-y-1">
                              <div className="flex justify-between text-xs font-mono">
                                <span className={isFull ? "text-rose-400 font-bold" : "text-slate-300"}>
                                  {k.current_uses} / {k.max_uses}
                                </span>
                                <span className="text-slate-500">
                                  {isFull ? "Esgotado" : `${k.max_uses - k.current_uses} rest.`}
                                </span>
                              </div>
                              <div className="w-full h-1.5 bg-slate-950 rounded-full overflow-hidden border border-slate-900/80">
                                <div 
                                  className={`h-full rounded-full transition-all duration-300 ${progressColor}`}
                                  style={{ width: `${Math.min(percentage, 100)}%` }}
                                ></div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 text-xs font-mono text-slate-400">
                            {k.created_at ? new Date(k.created_at).toLocaleString("pt-BR", {
                              day: "2-digit",
                              month: "2-digit",
                              year: "numeric",
                              hour: "2-digit",
                              minute: "2-digit"
                            }) : "-"}
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex items-center justify-end gap-2 opacity-80 group-hover:opacity-100 transition-opacity">
                              <button
                                onClick={() => handleCopy(k.key_hash, k.id)}
                                className="p-2 text-slate-400 hover:text-white bg-slate-950/40 border border-slate-900 hover:border-slate-800 rounded-lg text-xs font-medium inline-flex items-center gap-1 transition-all"
                                title="Copiar Chave"
                              >
                                {copiedKeyId === k.id ? (
                                  <>
                                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                                    <span className="text-emerald-400">Copiada</span>
                                  </>
                                ) : (
                                  <>
                                    <Copy className="w-3.5 h-3.5" />
                                    <span>Copiar</span>
                                  </>
                                )}
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          )}

          {/* Table Footer / Info */}
          <div className="p-4 border-t border-slate-900/60 bg-slate-950/10 text-[10px] font-mono text-slate-500 flex justify-between items-center">
            <span>LexGrid Key Enforcement System v1.0.0</span>
            <span>Estritamente Confidencial</span>
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 mt-12 bg-slate-950/40 text-center text-xs text-slate-500">
        <p>&copy; {new Date().getFullYear()} LexGrid Intelligence. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}
