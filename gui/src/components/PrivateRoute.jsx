import { Redirect, Outlet } from 'react-router-dom';
import { useAuth } from "../contexts/AuthContext";

export default function Dashboard(){
    const auth = useAuth; 
    if (!auth) {
        return Redirect("/login");
      }
    
      else if (auth === true) {
        return Redirect("/dashboard");
      }
}