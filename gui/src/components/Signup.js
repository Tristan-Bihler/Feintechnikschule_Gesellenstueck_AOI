import React, { useRef, useState } from "react"
import { Form, Button,Card, Alert } from "react-bootstrap"
import { useAuth } from "../contexts/AuthContext"
import {Link, useNavigate} from "react-router-dom"

export default function Signup(){

    const emailRef = useRef()
    const passwordRef = useRef()
    const passwordconfirmRef = useRef()
    const { signup } = useAuth()
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    async function handlesubmit(e){
        e.preventDefault()
        if (passwordRef.current.value !== passwordconfirmRef.current.value){
            return setError("Passwords do not match")
        }

        try {
            setError("")
            setLoading(true)
            await signup(emailRef.current.value, passwordRef.current.value)
            navigate("/");
        } catch{
            setError("Failed to create an account")
        }

        setLoading(false)
    }
    return (
        <>
            <Card>
                <Card.Body>
                    {error && <Alert cariant = "danger">{error}</Alert>}
                    <Form onSubmit = {handlesubmit}>
                    <h2 className = "text-center mb-4">Signup</h2>
                    <Form.Group id = "email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type = "email" ref ={emailRef} rquiered></Form.Control>
                        <Form.Label>Passwort</Form.Label>
                        <Form.Control type = "password" ref ={passwordRef} rquiered></Form.Control>
                        <Form.Label>Passwort Confirm</Form.Label>
                        <Form.Control type = "password" ref ={passwordconfirmRef} rquiered></Form.Control>
                    </Form.Group>
                    <Button disabled = {loading} className = "w-100" type = "submit">Sign in</Button>
                    </Form>
                </Card.Body>
            </Card>
            <div className ="w-100 text-center mt-2">
            <p>Benutzer<Link to = "/Login"> Anmelden</Link></p>
            </div>
        </>
    )
}