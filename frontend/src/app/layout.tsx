import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = { title: "Orchestra / Enterprise Intelligence", description: "Multi-agent pricing orchestration console" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
