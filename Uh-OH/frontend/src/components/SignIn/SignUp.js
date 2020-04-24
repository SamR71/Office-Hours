import React from "react"
import "./SignIn.css"

/*
The SignUp React Component Serves As The Main Page
For New Users Joining Uh-OH!
The Component Will Display Fields/Data For The User To Specify
So That They Can Login After This Point On ...
*/
class SignUp extends React.Component
{

    //State Stores Key user Information To Provide Backend For Saving Data.
    constructor(props)
    {
        super(props);
        //Repeat Password Ensures That The User Has Entered Their Password The Same Twice.
        //Ensures They Are Aware Of Their Password At The Time Of Signing Up.
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

    //Click Indicates User Has Entered "Join Uh-OH!" Button.
    handleClick(event)
    {
        event.preventDefault(); 
        //Create POST Request In Backend Requesting To Register New User + Saves User Data.
        var url = 'http://localhost:8000/login/registeruser/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            //Case 1: Successful Register
            if (xhr.readyState == XMLHttpRequest.DONE) 
            {
                alert(xhr.responseText);
                if (xhr.responseText == "Registration Successful!") 
                {
                    window.location.href = "/LogIn"
                }
            }
        }
        //Supply/Send Form Data To Backend.
        xhr.open('POST', url)
        const form = new FormData()
        form.set('fullName', this.state.fullName)
        form.set('email', this.state.email)
        form.set('password', this.state.password)
        form.set('repeatPassword', this.state.repeatPassword)
        xhr.send(form)
        
    }   

    //Similar To Other Files, Function Listens For + Adjusts State Fields Based On Changes.
    handleChange(event)
    {
        const input = event.target.name;
        const value = event.target.value;
        this.setState({ [input]: value })
    }

    //Main React Displaying of Sign Up Page:
    //Contains Full Name, Email, Passsword, Repeat Password Fields
    //+ Join Uh-OH! Button ...
    render()
    {
        return(
			<div className="container">
				<div className="row">
					<div className="col-md-5 mx-auto">
						<div className="myform form">
							<div className="logo mb-3">
								<div className="col-md-12 text-center">
									<h1 >Sign Up For Uh-OH!</h1>
								</div>
							</div>
							<form action="#" name="registration">
								<div className="form-group">
									<label htmlFor="exampleInputEmail1">Name</label>
									<input type="text"  name="fullName" className="form-control" id="fullName" aria-describedby="emailHelp" placeholder="Enter Name" onChange={this.handleChange} />
								</div>
								<div className="form-group">
									<label htmlFor="exampleInputEmail1">Email</label>
									<input type="email"  name="email" className="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter Email" onChange={this.handleChange} />
								</div>
								<div className="form-group">
									<label htmlFor="exampleInputEmail1">Password</label>
									<input type="password" name="password"  className="form-control" id="password" aria-describedby="emailHelp" placeholder="Enter Password" onChange={this.handleChange}/>
								</div>
								<div className="form-group">
									<label htmlFor="exampleInputEmail1">Confirm Password</label>
									<input type="password" name="repeatPassword" id="repeatPassword"  className="form-control" aria-describedby="emailHelp" placeholder="Confirm Password" onChange={this.handleChange}/>
								</div>
								<div className="col-md-12 text-center mb-3">
									<button  onClick={this.handleClick} className=" btn btn-block mybtn btn-primary tx-tfm">Join Uh-OH!</button>
								</div>
								<div className="col-md-12 ">
									<div className="form-group">
										<p className="text-center"><a href="/LogIn/" id="signin">Already Have An Uh-OH! Account?</a></p>
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