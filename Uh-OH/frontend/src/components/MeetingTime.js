import React from 'react';
import {withRouter} from 'react-router-dom';

/* The MeetingTie component displays information about a CourseMeetingTime object.
 * It displays the information as a string but can be modified 
 */
class MeetingTime extends React.Component {
	// the state holds standard info of the fields of a CourseMeetingTime object
	state = {
		type: "",
		dates: "",
		instructor: "",
		startTime: "",
		endTime: "",
	};
	
	
	constructor(props) {
		super(props);
		this.state = {type: props.meeting.meetType,
					dates: props.meeting.meetDates,
					instructor: props.meeting.meetInstructor,
					startTime: props.meeting.meetStartTime,
					endTime: props.meeting.meetEndTime,};
	}
	
	render() {
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