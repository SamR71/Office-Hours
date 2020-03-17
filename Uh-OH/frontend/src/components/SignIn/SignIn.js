import React from "react"
import { Link } from "react-router-dom";
import "./SignIn.css";
import {useHistory} from "react-router-dom";
import { Redirect } from 'react-router';

class SignIn extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            userName: "",
            password: "",
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleClick(event)
    {
        event.preventDefault();
        var url = 'http://localhost:8000/login/loginuser/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.responseText);
                if (xhr.responseText == "User logged in!") {
                    window.location.href = "/"
                }
            }
        }
        xhr.open('POST', url)
        const form = new FormData()
        form.set('username', this.state.userName)
        form.set('password', this.state.password)
        xhr.send(form)
    }



    handleChange(event)
    {
        const input = event.target.name;
        const value = event.target.value;
        this.setState({ [input]: value })
    }

    render() {
        return(
            <div className="signin">
                <form>
                    <label htmlFor="userName"><b>Username/E-mail: </b></label>
                    <input type="text" onChange={this.handleChange} placeholder="Enter Username" name="userName" required />
                    <br/>
                    <label htmlFor="password"><b>Password: </b></label>
                    <input type="password" onChange={this.handleChange} placeholder="Enter password" name="password" required />
                    <br/>
                    <Link to="/LogIn/ResetPassword">Forgot Password</Link>
                    <br/>
                    <Link to="/LogIn/CreateAccount">Don't have an account Sign-up</Link>
                    <br/>
                    <button className="signinbutton" onClick={this.handleClick}>Log-in</button>
                </form>
            </div>
        )
    }
}

export default SignIn