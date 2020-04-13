import React from "react";
import Schedule from "./Schedule";

/*
The Home React Component = Main Uh-OH! Homepage Containing The User Schedule.
*/
class Home extends React.Component
{
    //State Stores All User Office Hours.
    //Displays "Hello! Login + Search For Office Hours To Display Here"
    //In Case User Is Not Logged In.
	constructor(props)
	{
		super(props);
		this.state =
		{
			officeHours: ["Hello! Login + Search For Office Hours To Display Here..."]
		}
	}

    //Main Mounting For Homepage Component:
	async componentDidMount()
	{
        //Retrive Login Token = Whether User Is Logged In.
        var user = localStorage.getItem("loggedinuser");

		//Sends GET Request To Backend To Receive Schedule Data.
        let schedule = null;
        let url = "http://localhost:8000/schedules/get/";
        let xhr = new XMLHttpRequest();

        //Receives Callback When localhost:8000 Backend Server Responds...
	    xhr.addEventListener("load", () => {
	        //Updates the State of the Component with the result here.
	        schedule = xhr.responseText;
	        if(schedule !== "")
	        {
	        	//Special Formatting of the returned string supplied by the POST Request from Backend.
	        	let finalOfficeHours = [];
                //Office Hours Are Spilt By Commas...
	        	let arr = schedule.split(",");
	        	for(let i = 1; i < arr.length; i++)
		        {
		        	let strs = arr[i].split(" + ");
		        	let str = strs[0] + ": " + strs[1] + " " + strs[2] + " (" + strs[3] + " - " + strs[4] + ")";
			        finalOfficeHours.push(str)
		        }
                //Updates State Accordingly = Final Office Hours Received From Backend.
	        	this.setState({officeHours: finalOfficeHours});
	        }
	    });

        xhr.open("POST", url);
        const form = new FormData();
        //Sends Along Login Username Token To Backend To Query For Specific User Schedule Data.
        form.set("user",user);
        xhr.send(form);
	}

    render()
    {
    	const homePageStyle =
        {
            margin: "20px"
        };

        return(
            <div style={homePageStyle} class="container-fluid">
                <div class="row justify-content-center">
                    <div class="col-xl-9 mr-5">
                        <h2>My Schedule:</h2>
                        <Schedule />
                        <br></br>
                        <h2>Office Hours:</h2>
                        <p>{this.state.officeHours.map(item => <ul>{item}</ul>)}</p>
                    </div>
                </div>
            </div>
        );
    }
}

export default Home;