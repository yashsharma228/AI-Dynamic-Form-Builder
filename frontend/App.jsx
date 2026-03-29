import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import FormBuilderPage from "./pages/FormBuilderPage";
import FormFillPage from "./pages/FormFillPage";

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>AI Dynamic Form Builder</h1>
        <nav>
          <NavLink to="/builder">Form Builder</NavLink>
          <NavLink to="/fill">Form Fill</NavLink>
          <NavLink to="/dashboard">Dashboard</NavLink>
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<Navigate to="/builder" replace />} />
          <Route path="/builder" element={<FormBuilderPage />} />
          <Route path="/fill" element={<FormFillPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
