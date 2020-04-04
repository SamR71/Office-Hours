import React from "react";
import moment from "moment";
import WeekCalendar from "react-week-calendar";
import customEvent from "./customEvent";
import "./ScheduleStyle.css";

class Schedule extends React.Component
{

    state = {
        loggedin: ""
    };
    
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
		    this.setState({rawData: schedule.split(",")});
		    this.helpFormatStrings();
	    });

        xhr.open("POST", url);
        const form = new FormData();

        // Send along login token
        form.set("user",user);
        xhr.send(form);
	}

	// this helper functoin takes the raw string data and converts to event interval object
	helpFormatStrings()
	{
		// clear intervals of any old data
		this.setState({eventIntervals: []});

		let intervals = [];
		let officeHour = "";
		//looping over all office hours to turn into intervals
		for(let i = 1; i < this.state.rawData.length; i++)
		{
			officeHour = this.state.rawData[i];
			const info = officeHour.split(" + ");
			const days = info[2].split("");

			for(let j = 0; j < days.length; j++)
			{
				const start = moment(info[3], "LT").day(this.numDay(days[j]));
				const end = moment(info[4], "LT").day(this.numDay(days[j]));
				const value = info[1];

				intervals.push({start, end, value});
			}
		}

		this.setState({eventIntervals: intervals})
	}

	// this helper function takes in the charcter for a day and trurns the number for it for moments
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