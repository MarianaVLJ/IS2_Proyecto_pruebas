import { Routes, Route } from "react-router-dom";
import HomePage from '../pages/HomePage';
import DenunciaPage from "../pages/DenunciaPage";

export default function AuthRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/denuncia" element={<DenunciaPage />} />
    </Routes>
  );
} 