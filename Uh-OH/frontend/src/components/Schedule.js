import React from "react";
import moment from "moment";
import WeekCalendar from "react-week-calendar";
import "./ScheduleStyle.css";

class Schedule extends React.Component
{

    constructor(props) {
        super(props);
        this.state =
        {
            lastUID: 2,
            eventIntervals:
            [
                {
                    uid: 1,
                    start: moment({h: 10, m: 0}).day(1), //day 1 is monday
                    end: moment({h: 12, m: 0}).day(1),
                    value: "Test"
                },
            ],
        };
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
                    /*eventComponent = will take in a component to style how events are shown*/
                    />
            </div>
        );
    }
}

export default Schedule;