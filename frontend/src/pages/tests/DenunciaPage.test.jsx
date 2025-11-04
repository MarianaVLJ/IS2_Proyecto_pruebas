import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import ReportPage from '../DenunciaPage';
import { denunciaService } from '../../services/api';

// Mockea el servicio de denuncias
jest.mock('../../services/api', () => ({
  denunciaService: {
    crearDenuncia: jest.fn(),
  },
}));

// Helper para renderizar con Router
function renderWithRouter(ui) {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
}

describe('ReportPage (DenunciaPage)', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza todos los campos y el botón de envío', () => {
    renderWithRouter(<ReportPage />);
    // Solo hay un combobox (categoría)
    expect(screen.getByRole('combobox')).toBeInTheDocument();
    // Textarea descripción
    expect(screen.getByPlaceholderText(/Describe lo sucedido/i)).toBeInTheDocument();
    // Input lugar
    expect(screen.getByPlaceholderText(/Ej. Pasillo B/i)).toBeInTheDocument();
    // Botón de enviar habilitado al inicio
    expect(screen.getByRole('button', { name: /Enviar Denuncia/i })).toBeEnabled();
  });

  test('muestra errores de validación si faltan campos obligatorios', async () => {
    renderWithRouter(<ReportPage />);
    await userEvent.click(screen.getByRole('button', { name: /Enviar Denuncia/i }));

    expect(await screen.findByText('La categoría es obligatoria')).toBeInTheDocument();
    expect(screen.getByText('La descripción es obligatoria')).toBeInTheDocument();
    expect(screen.getByText('El lugar es obligatorio')).toBeInTheDocument();
  });

  test('envío exitoso muestra mensaje de éxito y resetea el formulario', async () => {
    denunciaService.crearDenuncia.mockResolvedValue({ success: true });

    renderWithRouter(<ReportPage />);
    const selectCategoria = screen.getByRole('combobox');
    const textareaDesc = screen.getByPlaceholderText(/Describe lo sucedido/i);
    const inputLugar = screen.getByPlaceholderText(/Ej. Pasillo B/i);

    // Rellenar campos obligatorios
    userEvent.selectOptions(selectCategoria, 'bullying');
    await userEvent.type(textareaDesc, 'Descripción de prueba');
    await userEvent.type(inputLugar, 'Biblioteca');

    await userEvent.click(screen.getByRole('button', { name: /Enviar Denuncia/i }));

    // Confirmar llamada al servicio
    expect(denunciaService.crearDenuncia).toHaveBeenCalledTimes(1);
    // Mensaje de éxito visible
    expect(await screen.findByRole('alert')).toHaveTextContent(/Denuncia registrada exitosamente/i);

    // Verificar reset de formulario
    expect(selectCategoria.value).toBe('');
    expect(textareaDesc.value).toBe('');
    expect(inputLugar.value).toBe('');
  });

  test('envío fallido muestra mensaje de error personalizado', async () => {
    denunciaService.crearDenuncia.mockResolvedValue({ success: false, message: 'Error personal' });

    renderWithRouter(<ReportPage />);
    const selectCategoria = screen.getByRole('combobox');
    const textareaDesc = screen.getByPlaceholderText(/Describe lo sucedido/i);
    const inputLugar = screen.getByPlaceholderText(/Ej. Pasillo B/i);

    userEvent.selectOptions(selectCategoria, 'bullying');
    await userEvent.type(textareaDesc, 'Texto');
    await userEvent.type(inputLugar, 'Lugar');

    await userEvent.click(screen.getByRole('button', { name: /Enviar Denuncia/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Error personal');
  });

  test('error de conexión muestra mensaje de error genérico', async () => {
    denunciaService.crearDenuncia.mockRejectedValue(new Error('Network failure'));

    renderWithRouter(<ReportPage />);
    const selectCategoria = screen.getByRole('combobox');
    const textareaDesc = screen.getByPlaceholderText(/Describe lo sucedido/i);
    const inputLugar = screen.getByPlaceholderText(/Ej. Pasillo B/i);

    userEvent.selectOptions(selectCategoria, 'bullying');
    await userEvent.type(textareaDesc, 'Texto');
    await userEvent.type(inputLugar, 'Lugar');

    await userEvent.click(screen.getByRole('button', { name: /Enviar Denuncia/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Error en la conexión con el servidor');
  });
});