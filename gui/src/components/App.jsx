import { AuthProvider } from "../contexts/AuthContext";
import Signup from "./Signup"
import React from "react";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
import Dashboard from "./Dashboard";
import Login from "./Login";
import Files from "./Files"
import PrivateRoute from "./PrivateRoute";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Switch>
          <Route exact path='/' element={<Dashboard/>}/>
          <Route path = "/signup" element = {<Signup />} />
          <Route path = "/login" element = {<Login />} />
          <Route path = "/files" element = {<Files />} />
        </Switch>
      </AuthProvider>
    </Router>
    
  )
}

export default App;
