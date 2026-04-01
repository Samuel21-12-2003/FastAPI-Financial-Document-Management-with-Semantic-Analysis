import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

export default function DashboardLayout() {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content" style={{ position: 'relative' }}>
        <Outlet />
      </div>
    </div>
  );
}
