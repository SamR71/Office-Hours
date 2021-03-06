import React from "react";
import Schedule from "./Schedule";
import EditModal from "./EditModal";

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
			officeHours: ["N/A"],
			instructorHours: ["N/A"]
		}
	}

	//Main Mounting For Homepage Component:
	async componentDidMount()
	{
		//Retrieve Login Token = Whether User Is Logged In.
		var user = localStorage.getItem("loggedinuser");

		//Sends POST Requests To Backend To Receive Schedule Data.
		let schedule = null;
		let hours = null;
		let url1 = "http://localhost:8000/schedules/get/";
		let url2 = "http://localhost:8000/hours/";
		let xhr1 = new XMLHttpRequest();
		let xhr2 = new XMLHttpRequest();
		
		//Handles All User Schedule Office Hours:
		//Receives Callback When localhost:8000 Backend Server Responds...
		xhr1.addEventListener("load", () => {
			//Updates the State of the Component with the result here.
			schedule = xhr1.responseText;
			if (schedule !== "")
			{
				//Special Formatting of the returned string supplied by the POST Request from Backend.
				let finalOfficeHours = [];
				//Office Hours Are Spilt By Commas...
				let arr = schedule.split(",");
				for (let i = 1; i < arr.length; i++)
				{
					let strs = arr[i].split(" + ");
					let courseName = strs[0]
					let courseNameTitleCase = courseName.replace(
						/(\w)(\w*)/g,
						(_, firstChar, rest) => firstChar + rest.toLowerCase()
					  );
					let str = courseNameTitleCase + ", " + strs[1] + ": " + strs[2] + " " + strs[3] + " (" + strs[4] + " - " + strs[5] + ")";
					finalOfficeHours.push(str)
				}
				//Updates State Accordingly = Final Office Hours Received From Backend.
				this.setState({officeHours: finalOfficeHours});
			}
		});
		
		//Handles Instructor Office Hours To Be Displayed Specific To Logged In User:
		xhr2.addEventListener("load", () => {
			//Updates the State of the Component with the result here.
			hours = xhr2.responseText;
			console.log(hours);
			if (hours !== "")
			{
				//Special Formatting of the returned string supplied by the POST Request from Backend.
				let finalHours = [];
				//Office Hours Are Spilt By Commas...
				let arr = hours.split(",");
				console.log(arr);
				for (let i = 0; i < arr.length; i++)
				{
					let strs = arr[i];
					let allstr = strs.split(" + ");
					console.log(allstr);
					let hour = {}
					hour.course = allstr[0];
					hour.instructorType = allstr[1];
					hour.instructor = allstr[2];
					hour.instructorID = allstr[3];
					hour.type = allstr[4];
					hour.place = allstr[5];
					hour.day = allstr[6];
					hour.start = allstr[7];
					hour.end = allstr[8];
					hour.id = allstr[9];
					
					let str = allstr[1] + ", " + allstr[0] + ": " + allstr[7] + " to " + allstr[8] + ", " + allstr[6] + ", " + allstr[5];
					hour.strrep = str;
					finalHours.push(hour)
				}
				//Updates State Accordingly = Final Office Hours Received From Backend.
				this.setState({instructorHours: finalHours});
			}

		});

		xhr1.open("POST", url1);
		xhr2.open("POST", url2);
		
		const form = new FormData();
		//Sends Along Login Username Token To Backend To Query For Specific User Schedule Data.
		form.set("user",user);
		xhr1.send(form);
		xhr2.send(form);
	}

	//Main Rendering For Homepage Data:
	//Includes Schedule, Office Hours, Sections:
	render()
	{
		const homePageStyle =
		{
			margin: "20px"
		};

		return(
			<div style={homePageStyle} className="container-fluid">
				<div className="row justify-content-center">
					<div className="col-xl-9 mr-5">
						<h2>My Schedule:</h2>
						<Schedule />
						<br></br>
						<h2>Office Hours:</h2>
						<p>{this.state.officeHours == "N/A" || this.state.officeHours == "" ? "Hello! Login and Search For Office Hours To Display Them Here." : this.state.officeHours.map(item => <ul key={item.id}>{item}</ul>)}</p><br></br>
						<h2>My Sections:</h2>
						{this.state.instructorHours == "N/A" ? "You Currently Do Not Run Any Office Hours": this.state.instructorHours.map(item => (
							<div key={item.strrep}>
								<EditModal hour={item}/>
							</div>
						))}
					</div>
				</div>
			</div>
		);
	}
}

export default Home;