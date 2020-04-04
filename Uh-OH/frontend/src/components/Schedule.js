import React from "react";
import moment from "moment";
import WeekCalendar from "react-week-calendar";
import customEvent from "./customEvent";
import "./ScheduleStyle.css";

class Schedule extends React.Component
{

    constructor(props)
	{
        super(props);
        this.state =
        {
        	test: "",
            rawData: [],
            eventIntervals: [],
        };
        this.helpFormatStrings = this.helpFormatStrings.bind(this);
    }

    async componentDidMount()
	{
    	try
	    {
    		// GET request using fetch with async/await
		    let xhr = new XMLHttpRequest();
		    let user = localStorage.getItem("loggedinuser");

		    // get a callback when the server responds
		    xhr.addEventListener("load", () => {
				// update the state of the component with the result here
			    this.setState({test: xhr.responseText})
		    });
		    // open the request with the verb and the url
		    xhr.open("GET", "http://localhost:8000/schedules/get/", true, user);
		    // send the request
		    xhr.send();
		}
		catch (e)
		{
			console.log(e);
		}
	}

	helpFormatStrings()
	{
		// clear intervals of any old data
		this.setState({eventIntervals: []});

		let intervals = [];
		let officeHour = "";
		//looping over all office hours to turn into intervals
		for(officeHour in this.state.rawData)
		{
			const info = officeHour.split(" + ");
			const days = info[2].split("");

			const start = moment(info[3], "LT");
			const end = moment(info[4], "LT");
			const value = info[1];

			intervals.push({start, end, value});
		}

		this.setState({eventIntervals: intervals})
	}

    render()
    {

        return(
            <div>
	            {this.state.rawData}
	            {this.state.test}
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