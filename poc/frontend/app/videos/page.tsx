import React, { useEffect, useState } from 'react';
import { fetchWithAuth } from '@/lib/utils';

interface Video {
  id: string;
  title: string;
  url: string;
  thumbnail_url?: string;
  description: string;
}

export default function VideosPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchVideos() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetchWithAuth(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/videos`);
        if (res.status === 401) {
          setError('Sesión expirada. Por favor, inicia sesión nuevamente.');
          setVideos([]);
          return;
        }
        if (!res.ok) throw new Error('Error al cargar los videos');
        const data = await res.json();
        setVideos(data);
      } catch (e: any) {
        setError(e.message || 'Error desconocido');
        setVideos([]);
      } finally {
        setLoading(false);
      }
    }
    fetchVideos();
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">Videos almacenados</h1>
      <p className="mb-8 text-lg text-gray-700">Aquí puedes ver todos los videos almacenados en el sistema. Selecciona un video para reproducirlo y ver su información.</p>
      {loading && <div className="text-gray-500">Cargando videos...</div>}
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {videos.map((video) => (
          <div key={video.id} className="bg-white rounded-lg shadow p-4 flex flex-col items-center">
            {video.thumbnail_url ? (
              <img src={video.thumbnail_url} alt={video.title} className="w-full h-40 object-cover rounded mb-2" />
            ) : (
              <div className="w-full h-40 bg-gray-200 flex items-center justify-center rounded mb-2 text-gray-400">Sin miniatura</div>
            )}
            <h2 className="text-lg font-semibold mb-1">{video.title}</h2>
            <p className="text-gray-600 text-sm mb-2">{video.description}</p>
            <a href={video.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline mt-auto">Ver video</a>
          </div>
        ))}
      </div>
      {!loading && !error && videos.length === 0 && (
        <div className="bg-gray-50 rounded-lg p-4 text-gray-500 mt-8">No hay videos disponibles.</div>
      )}
    </main>
  );
} 