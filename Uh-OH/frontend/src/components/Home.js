import React from "react";
import Schedule from "./Schedule";

class Home extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state =
		{
			officeHours: ["Search For Office Hours To Display Here..."]
		}
	}

	async componentDidMount()
	{
        // Retrieve login token
        var user = localStorage.getItem("loggedinuser");

		// GET request to get the schedule data.
        let schedule = null;
        let url = "http://localhost:8000/schedules/get/";
        let xhr = new XMLHttpRequest();

        // get a callback when the server responds
	    xhr.addEventListener("load", () => {
	        // update the state of the component with the result here
	        schedule = xhr.responseText;
	        if(schedule !== "")
	        {
	        	// formatting the string given in by the post request
	        	let finalOfficeHours = [];
	        	let arr = schedule.split(",");
	        	for(let i = 1; i < arr.length; i++)
		        {
		        	let strs = arr[i].split(" + ");
		        	let str = strs[0] + ": " + strs[1] + " " + strs[2] + " (" + strs[3] + " - " + strs[4] + ")";
			        finalOfficeHours.push(str)
		        }
	        	this.setState({officeHours: finalOfficeHours});
	        }
	    });

        xhr.open("POST", url);
        const form = new FormData();

        // Send along login token
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