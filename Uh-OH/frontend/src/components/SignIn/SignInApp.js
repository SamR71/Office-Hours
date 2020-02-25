import React from "react";
import { Switch, Route} from "react-router-dom";
import SignIn from "./SignIn";
import SignUp from "./SignUp";
import ForgotPassword from "./ForgotPassword";

class SignInApp extends React.Component{

    render() {
        return(
            <Switch>
                <Route exact path="/LogIn" component={SignIn}/>
                <Route path="/LogIn/CreateAccount" component={SignUp}/>
                <Route path="/LogIn/ResetPassword" component={ForgotPassword}/>
            </Switch>
        )
    }
}

export default SignInApp