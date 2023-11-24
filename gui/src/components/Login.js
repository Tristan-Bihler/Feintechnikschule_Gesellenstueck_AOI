import React, { useRef, useState } from "react"
import { Form, Button,Card, Alert } from "react-bootstrap"
import { useAuth } from "../contexts/AuthContext"
import {Link, useNavigate } from "react-router-dom"
export default function Login(){

    const emailRef = useRef()
    const passwordRef = useRef()
    const { login } = useAuth()
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate() 

    async function handlesubmit(e){
        e.preventDefault()

        try {
            setError("")
            setLoading(true)
            await login(emailRef.current.value, passwordRef.current.value)
            navigate("/");
        } catch{
            setError("Failed to sign in")
        }

        setLoading(false)
    }
    return (
        <>
            <Card>
                <Card.Body>
                    {error && <Alert cariant = "danger">{error}</Alert>}
                    <Form onSubmit = {handlesubmit}>
                    <h2 className = "text-center mb-4">Log in</h2>
                    <Form.Group id = "email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type = "email" ref ={emailRef} rquiered></Form.Control>
                        <Form.Label>Passwort</Form.Label>
                        <Form.Control type = "password" ref ={passwordRef} rquiered></Form.Control>
                    </Form.Group>
                    <Button disabled = {loading} className = "w-100" type = "submit">Log in</Button>
                    </Form>
                </Card.Body>
            </Card>
            <div className ="w-100 text-center mt-2">
                Neuen Benutzer <Link to = "/signup">Anmelden</Link>!
            </div>
        </>
    )
}