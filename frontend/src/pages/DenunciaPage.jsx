import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import { denunciaService } from '../services/api';

function ReportPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    categoria: '',
    descripcion: '',
    fechaHora: '',
    lugar: '',
    involucrados: '',
  });

  const [archivoPrueba, setArchivoPrueba] = useState(null);
  const [mensaje, setMensaje] = useState('');
  const [tipoMensaje, setTipoMensaje] = useState('');
  const [errores, setErrores] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const mostrarMensajeBackend = (texto, tipo = 'success') => {
    setMensaje(texto);
    setTipoMensaje(tipo);
    setTimeout(() => setMensaje(''), 5000);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    // Limpiar error cuando el usuario comienza a escribir
    if (errores[name]) {
      setErrores({ ...errores, [name]: '' });
    }
  };

  const handleFileChange = (e) => {
    setArchivoPrueba(e.target.files[0]);
  };

  const validarCampos = () => {
    const nuevosErrores = {};
    
    if (!formData.categoria) {
      nuevosErrores.categoria = 'La categoría es obligatoria';
    }
    if (!formData.descripcion) {
      nuevosErrores.descripcion = 'La descripción es obligatoria';
    }
    if (!formData.lugar) {
      nuevosErrores.lugar = 'El lugar es obligatorio';
    }
    
    return nuevosErrores;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const erroresValidacion = validarCampos();
    
    if (Object.keys(erroresValidacion).length > 0) {
      setErrores(erroresValidacion);
      setIsSubmitting(false);
      
      // Desplazamiento al primer error
      const primerError = Object.keys(erroresValidacion)[0];
      document.querySelector(`[name="${primerError}"]`)?.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
      return;
    }

    const datos = new FormData();
    Object.entries(formData).forEach(([key, value]) => datos.append(key, value));
    if (archivoPrueba) datos.append('pruebas', archivoPrueba);

    try {
      const result = await denunciaService.crearDenuncia(datos);

      if (result.success) {
        mostrarMensajeBackend('Denuncia registrada exitosamente ✅', 'success');
        setFormData({
          categoria: '',
          descripcion: '',
          fechaHora: '',
          lugar: '',
          involucrados: '',
        });
        setArchivoPrueba(null);
        setErrores({});
        e.target.reset();
      } else {
        mostrarMensajeBackend(result.message || 'Error al registrar la denuncia ❌', 'error');
      }
    } catch (error) {
      mostrarMensajeBackend('Error en la conexión con el servidor', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f7f9fb] relative">
      <Header />

      <main className="max-w-xl mx-auto mt-10 px-6">
        <button
          onClick={() => navigate('/')}
          className="absolute mb-6 left-20 bg-gray-200 text-blue-700 font-medium px-4 py-2 rounded hover:bg-gray-300 transition z-10"
        >
          ← Regresar al inicio
        </button>

        <h2 className="text-2xl font-bold text-center text-blue-700 mb-6">
          Formulario de Denuncia
        </h2>

        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded-xl shadow space-y-4 relative"
          encType="multipart/form-data"
        >
          {/* Notificación solo para respuestas del backend */}
          {mensaje && (
            <div 
              className={`fixed top-20 left-1/2 transform -translate-x-1/2 w-full max-w-md p-4 rounded-lg shadow-lg z-50 ${
                tipoMensaje === 'success' 
                  ? 'bg-green-100 border border-green-400 text-green-700' 
                  : 'bg-red-100 border border-red-400 text-red-700'
              }`}
              role="alert"
            >
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  {tipoMensaje === 'success' ? (
                    <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                  ) : (
                    <svg className="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                    </svg>
                  )}
                </div>
                <div className="ml-3">
                  <p className="font-medium">{mensaje}</p>
                </div>
                <button
                  type="button"
                  className="ml-auto -mx-1.5 -my-1.5 rounded-lg p-1.5 inline-flex h-8 w-8 hover:bg-green-200 focus:ring-2 focus:ring-green-400"
                  onClick={() => setMensaje('')}
                  aria-label="Cerrar"
                >
                  <span className="sr-only">Cerrar</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"/>
                  </svg>
                </button>
              </div>
            </div>
          )}

          <div className="pt-6">
            <label className="block font-medium mb-1">Categoría</label>
            <select
              name="categoria"
              value={formData.categoria}
              onChange={handleChange}
              className={`w-full border rounded-lg p-2 ${
                errores.categoria ? 'border-red-500 bg-red-50' : 'border-gray-300'
              }`}
            >
              <option value="">Selecciona una categoría</option>
              <option value="bullying">Bullying o acoso escolar</option>
              <option value="acoso_verbal">Acoso verbal</option>
              <option value="acoso_fisico">Acoso físico</option>
              <option value="violencia_psicologica">Violencia psicológica</option>
              <option value="discriminacion">Discriminación</option>
              <option value="violencia_genero">Violencia de género</option>
              <option value="ciberacoso">Ciberacoso</option>
              <option value="otro">Otro</option>
            </select>
            {errores.categoria && (
              <p className="mt-1 text-sm text-red-600">{errores.categoria}</p>
            )}
          </div>

          <div>
            <label className="block font-medium mb-1">Descripción</label>
            <textarea
              name="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
              rows="4"
              className={`w-full border rounded-lg p-2 ${
                errores.descripcion ? 'border-red-500 bg-red-50' : 'border-gray-300'
              }`}
              placeholder="Describe lo sucedido..."
            />
            {errores.descripcion && (
              <p className="mt-1 text-sm text-red-600">{errores.descripcion}</p>
            )}
          </div>

          <div>
            <label className="block font-medium mb-1">Fecha y Hora (opcional)</label>
            <input
              type="datetime-local"
              name="fechaHora"
              value={formData.fechaHora}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg p-2"
            />
          </div>

          <div>
            <label className="block font-medium mb-1">Lugar</label>
            <input
              type="text"
              name="lugar"
              value={formData.lugar}
              onChange={handleChange}
              className={`w-full border rounded-lg p-2 ${
                errores.lugar ? 'border-red-500 bg-red-50' : 'border-gray-300'
              }`}
              placeholder="Ej. Pasillo B, Biblioteca"
            />
            {errores.lugar && (
              <p className="mt-1 text-sm text-red-600">{errores.lugar}</p>
            )}
          </div>

          <div>
            <label className="block font-medium mb-1">Involucrados (opcional)</label>
            <input
              type="text"
              name="involucrados"
              value={formData.involucrados}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg p-2"
              placeholder="Nombres, cargos, etc."
            />
          </div>

          <div>
            <label className="block font-medium mb-1">Pruebas (opcional)</label>
            <input
              type="file"
              onChange={handleFileChange}
              className="w-full border border-gray-300 rounded-lg p-2"
              accept="image/*,.pdf,.doc,.docx"
            />
            {archivoPrueba && (
              <p className="text-sm text-gray-600 mt-1">
                Archivo seleccionado: {archivoPrueba.name}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
              isSubmitting ? 'opacity-70 cursor-not-allowed' : ''
            }`}
          >
            {isSubmitting ? 'Enviando...' : 'Enviar Denuncia'}
          </button>
        </form>
      </main>
    </div>
  );
}

export default ReportPage;