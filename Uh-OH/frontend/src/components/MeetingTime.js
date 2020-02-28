import React from 'react';
import {withRouter} from 'react-router-dom';

class MeetingTime extends React.Component {
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
				{this.state.type + " | " +
				this.state.dates + " | " +
				this.state.instructor + " | " +
				this.state.startTime + " to " + this.state.endTime}
			</div>
		);
	}

}
export default withRouter(MeetingTime);