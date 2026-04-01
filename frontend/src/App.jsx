import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './pages/Login';
import DashboardLayout from './pages/DashboardLayout';
import Documents from './pages/Documents';
import Search from './pages/Search';

function App() {
  const { token } = useAuth();
  
  return (
    <Routes>
      <Route path="/login" element={!token ? <Login /> : <Navigate to="/dashboard" />} />
      <Route path="/dashboard" element={token ? <DashboardLayout /> : <Navigate to="/login" />}>
        <Route index element={<Navigate to="/dashboard/documents" />} />
        <Route path="documents" element={<Documents />} />
        <Route path="search" element={<Search />} />
      </Route>
      <Route path="*" element={<Navigate to={token ? "/dashboard/documents" : "/login"} />} />
    </Routes>
  );
}

export default App;
