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
                    firstDay = {moment().day(1)}
                    startTime = {moment({h: 8, m: 0})}
                    endTime = {moment({h: 20, m: 0})}
                    scaleUnit = {60}
                    dayFormat = {'dd.'}
                    cellHeight = {50}
                    numberOfDays = {7}
                    useModal = {false}
                    />
            </div>
        );
    }
}

export default Schedule;