import React, {useEffect} from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignUpPage';
import HomePage from './pages/HomePage';
import VerifyOtp from "./pages/VerifyOtp";
import ExpensesPage from "./pages/ExpensesPage";
import AdminDashboard from "./pages/AdminDashBoard";



function App() {

  return (

    <Router>
      <Routes>
          <Route path="/home/" element={<HomePage />} />
          <Route path="/login/" element={<LoginPage />} />
          <Route path="/" element={<LoginPage />} />
          <Route path="/signup/" element={<SignupPage />} />
          <Route path="/verifyotp/" element={<VerifyOtp />} />
          <Route path="*" element={<div>404 Not Found</div>} />
          <Route path="/expenses/" element={<ExpensesPage/>} />
          <Route path="/admin-dashboard/" element={<AdminDashboard />} />

      </Routes>
    </Router>


  );
}

export default App;
