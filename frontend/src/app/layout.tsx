import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <main className="min-h-screen bg-lexgrid-900">{children}</main>
      </body>
    </html>
  );
}