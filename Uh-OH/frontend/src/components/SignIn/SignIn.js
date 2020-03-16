import React from "react"
import { Link } from "react-router-dom";
import "./SignIn.css";


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
        var url = 'http://localhost:8000/login/loginuser/';
        const form = new FormData()
        form.set('username', this.state.userName)
        form.set('password', this.state.password)
        const res = fetch(url, {
            method: 'POST',
            body: form,
        })

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