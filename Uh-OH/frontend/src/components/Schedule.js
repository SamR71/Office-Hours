import React from 'react';
import moment from 'moment';
import WeekCalendar from 'react-week-calendar';
import './ScheduleStyle.css';

class Schedule extends React.Component
{

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
                    /*eventComponent = will take in a component we define to display specific hours*/
                    />
            </div>
        );
    }
}

export default Schedule;