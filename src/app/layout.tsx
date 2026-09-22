import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import styles from "./layout.module.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Smart Urban Operations Platform",
  description: "Bandra - Borivali | Mumbai",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className={styles.appContainer}>
          <Header />
          <div className={styles.mainWrapper}>
            <Sidebar />
            <main className={styles.mainContent}>
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
