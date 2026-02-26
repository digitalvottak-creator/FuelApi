'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { FiCopy, FiTrash2, FiPlus } from 'react-icons/fi';
import axios from 'axios';

interface APIKey {
  id: number;
  key: string;
  name: string;
  is_active: boolean;
  created_at: string;
  last_used_at: string | null;
}

interface Subscription {
  id: number;
  plan: {
    name: string;
    monthly_requests: number;
    price_uah: number;
  };
  status: string;
  requests_used: number;
  started_at: string;
  expires_at: string;
}

interface Stats {
  user: {
    id: number;
    email: string;
    username: string;
    company_name: string | null;
  };
  subscription: Subscription;
  api_usage: {
    total_requests_used: number;
    total_requests_available: number;
    progress_percent: number;
    days_remaining: number;
  };
  api_keys: APIKey[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Dashboard() {
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [showNewKeyForm, setShowNewKeyForm] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      setApiKey(token);

      const response = await axios.get(`${API_URL}/account/stats`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setStats(response.data);
      setError('');
    } catch (error: any) {
      console.error('Error loading stats:', error);
      setError('Помилка завантаження статистики');
      
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        router.push('/auth/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(text);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const createNewKey = async () => {
    if (!newKeyName.trim()) return;

    try {
      const response = await axios.post(`${API_URL}/api-keys`, 
        { name: newKeyName },
        {
          headers: {
            'Authorization': `Bearer ${apiKey}`
          }
        }
      );
      
      setShowNewKeyForm(false);
      setNewKeyName('');
      loadStats();
    } catch (error) {
      console.error('Error creating key:', error);
      setError('Помилка при створенні ключа');
    }
  };

  const deleteKey = async (keyId: number) => {
    if (!confirm('Ви впевнені?')) return;

    try {
      await axios.delete(`${API_URL}/api-keys/${keyId}`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`
        }
      });
      
      loadStats();
    } catch (error) {
      console.error('Error deleting key:', error);
      setError('Помилка при видаленні ключа');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl text-gray-600">Завантаження...</div>
      </div>
    );
  }

  if (error && !stats) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl text-red-600">{error}</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl text-gray-600">Помилка завантаження</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto py-12 px-4">
      <h1 className="text-4xl font-bold mb-8">Мій аккаунт</h1>

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-8">
          {error}
        </div>
      )}

      {/* Profile Info */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-bold mb-4">Інформація профілю</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <p className="text-gray-600">Email</p>
            <p className="font-bold text-lg">{stats.user.email}</p>
          </div>
          <div>
            <p className="text-gray-600">Ім'я користувача</p>
            <p className="font-bold text-lg">{stats.user.username}</p>
          </div>
          {stats.user.company_name && (
            <div>
              <p className="text-gray-600">Компанія</p>
              <p className="font-bold text-lg">{stats.user.company_name}</p>
            </div>
          )}
        </div>
      </div>

      {/* Subscription Info */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-bold mb-4">Підписка</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <p className="text-gray-600 mb-2">План</p>
            <p className="text-3xl font-bold text-blue-600 mb-2">{stats.subscription.plan.name}</p>
            <p className="text-gray-600">₴{stats.subscription.plan.price_uah}/місяць</p>
          </div>
          <div>
            <p className="text-gray-600 mb-2">Статус</p>
            <p className="text-xl font-bold mb-2 capitalize">
              {stats.subscription.status === 'active' ? '✓ Активна' : 'Неактивна'}
            </p>
            <p className="text-gray-600">
              До:{' '}
              {new Date(stats.subscription.expires_at).toLocaleDateString('uk-UA')}
            </p>
          </div>
        </div>
      </div>

      {/* API Usage */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-bold mb-4">Використання API</h2>
        <div className="mb-4">
          <div className="flex justify-between mb-2">
            <span>Запросів цього місяця</span>
            <span className="font-bold">
              {stats.api_usage.total_requests_used} / {stats.api_usage.total_requests_available}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-blue-600 h-4 rounded-full transition-all"
              style={{ width: `${Math.min(stats.api_usage.progress_percent, 100)}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {stats.api_usage.progress_percent.toFixed(1)}% використано
          </p>
        </div>
        <p className="text-gray-600">
          Залишилося днів: {stats.api_usage.days_remaining}
        </p>
      </div>

      {/* API Keys */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">API ключі</h2>
          <button
            onClick={() => setShowNewKeyForm(!showNewKeyForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center gap-2"
          >
            <FiPlus /> Новий ключ
          </button>
        </div>

        {showNewKeyForm && (
          <div className="bg-gray-100 p-4 rounded mb-6">
            <input
              type="text"
              placeholder="Назва ключа"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              className="w-full px-4 py-2 border rounded mb-2"
            />
            <button
              onClick={createNewKey}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Створити
            </button>
          </div>
        )}

        <div className="space-y-4">
          {stats.api_keys.map((key) => (
            <div key={key.id} className="bg-gray-50 p-4 rounded border flex justify-between items-center">
              <div className="flex-1">
                <p className="font-bold">{key.name}</p>
                <p className="text-gray-600 text-sm font-mono break-all">
                  {key.key.substring(0, 10)}...{key.key.substring(key.key.length - 10)}
                </p>
                <p className="text-gray-600 text-sm">
                  Останнього використання:{' '}
                  {key.last_used_at
                    ? new Date(key.last_used_at).toLocaleDateString('uk-UA')
                    : 'Ніколи'}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => copyToClipboard(key.key)}
                  className="bg-gray-300 text-gray-700 px-3 py-2 rounded hover:bg-gray-400"
                  title="Copy"
                >
                  <FiCopy />
                </button>
                <button
                  onClick={() => deleteKey(key.id)}
                  className="bg-red-500 text-white px-3 py-2 rounded hover:bg-red-600"
                  title="Delete"
                >
                  <FiTrash2 />
                </button>
              </div>
            </div>
          ))}
        </div>

        {copiedKey && (
          <p className="text-green-600 mt-4">✓ Скопійовано!</p>
        )}
      </div>
    </div>
  );
}