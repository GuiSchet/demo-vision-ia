import React from 'react';
import Link from 'next/link';

export default function DashboardPage() {
  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">Panel de Control</h1>
      <p className="mb-8 text-lg text-gray-700">Bienvenido al sistema de monitoreo inteligente. Aquí puedes ver un resumen de la actividad reciente, videos almacenados y alertas detectadas.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-2">Videos</h2>
          <p className="text-gray-600 mb-4">Resumen de videos almacenados y recientes.</p>
          <Link href="/videos" className="text-blue-600 hover:underline">Ver videos</Link>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-2">Alertas</h2>
          <p className="text-gray-600 mb-4">Últimas alertas generadas por el sistema.</p>
          <Link href="/alertas" className="text-blue-600 hover:underline">Ver alertas</Link>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-2">Chatbot</h2>
          <p className="text-gray-600 mb-4">Consulta al agente inteligente sobre los videos y alertas.</p>
          <Link href="/chat" className="text-blue-600 hover:underline">Ir al Chatbot</Link>
        </div>
      </div>
      <section className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Actividad Reciente</h2>
        {/* Aquí se mostrarán los datos recientes de Qdrant (videos, alertas, etc.) */}
        <div className="bg-gray-50 rounded-lg p-4 text-gray-500">
          Próximamente: resumen de actividad reciente extraída de Qdrant.
        </div>
      </section>
    </main>
  );
} 