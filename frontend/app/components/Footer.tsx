'use client';

import React from 'react';
import Link from 'next/link';
import { FiGithub, FiTwitter, FiMail } from 'react-icons/fi';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12 px-4 mt-20">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Company */}
          <div>
            <h3 className="text-xl font-bold mb-4">Fuel API</h3>
            <p className="text-gray-400">
              Отслеживай цены на топливо в реальном времени
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="font-bold mb-4">Продукт</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/#" className="hover:text-white">API</Link></li>
              <li><Link href="/#" className="hover:text-white">Pricing</Link></li>
              <li><Link href="/#" className="hover:text-white">Документация</Link></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-bold mb-4">Ресурсы</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/#" className="hover:text-white">Blog</Link></li>
              <li><Link href="/#" className="hover:text-white">Статус</Link></li>
              <li><Link href="/#" className="hover:text-white">Support</Link></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-bold mb-4">Юридичні</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/#" className="hover:text-white">Privacy</Link></li>
              <li><Link href="/#" className="hover:text-white">Terms</Link></li>
              <li><Link href="/#" className="hover:text-white">Contact</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 flex justify-between items-center flex-col md:flex-row gap-4">
          <p className="text-gray-400">
            &copy; 2024 Fuel API. All rights reserved.
          </p>
          
          <div className="flex gap-4 text-gray-400">
            <a href="#" className="hover:text-white text-xl">
              <FiGithub />
            </a>
            <a href="#" className="hover:text-white text-xl">
              <FiTwitter />
            </a>
            <a href="#" className="hover:text-white text-xl">
              <FiMail />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
