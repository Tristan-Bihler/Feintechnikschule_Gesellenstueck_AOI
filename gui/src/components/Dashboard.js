import React, { useState} from "react";
import {Button} from "react-bootstrap"
import { useAuth } from "../contexts/AuthContext";
import {useNavigate} from "react-router-dom"

export default function Dashboard(){
    const [error, setError] = useState("")
    const {currentUser, logout} = useAuth()
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
    return(
        <div>
            <p>hello </p>
            <strong>Email: </strong> {currentUser.email}
            <Button variant = "link" onClick = {handlingLogout}> Ausloggen</Button>
        </div>
    )
}