import React from 'react';
import {withRouter} from 'react-router-dom';

/* The MeetingTime component displays information about a CourseMeetingTime object.
 * It displays the information as a string but can be modified 
 */
class MeetingTime extends React.Component 
{
	//Constructor:
	//State Stores All Meeting Time Attributes (i.e., meetType = Lecture, Recitation, Lab, ... 
	//meetDates = MTWRF, ..., meetInstructor = Instructor, meetStartTime = 10:00 AM, ...,
	//meetEndTime = 12:00 PM, ... )
	constructor(props) {
		super(props);
		this.state = {type: props.meeting.meetType,
					dates: props.meeting.meetDates,
					instructor: props.meeting.meetInstructor,
					startTime: props.meeting.meetStartTime,
					endTime: props.meeting.meetEndTime,};
	}
	
	//Main Rendering/Displaying of Meeting Time Data Under SectionModal.
	render() 
	{
		return (
			<div>
			{/* The Body Content of the MeetingTime, currently displays just as text */}
				{this.state.type + " | " +
				this.state.dates + " | " +
				this.state.instructor + " | " +
				this.state.startTime + " to " + this.state.endTime}
			</div>
		);
	}

}
export default withRouter(MeetingTime);