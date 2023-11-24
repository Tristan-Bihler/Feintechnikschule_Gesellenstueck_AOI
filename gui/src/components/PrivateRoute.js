import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from "../contexts/AuthContext";

export default function Dashboard(){
    const auth = useAuth; 
    return auth ? <Outlet /> : <Navigate to="/login" />;
}