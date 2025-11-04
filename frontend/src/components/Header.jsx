import { useLocation, useNavigate } from 'react-router-dom';

function Header({ isLoggedIn, onLoginClick }) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <header className="bg-blue-900 text-white py-6 shadow">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-12 items-center">
          <div className="col-span-7">
            <h1 className="text-3xl font-bold">ESCÚ!</h1>
            <h6 className="text-lg mt-1">Un lugar seguro para lo que sientes.</h6>
          </div>

          <div className="col-span-5 flex justify-end items-center space-x-4">
            {location.pathname !== '/denuncia' && (
              <button
                onClick={() => navigate('/denuncia')}
                className="bg-red-600 text-white px-5 py-2 text-lg rounded-lg hover:bg-red-700 transition"
              >
                ¡Denuncia ya!
              </button>
            )}
            {isLoggedIn ? (
              <img
                src="/user-icon.png"
                alt="Usuario"
                className="rounded-full w-[45px] h-[45px]"
              />
            ) : (
              <button
                className="bg-white text-blue-900 px-5 py-2 text-lg rounded-lg hover:bg-gray-100 transition"
                onClick={onLoginClick}
              >
                Iniciar sesión
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}


export default Header;
