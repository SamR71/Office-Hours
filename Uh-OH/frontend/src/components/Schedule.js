import React from "react";
import moment from "moment";
import WeekCalendar from "react-week-calendar";
import customEvent from "./customEvent";
import "./ScheduleStyle.css";

class Schedule extends React.Component
{

    state = {
        loggedin: ''
    };
    
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
        // Retrieve login token
        var user = localStorage.getItem('loggedinuser');
        alert(user)
        
		// GET request to get the schedule data.
        // Schedule will be stored in the string 'schedule'
        let schedule = "testing";
        let url = "http://localhost:8000/schedules/get/";
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function()
        {
            if (xhr.readyState === XMLHttpRequest.DONE)
            {
                let status = xhr.status;
                if (status === 0 || (status >= 200 && status < 400))
                {
                    schedule = xhr.responseText;
                    alert(schedule)
                }
                else
                {
                    schedule = "ERROR!"
                }
            }
        };

        //tried to get schedule to say something other than testing this also didnt work
        // get a callback when the server responds
	    //xhr.addEventListener("load", () => {
	        // update the state of the component with the result here
	    //    schedule = xhr.responseText;
	    //})

        xhr.open("POST", url);
        const form = new FormData();

        // Send along login token
        form.set("user",user);
        xhr.send(form);

		this.setState({test: schedule});
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