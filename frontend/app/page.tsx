'use client';

import React from 'react';
import Link from 'next/link';
import { FiZap, FiMap, FiTrendingDown } from 'react-icons/fi';

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">Fuel Price API</h1>
          <p className="text-xl mb-8">
            Отслеживай цены на топливо (OKKO, WOG, SOCAR) в реальном времени
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/auth/register" className="bg-white text-blue-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-100">
              Початися
            </Link>
            <Link href="/auth/login" className="border-2 border-white text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700">
              Вхід
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Можливості</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition">
              <FiZap className="text-blue-600 text-4xl mb-4" />
              <h3 className="text-xl font-bold mb-2">Дані в реальному часі</h3>
              <p className="text-gray-600">
                Отримуй актуальні ціни на паливо оновлені кожну годину
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition">
              <FiMap className="text-blue-600 text-4xl mb-4" />
              <h3 className="text-xl font-bold mb-2">Геолокація</h3>
              <p className="text-gray-600">
                Знайди найближчу АЗС з найкращою ціною на топливо
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition">
              <FiTrendingDown className="text-blue-600 text-4xl mb-4" />
              <h3 className="text-xl font-bold mb-2">Аналітика</h3>
              <p className="text-gray-600">
                Відслідковуй тренди цін та приймай вдалі рішення
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-gray-100 py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Плани підписки</h2>
          
          <div className="grid md:grid-cols-5 gap-6">
            {/* Starter */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-bold mb-2">Starter</h3>
              <p className="text-3xl font-bold text-blue-600 mb-4">₴99</p>
              <p className="text-sm text-gray-600 mb-4">/місяць</p>
              <ul className="text-sm text-gray-600 mb-6 space-y-2">
                <li>✓ 5,000 запросів</li>
                <li>✓ Основний API</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                Обрати
              </button>
            </div>

            {/* Professional */}
            <div className="bg-white p-6 rounded-lg shadow-md border-2 border-blue-600">
              <div className="bg-blue-600 text-white px-2 py-1 rounded text-xs font-bold w-fit mb-2">
                ПОПУЛЯРНИЙ
              </div>
              <h3 className="text-xl font-bold mb-2">Professional</h3>
              <p className="text-3xl font-bold text-blue-600 mb-4">₴299</p>
              <p className="text-sm text-gray-600 mb-4">/місяць</p>
              <ul className="text-sm text-gray-600 mb-6 space-y-2">
                <li>✓ 20,000 запросів</li>
                <li>✓ API v1+v2</li>
                <li>✓ Вебхуки</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                Обрати
              </button>
            </div>

            {/* Business */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-bold mb-2">Business</h3>
              <p className="text-3xl font-bold text-blue-600 mb-4">₴699</p>
              <p className="text-sm text-gray-600 mb-4">/місяць</p>
              <ul className="text-sm text-gray-600 mb-6 space-y-2">
                <li>✓ 50,000 запросів</li>
                <li>✓ Advanced API</li>
                <li>✓ Аналітика</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                Обрати
              </button>
            </div>

            {/* Enterprise */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-bold mb-2">Enterprise</h3>
              <p className="text-3xl font-bold text-blue-600 mb-4">₴1,299</p>
              <p className="text-sm text-gray-600 mb-4">/місяць</p>
              <ul className="text-sm text-gray-600 mb-6 space-y-2">
                <li>✓ 100,000 запросів</li>
                <li>✓ Full API</li>
                <li>✓ 24/7 Поддержка</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                Обрати
              </button>
            </div>

            {/* Ultra */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-bold mb-2">Ultra</h3>
              <p className="text-3xl font-bold text-blue-600 mb-4">₴4,999</p>
              <p className="text-sm text-gray-600 mb-4">/місяць</p>
              <ul className="text-sm text-gray-600 mb-6 space-y-2">
                <li>✓ 1,000,000 запросів</li>
                <li>✓ All Features</li>
                <li>✓ Account Manager</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                Обрати
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
