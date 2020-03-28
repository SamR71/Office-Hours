import React from "react"
import "./SignIn.css"

class SignUp extends React.Component{

    constructor(props)
    {
        super(props);
        this.state =
        {
            fullName: "",
            email: "",
            password: "",
            repeatPassword: ""
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleClick(event)
    {
        event.preventDefault();
        var url = 'http://localhost:8000/login/registeruser/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.responseText);
                if (xhr.responseText == "Registration Successful!") {
                    window.location.href = "/LogIn"
                }
            }
        }
        xhr.open('POST', url)
        const form = new FormData()
        form.set('fullName', this.state.fullName)
        form.set('email', this.state.email)
        form.set('password', this.state.password)
        form.set('repeatPassword', this.state.repeatPassword)
        xhr.send(form)
        
   
    }

    handleChange(event)
    {
        const input = event.target.name;
        const value = event.target.value;
        this.setState({ [input]: value })
    }

    render(){
        return(
			<div class="container">
				<div class="row">
					<div class="col-md-5 mx-auto">
						<div class="myform form">
							<div class="logo mb-3">
								<div class="col-md-12 text-center">
									<h1 >Signup</h1>
								</div>
							</div>
							<form action="#" name="registration">
								<div class="form-group">
									<label for="exampleInputEmail1">Name</label>
									<input type="text"  name="fullName" class="form-control" id="fullName" aria-describedby="emailHelp" placeholder="FullName" onChange={this.handleChange} />
								</div>
								<div class="form-group">
									<label for="exampleInputEmail1">Email</label>
									<input type="email"  name="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter Lastname" onChange={this.handleChange} />
								</div>
								<div class="form-group">
									<label for="exampleInputEmail1">Password</label>
									<input type="password" name="password"  class="form-control" id="password" aria-describedby="emailHelp" placeholder="Enter email" onChange={this.handleChange}/>
								</div>
								<div class="form-group">
									<label for="exampleInputEmail1">Confirm Password</label>
									<input type="password" name="repeatPassword" id="repeatPassword"  class="form-control" aria-describedby="emailHelp" placeholder="Enter Password" onChange={this.handleChange}/>
								</div>
								<div class="col-md-12 text-center mb-3">
									<button  onClick={this.handleClick} class=" btn btn-block mybtn btn-primary tx-tfm">Join Uh-OH!</button>
								</div>
								<div class="col-md-12 ">
									<div class="form-group">
										<p class="text-center"><a href="/LogIn/" id="signin">Already have an account?</a></p>
									</div>
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
        )
    }
}

export default SignUp