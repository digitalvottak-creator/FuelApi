'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { FiMenu, FiX, FiLogOut } from 'react-icons/fi';

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [mounted, setMounted] = useState(false);

  // Проверка аутентификации только на client side
  useEffect(() => {
    setMounted(true);
    const token = typeof window !== 'undefined' && localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    router.push('/');
  };

  // Не рендерить conditional content пока не смонтировано
  if (!mounted) {
    return (
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            Fuel API
          </Link>
        </div>
      </nav>
    );
  }

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-blue-600">
          Fuel API
        </Link>

        {/* Desktop Menu */}
        <div className="hidden md:flex gap-8 items-center">
          <Link 
            href="/#" 
            className="text-gray-700 hover:text-blue-600"
          >
            API Документація
          </Link>
          
          {isAuthenticated ? (
            <>
              <Link 
                href="/dashboard" 
                className={`${
                  pathname === '/dashboard' 
                    ? 'text-blue-600 font-bold' 
                    : 'text-gray-700 hover:text-blue-600'
                }`}
              >
                Dashboard
              </Link>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 flex items-center gap-2"
              >
                <FiLogOut /> Вихід
              </button>
            </>
          ) : (
            <>
              <Link 
                href="/auth/login" 
                className="text-gray-700 hover:text-blue-600"
              >
                Вхід
              </Link>
              <Link 
                href="/auth/register" 
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Реєстрація
              </Link>
            </>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button 
          className="md:hidden text-2xl"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <FiX /> : <FiMenu />}
        </button>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-gray-50 p-4 space-y-4">
          <Link 
            href="/#" 
            className="block text-gray-700 hover:text-blue-600"
          >
            API Документація
          </Link>
          
          {isAuthenticated ? (
            <>
              <Link 
                href="/dashboard" 
                className="block text-gray-700 hover:text-blue-600"
              >
                Dashboard
              </Link>
              <button
                onClick={handleLogout}
                className="block w-full text-left bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              >
                Вихід
              </button>
            </>
          ) : (
            <>
              <Link 
                href="/auth/login" 
                className="block text-gray-700 hover:text-blue-600"
              >
                Вхід
              </Link>
              <Link 
                href="/auth/register" 
                className="block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-center"
              >
                Реєстрація
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}