async function handlingLogout(){
    const [error, setError] = useState("")
    const {auth, currentUser, logout} = useAuth()
    const navigate = useNavigate()
    setError("")
    try{
        navigate("/login")
        logout()
    }
    catch{
        setError("Failed to Log out")
    }
  }