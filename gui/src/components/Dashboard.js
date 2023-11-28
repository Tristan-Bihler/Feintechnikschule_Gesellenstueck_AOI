import React, { useState} from "react";
import {Button} from "react-bootstrap"
import { useAuth } from "../contexts/AuthContext";
import {useNavigate, redirect} from "react-router-dom"

export default function Dashboard(){
    const [error, setError] = useState("")
    const {auth, currentUser, logout} = useAuth()
    const navigate = useNavigate()



    async function handlingLogout(){
        setError("")
        try{
            navigate("/login")
            logout()
        }
        catch{
            setError("Failed to Log out")
        }
    }

    function load(){
        if (!auth) {
            return redirect("/login");
          }

        else {
            
        }

    }

    return(
        <body onload="load();">
            <p>hello </p>
            <Button variant = "link" onClick = {handlingLogout}> Ausloggen</Button>
        </body>
    )
}