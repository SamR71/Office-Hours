import React from "react";
import moment from "moment";
import WeekCalendar from "react-week-calendar";
import customEvent from "./customEvent";
import "./ScheduleStyle.css";

/*
The Schedule React Component Serves As The Main Way For User
To View All Their Office Hours Data.
*/
class Schedule extends React.Component
{

	//State Stores Currently Logged In User, OR "" If Not Applicable.
    state = {
        loggedIn: ""
    };
    
    //Initializes All Helper Functions/State Releated Data.
    constructor(props)
	{
        super(props);
        this.state =
        {
            rawData: [],
            eventIntervals: [],
        };
        this.helpFormatStrings = this.helpFormatStrings.bind(this);
        this.numDay = this.numDay.bind(this);
    }

    //Main Mounting Function To Real-Time Update + Retrive + Display User Schedule Data.
    async componentDidMount()
	{
        //Retrieves Login Token = Current Logged In User.
        var user = localStorage.getItem("loggedinuser");
        
		//Send GET Request To Obtain User Schedule Data.
        let schedule = null;
        let url = "http://localhost:8000/schedules/get/";
        let xhr = new XMLHttpRequest();

        //Get A Callback When Backend Server Responds.
	    xhr.addEventListener("load", () => {
	        //Update the State of the Component with the result here.
	        schedule = xhr.responseText;
		    this.setState({rawData: schedule.split(",")});
		    this.helpFormatStrings();
	    });

        xhr.open("POST", url);
        const form = new FormData();
        //Send Along Login Token.
        form.set("user",user);
        xhr.send(form);
	}

	//Helper Function:
	//Takes the Raw String Data + Converts To Event Intervals For React Schedule.
	helpFormatStrings()
	{
		//RESET: Clear Intervals of Old Data.
		this.setState({eventIntervals: []});

		let intervals = [];
		let officeHour = "";
		//Loop Over All Office Hours To Turn Into Intervals:
		for(let i = 1; i < this.state.rawData.length; i++)
		{
			officeHour = this.state.rawData[i];
			const info = officeHour.split(" + ");
			const days = info[3].split("");

			for(let j = 0; j < days.length; j++)
			{
				const start = moment(info[4], "LT").day(this.numDay(days[j]));
				const end = moment(info[5], "LT").day(this.numDay(days[j]));
				const loc = info[2];
				const prof = info[1];
				const courseName = info[0];

				intervals.push({start, end, loc, prof, courseName});
			}
		}
		//Update Event Intervals:
		this.setState({eventIntervals: intervals})
	}

	//Helper Function:
	//Takes Character Sepcifying Day Of Week + Converts Into Number For Moments.
	numDay(day)
	{
		switch(day)
		{
			case "M":
				return 1;
			case "T":
				return 2;
			case "W":
				return 3;
			case "R":
				return 4;
			case "F":
				return 5;
			case "S":
				return 6;
			default:
				return 7;
		}
	}

	//Primary Rendering of User Schedule:
    render()
    {

        return(
            <div>
                <WeekCalendar
                    firstDay = {moment().day(1)}
                    startTime = {moment({h:8, m:0})}
                    endTime = {moment({h:20, m:0})}
                    scaleUnit = {60}
                    scaleFormat = {"h:mm a"}
                    dayFormat = {"dd."}
                    cellHeight = {40}
                    numberOfDays = {7}
                    useModal = {false}
                    eventSpacing = {0}
                    selectedIntervals = {this.state.eventIntervals}
                    eventComponent = {customEvent}
                    />
            </div>
        );
    }
}

export default Schedule;