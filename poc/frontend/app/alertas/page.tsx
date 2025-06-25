import React, { useEffect, useState } from 'react';
import { fetchWithAuth } from '@/lib/utils';

interface Alerta {
  id: string;
  title: string;
  description: string;
  severity: string;
  timestamp: string;
  video_url: string;
  thumbnail_url?: string;
}

export default function AlertasPage() {
  const [alertas, setAlertas] = useState<Alerta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAlertas() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetchWithAuth(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/alerts`);
        if (res.status === 401) {
          setError('Sesión expirada. Por favor, inicia sesión nuevamente.');
          setAlertas([]);
          return;
        }
        if (!res.ok) throw new Error('Error al cargar las alertas');
        const data = await res.json();
        setAlertas(data);
      } catch (e: any) {
        setError(e.message || 'Error desconocido');
        setAlertas([]);
      } finally {
        setLoading(false);
      }
    }
    fetchAlertas();
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">Alertas</h1>
      <p className="mb-8 text-lg text-gray-700">Aquí puedes ver las alertas generadas por el sistema, basadas en la metadata de Qdrant.</p>
      {loading && <div className="text-gray-500">Cargando alertas...</div>}
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {alertas.map((alerta) => (
          <div key={alerta.id} className="bg-white rounded-lg shadow p-4 flex flex-col md:flex-row gap-4 items-center">
            {alerta.thumbnail_url ? (
              <img src={alerta.thumbnail_url} alt={alerta.title} className="w-32 h-32 object-cover rounded mb-2 md:mb-0" />
            ) : (
              <div className="w-32 h-32 bg-gray-200 flex items-center justify-center rounded mb-2 md:mb-0 text-gray-400">Sin miniatura</div>
            )}
            <div className="flex-1">
              <h2 className="text-lg font-semibold mb-1">{alerta.title}</h2>
              <p className="text-gray-600 text-sm mb-1">{alerta.description}</p>
              <p className="text-xs mb-1">Severidad: <span className={`font-bold ${getSeverityColor(alerta.severity)}`}>{alerta.severity}</span></p>
              <p className="text-xs text-gray-500 mb-2">{new Date(alerta.timestamp).toLocaleString()}</p>
              <a href={alerta.video_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Ver video relacionado</a>
            </div>
          </div>
        ))}
      </div>
      {!loading && !error && alertas.length === 0 && (
        <div className="bg-gray-50 rounded-lg p-4 text-gray-500 mt-8">No hay alertas disponibles.</div>
      )}
    </main>
  );
}

function getSeverityColor(severity: string) {
  switch (severity) {
    case 'alta':
    case 'high':
      return 'text-red-600';
    case 'media':
    case 'medium':
      return 'text-yellow-600';
    case 'baja':
    case 'low':
      return 'text-green-600';
    default:
      return 'text-gray-600';
  }
} 