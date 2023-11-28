import React from 'react';
import { Navigate, Outlet, redirect } from 'react-router-dom';
import { useAuth } from "../contexts/AuthContext";

export default function Dashboard(){
    const auth = useAuth; 
    if (!auth) {
        return redirect("/login");
      }
    
      else if (auth === true) {
        return redirect("/dashboard");
      }
}