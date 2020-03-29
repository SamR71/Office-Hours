import React from 'react';
import {withRouter} from 'react-router-dom';

class OfficeHourInfo extends React.Component {
	state = {
		dates: "",
		location: "",
		startTime: "",
		endTime: "",
	};

	constructor(props) {
		super(props);
		this.state = {dates: props.officeHour.meetDates,
					location: props.officeHour.meetLocation,
					startTime: props.officeHour.meetStartTime,
					endTime: props.officeHour.meetEndTime,};
	}
	
	render() {
		return (
			<div>
			{/* The Body Content of the OfficeHourInfo component */}
			{this.state.dates + " | " + this.state.location + " | " + this.state.startTime + "-" + this.state.endTime}
			</div>
		);
	}

}
export default withRouter(OfficeHourInfo);