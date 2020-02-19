import React from 'react';
import moment from 'moment';
import WeekCalendar from 'react-week-calendar';
import 'react-week-calendar/dist/style.css';

class Schedule extends React.Component
{
    render()
    {

        return(
            <div>
                <WeekCalendar
                    startTime = {moment({h: 8, m: 0})}
                    endTime = {moment({h: 21, m: 0})}
                    scaleUnit ={60}
                    scaleHeaderTitle="Time"
                    cellHeight = {50}
                    numberOfDays= {7}
                    />
            </div>
        );
    }
}

export default Schedule;