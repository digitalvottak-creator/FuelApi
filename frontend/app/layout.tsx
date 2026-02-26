'use client';

import '../global.css';
import React, { ReactNode } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="uk">
      <body className="bg-gray-50">
        <Navbar />
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
