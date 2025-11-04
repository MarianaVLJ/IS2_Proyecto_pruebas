import { useEffect, useState } from 'react';
import Header from '../components/Header';
import AuthModal from '../components/AuthModal'


function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [mostrarModal, setMostrarModal] = useState(false);

  const posts = [
    { id: 1, content: 'Hoy me siento triste 😞' },
    { id: 2, content: 'Recuerda que eres fuerte 💪' },
    { id: 3, content: '¿Alguien necesita hablar?' },
  ];

  useEffect(() => {
    async function verificarSesion() {
      const resultado = await new Promise((res) =>
        setTimeout(() => res({ isLoggedIn: false }), 1000)
      );
      setIsLoggedIn(resultado.isLoggedIn);
    }

    verificarSesion();
  }, []);

  return (
    <div className="min-h-screen bg-[#e9f6ff]">
      <Header isLoggedIn={isLoggedIn} onLoginClick={() => setMostrarModal(true)} />

      <main className="max-w-2xl mx-auto mt-10 space-y-6 px-4">
        {posts.map((post) => (
          <div
            key={post.id}
            className="bg-white p-4 rounded-xl shadow-md border border-gray-200 hover:shadow-lg transition"
          >
            <p className="text-gray-700 text-lg">{post.content}</p>
          </div>
        ))}
      </main>

      {/* Modal de iniciar sesión */}
      <AuthModal
        mostrarModal={mostrarModal}
        setMostrarModal={setMostrarModal}
        setIsLoggedIn={setIsLoggedIn}
      />
    </div>
  );
}

export default HomePage;
